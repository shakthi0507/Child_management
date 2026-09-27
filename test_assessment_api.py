import unittest
import tempfile
import calendar
from pathlib import Path
from unittest.mock import patch
from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.base import Base
from app.database.deps import get_db
from app.models.assessment import Assessment
from app.models.assessment_question import AssessmentQuestion
from app.models.child import Child
from app.models.milestone import Milestone
from app.models.therapist import Therapist
from app.models.therapist_assignment import TherapistAssignment
from app.models.user import User
from app.core.dependencies import get_current_user
from app.core.security import hash_password
from main import app


class AssessmentApiFlowTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        db = self.Session()

        self.parent = User(username="parent", email="parent@test", password="x", role="PARENT")
        self.therapist_user = User(username="therapist", email="therapist@test", password=hash_password("Therapist@123"), role="THERAPIST")
        self.other_therapist_user = User(username="other", email="other@test", password="x", role="THERAPIST")
        self.admin = User(username="admin", email="admin@test", password="x", role="ADMIN")
        db.add_all([self.parent, self.therapist_user, self.other_therapist_user, self.admin])
        db.flush()

        therapist = Therapist(user_id=self.therapist_user.id)
        other_therapist = Therapist(user_id=self.other_therapist_user.id)
        today = date.today()
        child_dob = date(
            today.year - 2,
            today.month,
            min(today.day, calendar.monthrange(today.year - 2, today.month)[1]),
        )
        child = Child(
            child_code="API-CHILD",
            parent_id=self.parent.id,
            name="Test Child",
            dob=child_dob,
        )
        db.add_all([therapist, other_therapist, child])
        db.flush()
        db.add(TherapistAssignment(therapist_id=therapist.id, child_id=child.id))
        milestone = Milestone(
            age_group="24-36",
            expected_month=24,
            domain="Gross Motor",
            title="GM24-01",
            description="Walks independently",
        )
        db.add(milestone)
        db.flush()

        self.parent_assessment = Assessment(
            name="Parent screening",
            description="Parent screening fixture",
            assessment_type="PARENT_SCREENING",
            age_group="24 months",
            domain="Multiple",
            created_by=self.admin.id,
            status="PUBLISHED",
        )
        self.therapist_assessment = Assessment(
            name="Therapist assessment",
            description="Therapist assessment fixture",
            assessment_type="THERAPIST_ASSESSMENT",
            age_group="24-36",
            domain="Gross Motor",
            created_by=self.admin.id,
            status="PUBLISHED",
        )
        db.add_all([self.parent_assessment, self.therapist_assessment])
        db.flush()
        db.add(AssessmentQuestion(
            assessment_id=self.therapist_assessment.id,
            milestone_id=milestone.id,
            question="Walks independently?",
            order=1,
        ))
        db.add(AssessmentQuestion(
            assessment_id=self.parent_assessment.id,
            milestone_id=milestone.id,
            question="Parent screening question?",
            order=1,
        ))
        db.commit()

        self.parent_id = self.parent.id
        self.therapist_id = self.therapist_user.id
        self.other_therapist_id = self.other_therapist_user.id
        self.admin_id = self.admin.id
        self.child_id = child.id
        self.parent_assessment_id = self.parent_assessment.id
        self.therapist_assessment_id = self.therapist_assessment.id
        db.close()

        self.current_user = {"id": self.therapist_id, "role": "THERAPIST"}

        def override_db():
            session = self.Session()
            try:
                yield session
            finally:
                session.close()

        app.dependency_overrides[get_db] = override_db
        app.dependency_overrides[get_current_user] = lambda: self.current_user
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        app.dependency_overrides.clear()
        Base.metadata.drop_all(self.engine)
        self.engine.dispose()

    def test_role_filtered_assessments_and_assigned_child_flow(self):
        therapist_list = self.client.get(f"/assessments/child/{self.child_id}")
        self.assertEqual(therapist_list.status_code, 200)
        self.assertEqual([a["assessment_type"] for a in therapist_list.json()], ["THERAPIST_ASSESSMENT"])

        self.current_user = {"id": self.admin_id, "role": "ADMIN"}
        admin_list = self.client.get("/assessments/")
        self.assertEqual(admin_list.status_code, 200)
        self.assertEqual(len(admin_list.json()), 2)
        self.assertEqual(
            self.client.post("/assessments/start", json={
                "child_id": self.child_id,
                "assessment_id": self.therapist_assessment_id,
            }).status_code,
            403,
        )

        self.current_user = {"id": self.therapist_id, "role": "THERAPIST"}
        self.assertEqual(self.client.post("/assessments/", json={
            "name": "Therapist created template",
            "description": "Not permitted by the current role contract",
            "assessment_type": "THERAPIST_ASSESSMENT",
            "age_group": "24-36",
            "domain": "Motor",
        }).status_code, 403)

        self.current_user = {"id": self.parent_id, "role": "PARENT"}
        parent_list = self.client.get(f"/assessments/child/{self.child_id}")
        self.assertEqual(parent_list.status_code, 200)
        self.assertEqual([a["assessment_type"] for a in parent_list.json()], ["PARENT_SCREENING"])
        self.assertEqual(
            self.client.post("/assessments/start", json={
                "child_id": self.child_id,
                "assessment_id": self.therapist_assessment_id,
            }).status_code,
            403,
        )
        self.assertEqual(self.client.post("/assessments/", json={
            "name": "Parent created template",
            "description": "Not permitted by the current role contract",
            "assessment_type": "PARENT_SCREENING",
            "age_group": "24 months",
            "domain": "Multiple",
        }).status_code, 403)

        self.current_user = {"id": self.other_therapist_id, "role": "THERAPIST"}
        self.assertEqual(self.client.get(f"/assessments/child/{self.child_id}").status_code, 403)

        self.current_user = {"id": self.therapist_id, "role": "THERAPIST"}
        started = self.client.post("/assessments/start", json={
            "child_id": self.child_id,
            "assessment_id": self.therapist_assessment_id,
        })
        self.assertEqual(started.status_code, 200, started.text)
        session_id = started.json()["id"]
        questions = self.client.get(
            f"/assessments/{self.therapist_assessment_id}/questions",
            params={"child_id": self.child_id, "domain": "Gross Motor"},
        )
        self.assertEqual(questions.status_code, 200)
        self.assertTrue(all(question["domain"] == "Gross Motor" for question in questions.json()))
        self.assertEqual(
            self.client.get(
                f"/assessments/{self.therapist_assessment_id}/questions",
                params={"child_id": self.child_id, "domain": "Unspecified"},
            ).json(),
            [],
        )
        question_id = questions.json()[0]["id"]
        response = self.client.post("/assessments/responses", json={
            "session_id": session_id,
            "question_id": question_id,
            "answer": "YES",
            "therapist_remark": "Observed independently",
        })
        self.assertEqual(response.status_code, 200, response.text)
        retried_response = self.client.post("/assessments/responses", json={
            "session_id": session_id,
            "question_id": question_id,
            "answer": "YES",
            "therapist_remark": "Observed independently",
        })
        self.assertEqual(retried_response.status_code, 200, retried_response.text)
        self.assertEqual(retried_response.json()["id"], response.json()["id"])
        completed = self.client.post(
            f"/assessments/{session_id}/complete",
            params={"child_id": self.child_id},
        )
        self.assertEqual(completed.status_code, 200, completed.text)
        completed_again = self.client.post(
            f"/assessments/{session_id}/complete",
            params={"child_id": self.child_id},
        )
        self.assertEqual(completed_again.status_code, 200, completed_again.text)
        self.assertEqual(completed_again.json()["profiles_created"], completed.json()["profiles_created"])
        history = self.client.get(f"/assessments/child/{self.child_id}/sessions")
        self.assertEqual(history.status_code, 200, history.text)
        self.assertEqual(len(history.json()), 1)
        self.assertEqual(history.json()[0]["status"], "COMPLETED")
        result = self.client.get(f"/assessment-result/{session_id}")
        self.assertEqual(result.status_code, 200, result.text)
        self.assertEqual(result.json()["percentage"], 100.0)
        profiles = self.client.get(f"/development-profile/session/{session_id}")
        self.assertEqual(profiles.status_code, 200)
        self.assertEqual(profiles.json()[0]["domain"], "Gross Motor")

        self.current_user = {"id": self.parent_id, "role": "PARENT"}
        parent_session = self.client.post("/assessments/start", json={
            "child_id": self.child_id,
            "assessment_id": self.parent_assessment_id,
        })
        self.assertEqual(parent_session.status_code, 200, parent_session.text)
        parent_session_id = parent_session.json()["id"]
        parent_question = self.client.get(
            f"/assessments/{self.parent_assessment_id}/questions",
            params={"child_id": self.child_id},
        ).json()[0]
        parent_response = self.client.post("/assessments/responses", json={
            "session_id": parent_session_id,
            "question_id": parent_question["id"],
            "answer": "YES",
        })
        self.assertEqual(parent_response.status_code, 200, parent_response.text)
        self.assertEqual(
            self.client.post(
                f"/assessments/{parent_session_id}/complete",
                params={"child_id": self.child_id},
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.get(
                f"/assessments/sessions/{session_id}/responses",
                params={"child_id": self.child_id},
            ).status_code,
            403,
        )

        self.current_user = {"id": self.therapist_id, "role": "THERAPIST"}
        history_types = {
            item["assessment_type"]
            for item in self.client.get(
                f"/assessments/child/{self.child_id}/sessions"
            ).json()
        }
        self.assertEqual(history_types, {"PARENT_SCREENING", "THERAPIST_ASSESSMENT"})
        parent_review = self.client.get(
            f"/assessments/sessions/{parent_session_id}/responses",
            params={"child_id": self.child_id},
        )
        self.assertEqual(parent_review.status_code, 200, parent_review.text)
        self.assertEqual(parent_review.json()[0]["answer"], "YES")

        self.assertEqual(
            self.client.post("/assessments/responses", json={
                "session_id": session_id,
                "question_id": question_id,
                "answer": "NO",
            }).status_code,
            409,
        )

        self.current_user = {"id": self.parent_id, "role": "PARENT"}
        self.assertEqual(
            [item["assessment_type"] for item in self.client.get(
                f"/assessments/child/{self.child_id}/sessions"
            ).json()],
            ["PARENT_SCREENING"],
        )

    def test_parent_child_assessments_are_filtered_by_age_group(self):
        db = self.Session()
        try:
            db.add_all([
                Assessment(
                    name="Inclusive range",
                    description="",
                    assessment_type="PARENT_SCREENING",
                    age_group="24-36",
                    domain="Multiple",
                    created_by=self.admin_id,
                    status="PUBLISHED",
                ),
                Assessment(
                    name="Invalid age label",
                    description="",
                    assessment_type="PARENT_SCREENING",
                    age_group="unknown",
                    domain="Multiple",
                    created_by=self.admin_id,
                    status="PUBLISHED",
                ),
            ])
            db.commit()
            self.current_user = {"id": self.parent_id, "role": "PARENT"}
            response = self.client.get(f"/assessments/child/{self.child_id}")
            self.assertEqual(response.status_code, 200, response.text)
            self.assertEqual(
                {item["name"] for item in response.json()},
                {"Parent screening", "Inclusive range"},
            )
            generic_list = self.client.get(
                "/assessments/", params={"child_id": self.child_id}
            )
            self.assertEqual(generic_list.status_code, 200, generic_list.text)
            self.assertEqual(
                {item["name"] for item in generic_list.json()},
                {"Parent screening", "Inclusive range"},
            )

            child = db.query(Child).filter(Child.id == self.child_id).first()
            today = date.today()
            child.dob = date(
                today.year - 3,
                today.month,
                min(today.day, calendar.monthrange(today.year - 3, today.month)[1]),
            )
            db.commit()
            upper_boundary = self.client.get(f"/assessments/child/{self.child_id}")
            self.assertEqual(upper_boundary.status_code, 200)
            self.assertEqual(
                {item["name"] for item in upper_boundary.json()},
                {"Inclusive range"},
            )

            child.dob = None
            db.commit()
            self.assertEqual(
                self.client.get(f"/assessments/child/{self.child_id}").json(),
                [],
            )
        finally:
            db.close()

    def test_login_jwt_resolves_database_role_for_assigned_assessment_list(self):
        missing_user = self.client.post(
            "/auth/login",
            data={"username": "missing@test", "password": "Wrong@123"},
        )
        wrong_password = self.client.post(
            "/auth/login",
            data={"username": "therapist@test", "password": "Wrong@123"},
        )
        self.assertEqual(missing_user.status_code, 401)
        self.assertEqual(wrong_password.status_code, 401)
        self.assertEqual(missing_user.json()["detail"], wrong_password.json()["detail"])

        app.dependency_overrides.pop(get_current_user)
        invalid_token = self.client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid-token"},
        )
        self.assertEqual(invalid_token.status_code, 401)
        login = self.client.post(
            "/auth/login",
            data={"username": "therapist@test", "password": "Therapist@123"},
        )
        self.assertEqual(login.status_code, 200, login.text)
        token = login.json()["access_token"]

        response = self.client.get(
            f"/assessments/child/{self.child_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()[0]["assessment_type"], "THERAPIST_ASSESSMENT")

    def test_therapist_help_video_is_role_protected(self):
        with tempfile.TemporaryDirectory() as directory:
            video = Path(directory) / "therapist_video.mp4"
            video.write_bytes(b"test-video")
            with patch("app.api.therapist_media.VIDEO_PATH", video):
                self.current_user = {"id": self.therapist_id, "role": "THERAPIST"}
                response = self.client.get("/therapist/help-video")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.content, b"test-video")
                partial = self.client.get(
                    "/therapist/help-video",
                    headers={"Range": "bytes=0-3"},
                )
                self.assertEqual(partial.status_code, 206)
                self.assertEqual(partial.content, b"test")

                self.current_user = {"id": self.parent_id, "role": "PARENT"}
                self.assertEqual(self.client.get("/therapist/help-video").status_code, 403)

                self.current_user = {"id": self.admin_id, "role": "ADMIN"}
                self.assertEqual(self.client.get("/therapist/help-video").status_code, 403)

    def test_voice_audio_survives_transcription_failure_and_is_child_protected(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch("app.api.voice_notes.AUDIO_ROOT", Path(directory)), patch(
                "app.api.voice_notes.transcribe_audio",
                side_effect=RuntimeError("model unavailable"),
            ):
                self.current_user = {
                    "id": self.parent_id,
                    "role": "PARENT",
                    "sub": "parent@test",
                }
                uploaded = self.client.post(
                    "/voice-notes/upload",
                    data={"child_id": self.child_id},
                    files={"file": ("note.wav", b"original-audio", "audio/wav")},
                )
                self.assertEqual(uploaded.status_code, 200, uploaded.text)
                self.assertIsNone(uploaded.json()["transcribed_text"])
                audio_path = Path(directory) / uploaded.json()["audio_path"]
                self.assertEqual(audio_path.read_bytes(), b"original-audio")

                own_audio = self.client.get(
                    f"/voice-notes/{uploaded.json()['id']}/audio"
                )
                self.assertEqual(own_audio.status_code, 200)
                self.assertEqual(own_audio.content, b"original-audio")

                self.current_user = {
                    "id": self.therapist_id,
                    "role": "THERAPIST",
                }
                therapist_audio = self.client.get(
                    f"/voice-notes/{uploaded.json()['id']}/audio"
                )
                self.assertEqual(therapist_audio.status_code, 200)

                self.current_user = {
                    "id": self.other_therapist_id,
                    "role": "THERAPIST",
                }
                self.assertEqual(
                    self.client.get(
                        f"/voice-notes/{uploaded.json()['id']}/audio"
                    ).status_code,
                    403,
                )


if __name__ == "__main__":
    unittest.main()
