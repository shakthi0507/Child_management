import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models.user import User
from app.models.child import Child
from app.models.therapist import Therapist
from app.models.therapist_assignment import TherapistAssignment
from app.models.goal import Goal
from app.models.goal_milestone import GoalMilestone
from app.models.assessment import Assessment
from app.models.assessment_session import AssessmentSession
from app.models.development_profile import ChildDevelopmentProfile
from app.api.development_profile import DevelopmentProfileConfirm, confirm_profile
from app.services.assessment_scoring import calculate_score, calculate_percentage
from app.services.progress_service import calculate_goal_progress
from app.core.dependencies import ensure_child_access


class ContractTests(unittest.TestCase):
    counter = 0

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)

    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def setUp(self):
        type(self).counter += 1
        suffix = str(type(self).counter)
        self.db = Session(self.engine)
        self.parent = User(username="parent" + suffix, email="parent" + suffix + "@test.com", password="x", role="PARENT")
        self.other_parent = User(username="other" + suffix, email="other" + suffix + "@test.com", password="x", role="PARENT")
        self.therapist_user = User(username="therapist" + suffix, email="therapist" + suffix + "@test.com", password="x", role="THERAPIST")
        self.db.add_all([self.parent, self.other_parent, self.therapist_user])
        self.db.flush()
        self.child = Child(child_code="C1" + suffix, parent_id=self.parent.id, name="Child One")
        self.other_child = Child(child_code="C2" + suffix, parent_id=self.other_parent.id, name="Child Two")
        self.db.add_all([self.child, self.other_child])
        self.db.flush()
        self.therapist = Therapist(user_id=self.therapist_user.id)
        self.db.add(self.therapist)
        self.db.flush()
        self.db.add(TherapistAssignment(therapist_id=self.therapist.id, child_id=self.child.id))
        self.goal = Goal(
            child_id=self.child.id,
            therapist_id=self.therapist_user.id,
            domain="Speech",
            current_level="Beginner",
            short_term_goal="Use words",
            long_term_goal="Speak clearly",
            duration_days=30,
        )
        self.db.add(self.goal)
        self.db.flush()
        self.db.add_all([
            GoalMilestone(goal_id=self.goal.id, title="First", status="COMPLETED"),
            GoalMilestone(goal_id=self.goal.id, title="Second", status="PENDING"),
        ])
        self.db.commit()

    def tearDown(self):
        self.db.rollback()
        self.db.close()

    def test_yes_no_scoring_and_percentage(self):
        self.assertEqual(calculate_score("YES"), 2)
        self.assertEqual(calculate_score("NO"), 0)
        self.assertEqual(calculate_score("SOMETIMES/STARTING"), 1)
        self.assertEqual(calculate_score("Sometimes / Starting"), 1)
        self.assertEqual(calculate_score("NOT YET"), 0)
        self.assertEqual(calculate_percentage([2, 2, 0]), 66.67)
        self.assertEqual(calculate_percentage([]), 0.0)

    def test_parent_and_assigned_therapist_access(self):
        parent = {"id": self.parent.id, "role": "PARENT"}
        therapist = {"id": self.therapist_user.id, "role": "THERAPIST"}
        other_parent = {"id": self.other_parent.id, "role": "PARENT"}
        self.assertEqual(ensure_child_access(self.child.id, parent, self.db).id, self.child.id)
        self.assertEqual(ensure_child_access(self.child.id, therapist, self.db).id, self.child.id)
        with self.assertRaises(Exception):
            ensure_child_access(self.other_child.id, parent, self.db)

    def test_completed_milestones_drive_percentage(self):
        progress = calculate_goal_progress(self.goal.id, self.db)
        self.assertEqual(progress["total_milestones"], 2)
        self.assertEqual(progress["completed"], 1)
        self.assertEqual(progress["percentage"], 50.0)

    def test_therapist_cannot_confirm_unassigned_child_profile(self):
        assessment = Assessment(
            name="Test assessment",
            description="Test",
            assessment_type="THERAPIST_ASSESSMENT",
            age_group="24 months",
            domain="Speech & Language",
            created_by=self.parent.id,
            status="PUBLISHED",
        )
        self.db.add(assessment)
        self.db.flush()
        session = AssessmentSession(
            assessment_id=assessment.id,
            child_id=self.other_child.id,
            therapist_id=self.therapist_user.id,
            status="COMPLETED",
        )
        self.db.add(session)
        self.db.flush()
        profile = ChildDevelopmentProfile(
            child_id=self.other_child.id,
            assessment_session_id=session.id,
            domain="Speech & Language",
            system_level="Below expected level",
            score_percentage=25,
            confirmed=False,
        )
        self.db.add(profile)
        self.db.commit()

        with self.assertRaises(Exception) as error:
            confirm_profile(
                profile.id,
                DevelopmentProfileConfirm(
                    therapist_level="Emerging",
                    clinical_interpretation="Test interpretation",
                    confirmed=True,
                ),
                self.db,
                {"id": self.therapist_user.id, "role": "THERAPIST"},
            )

        self.assertEqual(error.exception.status_code, 403)
        self.db.refresh(profile)
        self.assertFalse(profile.confirmed)


if __name__ == "__main__":
    unittest.main()
