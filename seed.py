from datetime import date, datetime, timedelta
import os

from app.database.session import SessionLocal, engine
from app.database.base import Base
from app.core.security import hash_password

# Import models so SQLAlchemy registers every table before create_all().
from app.models.user import User
from app.models.child import Child
from app.models.therapist import Therapist
from app.models.therapist_assignment import TherapistAssignment
from app.models.milestone import Milestone
from app.models.assessment import Assessment
from app.models.assessment_question import AssessmentQuestion
from app.models.assessment_session import AssessmentSession
from app.models.assessment_response import AssessmentResponse
from app.models.development_profile import ChildDevelopmentProfile
from app.models.recommendation import Recommendation
from app.models.goal_recommendation import GoalRecommendation
from app.models.goal import Goal
from app.models.goal_milestone import GoalMilestone
from app.models.progress import GoalProgress
from app.models.voice_notes import VoiceNote
from app.services.assessment_scoring import calculate_score


# ============================================================
# WARNING
# ============================================================
# This seed is intentionally a RESET seed.
# It deletes ALL application data and recreates the tables.
#
# BACK UP your database before running this against real data.
#
# Run:
#     python seed.py
#
# ============================================================


def reset_database():
    print("Resetting database...")

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Database reset completed.")


db = SessionLocal()


def _demo_passwords():
    passwords = (
        os.getenv("DEMO_ADMIN_PASSWORD", ""),
        os.getenv("DEMO_PARENT_PASSWORD", ""),
        os.getenv("DEMO_THERAPIST_PASSWORD", ""),
    )
    if any(len(password) < 16 for password in passwords):
        raise RuntimeError(
            "Set DEMO_ADMIN_PASSWORD, DEMO_PARENT_PASSWORD, and "
            "DEMO_THERAPIST_PASSWORD to values of at least 16 characters."
        )
    if len(set(passwords)) != len(passwords):
        raise RuntimeError("Each demo role must have a different password.")
    return passwords


# ============================================================
# USERS
# ============================================================

def create_users():
    admin_password, parent_password, therapist_password = _demo_passwords()
    admin = User(
        username="admin",
        email="admin@test.com",
        password=hash_password(admin_password),
        role="ADMIN",
        is_active=True,
    )

    parent1 = User(
        username="parent1",
        email="parent1@test.com",
        password=hash_password(parent_password),
        role="PARENT",
        is_active=True,
    )

    parent2 = User(
        username="parent2",
        email="parent2@test.com",
        password=hash_password(parent_password),
        role="PARENT",
        is_active=True,
    )

    parent3 = User(
        username="parent3",
        email="parent3@test.com",
        password=hash_password(parent_password),
        role="PARENT",
        is_active=True,
    )

    therapist1 = User(
        username="therapist1",
        email="therapist1@test.com",
        password=hash_password(therapist_password),
        role="THERAPIST",
        is_active=True,
    )

    therapist2 = User(
        username="therapist2",
        email="therapist2@test.com",
        password=hash_password(therapist_password),
        role="THERAPIST",
        is_active=True,
    )

    therapist3 = User(
        username="therapist3",
        email="therapist3@test.com",
        password=hash_password(therapist_password),
        role="THERAPIST",
        is_active=True,
    )

    db.add_all([
        admin,
        parent1,
        parent2,
        parent3,
        therapist1,
        therapist2,
        therapist3,
    ])

    db.commit()

    for user in [
        admin,
        parent1,
        parent2,
        parent3,
        therapist1,
        therapist2,
        therapist3,
    ]:
        db.refresh(user)

    return {
        "admin": admin,
        "parents": [parent1, parent2, parent3],
        "therapists": [therapist1, therapist2, therapist3],
    }


# ============================================================
# THERAPIST PROFILES
# ============================================================

def create_therapists(users):
    therapist1 = Therapist(
        user_id=users["therapists"][0].id,
        specialization="Speech & Language",
        experience="6 years",
    )

    therapist2 = Therapist(
        user_id=users["therapists"][1].id,
        specialization="Occupational Therapy",
        experience="5 years",
    )

    therapist3 = Therapist(
        user_id=users["therapists"][2].id,
        specialization="Child Development",
        experience="8 years",
    )

    db.add_all([
        therapist1,
        therapist2,
        therapist3,
    ])

    db.commit()

    for therapist in [therapist1, therapist2, therapist3]:
        db.refresh(therapist)

    return [therapist1, therapist2, therapist3]


# ============================================================
# CHILDREN
# ============================================================

def create_children(users):
    parents = users["parents"]

    children = [
        # Parent 1 -> 3 children
        Child(
            child_code="CHILD001",
            parent_id=parents[0].id,
            name="Arjun",
            dob=date(2024, 1, 10),
            gender="Male",
            height=90,
            weight=12,
        ),
        Child(
            child_code="CHILD002",
            parent_id=parents[0].id,
            name="Diya",
            dob=date(2022, 7, 15),
            gender="Female",
            height=101,
            weight=15,
        ),
        Child(
            child_code="CHILD003",
            parent_id=parents[0].id,
            name="Kavin",
            dob=date(2020, 11, 3),
            gender="Male",
            height=112,
            weight=19,
        ),

        # Parent 2 -> 2 children
        Child(
            child_code="CHILD004",
            parent_id=parents[1].id,
            name="Meera",
            dob=date(2023, 3, 20),
            gender="Female",
            height=96,
            weight=14,
        ),
        Child(
            child_code="CHILD005",
            parent_id=parents[1].id,
            name="Rohan",
            dob=date(2021, 9, 8),
            gender="Male",
            height=108,
            weight=17,
        ),

        # Parent 3 -> 2 children
        Child(
            child_code="CHILD006",
            parent_id=parents[2].id,
            name="Ananya",
            dob=date(2024, 5, 2),
            gender="Female",
            height=86,
            weight=11,
        ),
        Child(
            child_code="CHILD007",
            parent_id=parents[2].id,
            name="Vishal",
            dob=date(2019, 12, 18),
            gender="Male",
            height=118,
            weight=21,
        ),
    ]

    db.add_all(children)
    db.commit()

    for child in children:
        db.refresh(child)

    return children


# ============================================================
# THERAPIST ASSIGNMENTS
# ============================================================

def create_assignments(therapists, children):
    # Therapist 1: Arjun, Diya, Meera
    # Therapist 2: Kavin, Rohan, Ananya
    # Therapist 3: Vishal, Diya
    assignments = [
        TherapistAssignment(
            therapist_id=therapists[0].id,
            child_id=children[0].id,
        ),
        TherapistAssignment(
            therapist_id=therapists[0].id,
            child_id=children[1].id,
        ),
        TherapistAssignment(
            therapist_id=therapists[0].id,
            child_id=children[3].id,
        ),

        TherapistAssignment(
            therapist_id=therapists[1].id,
            child_id=children[2].id,
        ),
        TherapistAssignment(
            therapist_id=therapists[1].id,
            child_id=children[4].id,
        ),
        TherapistAssignment(
            therapist_id=therapists[1].id,
            child_id=children[5].id,
        ),

        TherapistAssignment(
            therapist_id=therapists[2].id,
            child_id=children[6].id,
        ),
        TherapistAssignment(
            therapist_id=therapists[2].id,
            child_id=children[1].id,
        ),
    ]

    db.add_all(assignments)
    db.commit()

    return assignments


# ============================================================
# DEVELOPMENT MILESTONES
# ============================================================

def create_milestones():
    items = [
        # 24-36 months
        Milestone(
            age_group="24-36",
            expected_month=24,
            domain="Speech & Language",
            title="Uses two-word phrases",
            description="Child combines two meaningful words.",
        ),
        Milestone(
            age_group="24-36",
            expected_month=27,
            domain="Speech & Language",
            title="Names familiar objects",
            description="Child names common people and objects.",
        ),
        Milestone(
            age_group="24-36",
            expected_month=30,
            domain="Motor",
            title="Runs independently",
            description="Child runs without support.",
        ),
        Milestone(
            age_group="24-36",
            expected_month=28,
            domain="Social",
            title="Plays with others",
            description="Child interacts with peers during play.",
        ),
        Milestone(
            age_group="24-36",
            expected_month=32,
            domain="Self-help",
            title="Attempts self-feeding",
            description="Child attempts to eat independently.",
        ),

        # 36-48 months
        Milestone(
            age_group="36-48",
            expected_month=36,
            domain="Speech & Language",
            title="Uses short sentences",
            description="Child communicates using simple sentences.",
        ),
        Milestone(
            age_group="36-48",
            expected_month=40,
            domain="Cognition",
            title="Sorts objects",
            description="Child sorts objects by basic characteristics.",
        ),
        Milestone(
            age_group="36-48",
            expected_month=42,
            domain="Motor",
            title="Jumps with both feet",
            description="Child jumps using both feet.",
        ),
        Milestone(
            age_group="36-48",
            expected_month=44,
            domain="Social",
            title="Takes turns",
            description="Child can participate in simple turn-taking.",
        ),

        # 48-60 months
        Milestone(
            age_group="48-60",
            expected_month=48,
            domain="Speech & Language",
            title="Tells a simple story",
            description="Child communicates a short sequence of events.",
        ),
        Milestone(
            age_group="48-60",
            expected_month=50,
            domain="Cognition",
            title="Counts objects",
            description="Child counts a small group of objects.",
        ),
        Milestone(
            age_group="48-60",
            expected_month=52,
            domain="Motor",
            title="Balances on one foot",
            description="Child maintains balance briefly on one foot.",
        ),
        Milestone(
            age_group="48-60",
            expected_month=55,
            domain="Self-help",
            title="Dresses with minimal help",
            description="Child participates in dressing independently.",
        ),
    ]

    db.add_all(items)
    db.commit()

    for item in items:
        db.refresh(item)

    return items


# ============================================================
# ASSESSMENTS + QUESTIONS
# ============================================================

def create_assessments(admin, milestones):
    assessment1 = Assessment(
        name="24-36 Development Assessment",
        description="Parent-friendly developmental screening for children aged 24-36 months.",
        assessment_type="PARENT_SCREENING",
        age_group="24-36",
        domain="Multiple",
        created_by=admin.id,
        status="PUBLISHED",
        version=1,
    )

    assessment2 = Assessment(
        name="36-48 Development Assessment",
        description="Developmental assessment for children aged 36-48 months.",
        assessment_type="THERAPIST_ASSESSMENT",
        age_group="36-48",
        domain="Multiple",
        created_by=admin.id,
        status="PUBLISHED",
        version=1,
    )

    assessment3 = Assessment(
        name="48-60 Development Assessment",
        description="Developmental assessment for children aged 48-60 months.",
        assessment_type="THERAPIST_ASSESSMENT",
        age_group="48-60",
        domain="Multiple",
        created_by=admin.id,
        status="PUBLISHED",
        version=1,
    )

    db.add_all([
        assessment1,
        assessment2,
        assessment3,
    ])

    db.commit()

    for assessment in [
        assessment1,
        assessment2,
        assessment3,
    ]:
        db.refresh(assessment)

    milestone_map = {
        "24-36": [m for m in milestones if m.age_group == "24-36"],
        "36-48": [m for m in milestones if m.age_group == "36-48"],
        "48-60": [m for m in milestones if m.age_group == "48-60"],
    }

    questions = []

    for assessment, age_group in [
        (assessment1, "24-36"),
        (assessment2, "36-48"),
        (assessment3, "48-60"),
    ]:
        for index, milestone in enumerate(
            milestone_map[age_group],
            start=1,
        ):
            questions.append(
                AssessmentQuestion(
                    assessment_id=assessment.id,
                    milestone_id=milestone.id,
                    question=milestone.description,
                    order=index,
                )
            )

    db.add_all(questions)
    db.commit()

    for question in questions:
        db.refresh(question)

    return [
        assessment1,
        assessment2,
        assessment3,
    ], questions


# ============================================================
# COMPLETED ASSESSMENT SESSION
# ============================================================

def create_assessment_session(
    child,
    assessment,
    therapist_user,
    questions,
    answer_pattern,
):
    session = AssessmentSession(
        assessment_id=assessment.id,
        child_id=child.id,
        therapist_id=therapist_user.id,
        status="COMPLETED",
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    for index, question in enumerate(questions):
        answer = answer_pattern[index % len(answer_pattern)]

        score = calculate_score(answer)

        response = AssessmentResponse(
            session_id=session.id,
            question_id=question.id,
            answer=answer,
            score=score,
            therapist_remark=(
                "Child demonstrated the skill."
                if answer == "YES"
                else "Skill needs additional practice."
            ),
        )

        db.add(response)

    db.commit()

    return session


# ============================================================
# DEVELOPMENT PROFILE
# ============================================================

def create_profile(
    child,
    session,
    domain,
    level,
    score,
    gap,
    therapist_level,
    interpretation,
):
    profile = ChildDevelopmentProfile(
        child_id=child.id,
        assessment_session_id=session.id,
        domain=domain,
        system_level=level,
        score_percentage=score,
        development_gap=gap,
        therapist_level=therapist_level,
        clinical_interpretation=interpretation,
        confirmed=True,
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


# ============================================================
# RECOMMENDATIONS
# ============================================================

def create_recommendation(
    child,
    profile,
    domain,
    recommendation_text,
    reason,
    therapist_note=None,
):
    recommendation = Recommendation(
        child_id=child.id,
        profile_id=profile.id,
        domain=domain,
        recommendation=recommendation_text,
        reason=reason,
        status="REVIEWED" if therapist_note else "PENDING",
        therapist_note=therapist_note,
        created_by="AI",
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    return recommendation


# ============================================================
# GOALS + MILESTONES + PROGRESS
# ============================================================

def create_goal(
    child,
    therapist_user,
    domain,
    current_level,
    short_term,
    long_term,
    milestone_data,
):
    goal = Goal(
        child_id=child.id,
        therapist_id=therapist_user.id,
        domain=domain,
        current_level=current_level,
        short_term_goal=short_term,
        long_term_goal=long_term,
        duration_days=90,
        status="ACTIVE",
    )

    db.add(goal)
    db.commit()
    db.refresh(goal)

    created_milestones = []

    for item in milestone_data:
        status = item.get("status", "PENDING")

        completed_date = (
            datetime.utcnow() - timedelta(days=item.get("days_ago", 1))
            if status == "COMPLETED"
            else None
        )

        milestone = GoalMilestone(
            goal_id=goal.id,
            title=item["title"],
            description=item["description"],
            status=status,
            target_date=datetime.utcnow()
            + timedelta(days=item.get("target_days", 30)),
            completed_date=completed_date,
        )

        db.add(milestone)
        db.commit()
        db.refresh(milestone)

        created_milestones.append(milestone)

        # Create a progress record for every milestone.
        progress = GoalProgress(
            goal_id=goal.id,
            milestone_id=milestone.id,
            updated_by=therapist_user.id,
            status=status,
            notes=item.get(
                "notes",
                "Therapy progress recorded.",
            ),
        )

        db.add(progress)
        db.commit()

    return goal, created_milestones


# ============================================================
# GOAL RECOMMENDATIONS
# ============================================================

def create_goal_recommendation(
    child,
    session,
    domain,
    priority,
    current_level,
    gap,
    short_term,
    long_term,
    therapist_user=None,
    status="PENDING_REVIEW",
    notes=None,
):
    item = GoalRecommendation(
        child_id=child.id,
        assessment_session_id=session.id,
        domain=domain,
        priority=priority,
        current_level=current_level,
        development_gap=gap,
        short_term_goal=short_term,
        long_term_goal=long_term,
        duration_days=90,
        status=status,
        reviewed_by=(
            therapist_user.id
            if therapist_user
            else None
        ),
        therapist_notes=notes,
        reviewed_at=(
            datetime.utcnow()
            if therapist_user
            else None
        ),
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


# ============================================================
# CHILD DATA
# ============================================================

def create_child_data(
    child,
    therapist_user,
    assessment,
    assessment_questions,
    profile_config,
    goals_config,
    recommendation_config,
):
    session = create_assessment_session(
        child=child,
        assessment=assessment,
        therapist_user=therapist_user,
        questions=assessment_questions,
        answer_pattern=profile_config["answers"],
    )

    profile = create_profile(
        child=child,
        session=session,
        domain=profile_config["domain"],
        level=profile_config["system_level"],
        score=profile_config["score"],
        gap=profile_config["gap"],
        therapist_level=profile_config["therapist_level"],
        interpretation=profile_config["interpretation"],
    )

    create_recommendation(
        child=child,
        profile=profile,
        domain=recommendation_config["domain"],
        recommendation_text=recommendation_config["recommendation"],
        reason=recommendation_config["reason"],
        therapist_note=recommendation_config.get("therapist_note"),
    )

    for goal_config in goals_config:
        create_goal(
            child=child,
            therapist_user=therapist_user,
            domain=goal_config["domain"],
            current_level=goal_config["current_level"],
            short_term=goal_config["short_term"],
            long_term=goal_config["long_term"],
            milestone_data=goal_config["milestones"],
        )

    create_goal_recommendation(
        child=child,
        session=session,
        domain=recommendation_config["domain"],
        priority=recommendation_config.get(
            "priority",
            "MEDIUM",
        ),
        current_level=profile_config["therapist_level"],
        gap=profile_config["gap"],
        short_term=goals_config[0]["short_term"],
        long_term=goals_config[0]["long_term"],
        therapist_user=therapist_user,
        status="APPROVED",
        notes="Seeded therapist recommendation.",
    )

    return session, profile


# ============================================================
# MAIN
# ============================================================

def main():
    # Validate credentials before the reset fixture drops any existing data.
    _demo_passwords()
    reset_database()

    users = create_users()

    therapists = create_therapists(users)

    children = create_children(users)

    create_assignments(
        therapists,
        children,
    )

    milestones = create_milestones()

    assessments, all_questions = create_assessments(
        users["admin"],
        milestones,
    )

    questions_by_assessment = {}

    for question in all_questions:
        questions_by_assessment.setdefault(
            question.assessment_id,
            []
        ).append(question)

    # --------------------------------------------------------
    # Child 1 - Arjun
    # Parent 1
    # Therapist 1
    # 24-36 assessment
    # --------------------------------------------------------
    create_child_data(
        child=children[0],
        therapist_user=users["therapists"][0],
        assessment=assessments[0],
        assessment_questions=questions_by_assessment[
            assessments[0].id
        ],
        profile_config={
            "answers": ["YES", "YES", "YES", "NO", "YES"],
            "domain": "Multiple",
            "system_level": "NORMAL",
            "score": 80,
            "gap": "Minor speech and social interaction practice recommended.",
            "therapist_level": "GOOD",
            "interpretation": "Child is progressing well with minor areas for additional stimulation.",
        },
        goals_config=[
            {
                "domain": "Speech & Language",
                "current_level": "Emerging",
                "short_term": "Improve vocabulary and two-word combinations.",
                "long_term": "Speak complete age-appropriate sentences.",
                "milestones": [
                    {
                        "title": "Learn 10 new words",
                        "description": "Use 10 new familiar words during daily activities.",
                        "status": "COMPLETED",
                        "days_ago": 15,
                    },
                    {
                        "title": "Combine two words",
                        "description": "Use two meaningful words together.",
                        "status": "IN_PROGRESS",
                    },
                    {
                        "title": "Use simple sentences",
                        "description": "Use short sentences during structured activities.",
                        "status": "PENDING",
                    },
                ],
            },
            {
                "domain": "Social",
                "current_level": "Good",
                "short_term": "Increase interaction with peers.",
                "long_term": "Participate in cooperative play.",
                "milestones": [
                    {
                        "title": "Respond during play",
                        "description": "Respond to another child during guided play.",
                        "status": "COMPLETED",
                        "days_ago": 10,
                    },
                    {
                        "title": "Take turns",
                        "description": "Participate in simple turn-taking.",
                        "status": "IN_PROGRESS",
                    },
                ],
            },
        ],
        recommendation_config={
            "domain": "Speech & Language",
            "recommendation": "Practice vocabulary activities and two-word phrases daily.",
            "reason": "Minor speech improvement needed.",
            "priority": "MEDIUM",
            "therapist_note": "Continue home vocabulary activities.",
        },
    )

    # --------------------------------------------------------
    # Child 2 - Diya
    # Parent 1
    # Therapist 1 + Therapist 3
    # 24-36 assessment
    # --------------------------------------------------------
    create_child_data(
        child=children[1],
        therapist_user=users["therapists"][0],
        assessment=assessments[0],
        assessment_questions=questions_by_assessment[
            assessments[0].id
        ],
        profile_config={
            "answers": ["YES", "NO", "YES", "YES", "NO"],
            "domain": "Multiple",
            "system_level": "DELAYED",
            "score": 60,
            "gap": "Speech and self-help skills need additional support.",
            "therapist_level": "NEEDS_SUPPORT",
            "interpretation": "Child would benefit from structured speech and self-help activities.",
        },
        goals_config=[
            {
                "domain": "Speech & Language",
                "current_level": "Developing",
                "short_term": "Increase functional vocabulary.",
                "long_term": "Communicate needs using short sentences.",
                "milestones": [
                    {
                        "title": "Name 5 objects",
                        "description": "Name five familiar objects.",
                        "status": "COMPLETED",
                        "days_ago": 8,
                    },
                    {
                        "title": "Use two-word phrases",
                        "description": "Combine two meaningful words.",
                        "status": "IN_PROGRESS",
                    },
                    {
                        "title": "Use three-word phrases",
                        "description": "Use simple three-word phrases.",
                        "status": "PENDING",
                    },
                ],
            },
            {
                "domain": "Self-help",
                "current_level": "Emerging",
                "short_term": "Improve independent feeding.",
                "long_term": "Complete basic self-help routines with minimal support.",
                "milestones": [
                    {
                        "title": "Hold spoon",
                        "description": "Hold a spoon during meals.",
                        "status": "IN_PROGRESS",
                    },
                    {
                        "title": "Self-feed",
                        "description": "Eat part of a meal independently.",
                        "status": "PENDING",
                    },
                ],
            },
        ],
        recommendation_config={
            "domain": "Speech & Language",
            "recommendation": "Use picture cards and daily naming activities.",
            "reason": "Speech delay identified during screening.",
            "priority": "HIGH",
            "therapist_note": "Continue structured language stimulation.",
        },
    )

    # --------------------------------------------------------
    # Child 3 - Kavin
    # Parent 1
    # Therapist 2
    # 36-48 assessment
    # --------------------------------------------------------
    create_child_data(
        child=children[2],
        therapist_user=users["therapists"][1],
        assessment=assessments[1],
        assessment_questions=questions_by_assessment[
            assessments[1].id
        ],
        profile_config={
            "answers": ["YES", "YES", "YES", "NO"],
            "domain": "Multiple",
            "system_level": "NORMAL",
            "score": 75,
            "gap": "Minor social turn-taking practice recommended.",
            "therapist_level": "GOOD",
            "interpretation": "Motor and cognition skills are progressing appropriately.",
        },
        goals_config=[
            {
                "domain": "Motor",
                "current_level": "Good",
                "short_term": "Improve balance and coordination.",
                "long_term": "Perform age-appropriate gross motor activities independently.",
                "milestones": [
                    {
                        "title": "Jump with both feet",
                        "description": "Jump forward using both feet.",
                        "status": "COMPLETED",
                        "days_ago": 20,
                    },
                    {
                        "title": "Balance on one foot",
                        "description": "Maintain single-leg balance briefly.",
                        "status": "IN_PROGRESS",
                    },
                    {
                        "title": "Catch a large ball",
                        "description": "Catch a large ball from a short distance.",
                        "status": "PENDING",
                    },
                ],
            },
        ],
        recommendation_config={
            "domain": "Motor",
            "recommendation": "Continue balance and coordination games.",
            "reason": "Motor development is progressing well.",
            "priority": "LOW",
        },
    )

    # --------------------------------------------------------
    # Child 4 - Meera
    # Parent 2
    # Therapist 1
    # 24-36 assessment
    # --------------------------------------------------------
    create_child_data(
        child=children[3],
        therapist_user=users["therapists"][0],
        assessment=assessments[0],
        assessment_questions=questions_by_assessment[
            assessments[0].id
        ],
        profile_config={
            "answers": ["YES", "YES", "NO", "YES", "YES"],
            "domain": "Multiple",
            "system_level": "NORMAL",
            "score": 80,
            "gap": "Motor coordination needs additional practice.",
            "therapist_level": "GOOD",
            "interpretation": "Overall development is good with a small motor coordination gap.",
        },
        goals_config=[
            {
                "domain": "Motor",
                "current_level": "Developing",
                "short_term": "Improve running and jumping coordination.",
                "long_term": "Perform age-appropriate gross motor activities confidently.",
                "milestones": [
                    {
                        "title": "Run independently",
                        "description": "Run without losing balance.",
                        "status": "COMPLETED",
                        "days_ago": 12,
                    },
                    {
                        "title": "Jump independently",
                        "description": "Jump forward with both feet.",
                        "status": "IN_PROGRESS",
                    },
                ],
            },
        ],
        recommendation_config={
            "domain": "Motor",
            "recommendation": "Use outdoor running, jumping and balance games.",
            "reason": "Motor coordination requires additional stimulation.",
            "priority": "MEDIUM",
        },
    )

    # --------------------------------------------------------
    # Child 5 - Rohan
    # Parent 2
    # Therapist 2
    # 36-48 assessment
    # --------------------------------------------------------
    create_child_data(
        child=children[4],
        therapist_user=users["therapists"][1],
        assessment=assessments[1],
        assessment_questions=questions_by_assessment[
            assessments[1].id
        ],
        profile_config={
            "answers": ["YES", "YES", "NO", "NO"],
            "domain": "Multiple",
            "system_level": "DELAYED",
            "score": 50,
            "gap": "Social and motor development require additional support.",
            "therapist_level": "NEEDS_SUPPORT",
            "interpretation": "Child needs structured therapy activities across social and motor domains.",
        },
        goals_config=[
            {
                "domain": "Social",
                "current_level": "Emerging",
                "short_term": "Improve turn-taking and peer interaction.",
                "long_term": "Participate in cooperative group play.",
                "milestones": [
                    {
                        "title": "Take turns",
                        "description": "Take turns during a structured game.",
                        "status": "IN_PROGRESS",
                    },
                    {
                        "title": "Join group play",
                        "description": "Join a small group activity.",
                        "status": "PENDING",
                    },
                    {
                        "title": "Share toys",
                        "description": "Share a preferred toy during play.",
                        "status": "PENDING",
                    },
                ],
            },
            {
                "domain": "Motor",
                "current_level": "Developing",
                "short_term": "Improve coordination.",
                "long_term": "Perform age-appropriate gross motor activities.",
                "milestones": [
                    {
                        "title": "Jump with both feet",
                        "description": "Jump using both feet.",
                        "status": "COMPLETED",
                        "days_ago": 7,
                    },
                    {
                        "title": "Balance",
                        "description": "Maintain balance during simple activities.",
                        "status": "IN_PROGRESS",
                    },
                ],
            },
        ],
        recommendation_config={
            "domain": "Social",
            "recommendation": "Use turn-taking games and structured peer activities.",
            "reason": "Social interaction skills need additional support.",
            "priority": "HIGH",
            "therapist_note": "Review social interaction progress weekly.",
        },
    )

    # --------------------------------------------------------
    # Child 6 - Ananya
    # Parent 3
    # Therapist 2
    # 24-36 assessment
    # --------------------------------------------------------
    create_child_data(
        child=children[5],
        therapist_user=users["therapists"][1],
        assessment=assessments[0],
        assessment_questions=questions_by_assessment[
            assessments[0].id
        ],
        profile_config={
            "answers": ["YES", "YES", "YES", "YES", "YES"],
            "domain": "Multiple",
            "system_level": "NORMAL",
            "score": 100,
            "gap": "No significant developmental gap identified.",
            "therapist_level": "EXCELLENT",
            "interpretation": "Child is meeting the assessed milestones appropriately.",
        },
        goals_config=[
            {
                "domain": "Speech & Language",
                "current_level": "Good",
                "short_term": "Expand vocabulary through play.",
                "long_term": "Use age-appropriate sentences consistently.",
                "milestones": [
                    {
                        "title": "Name familiar objects",
                        "description": "Name common objects during play.",
                        "status": "COMPLETED",
                        "days_ago": 25,
                    },
                    {
                        "title": "Use short phrases",
                        "description": "Use short phrases during conversation.",
                        "status": "COMPLETED",
                        "days_ago": 12,
                    },
                ],
            },
        ],
        recommendation_config={
            "domain": "Speech & Language",
            "recommendation": "Continue age-appropriate conversation and reading activities.",
            "reason": "Development is progressing appropriately.",
            "priority": "LOW",
        },
    )

    # --------------------------------------------------------
    # Child 7 - Vishal
    # Parent 3
    # Therapist 3
    # 48-60 assessment
    # --------------------------------------------------------
    create_child_data(
        child=children[6],
        therapist_user=users["therapists"][2],
        assessment=assessments[2],
        assessment_questions=questions_by_assessment[
            assessments[2].id
        ],
        profile_config={
            "answers": ["YES", "NO", "YES", "YES"],
            "domain": "Multiple",
            "system_level": "NORMAL",
            "score": 75,
            "gap": "Cognition and counting activities need reinforcement.",
            "therapist_level": "GOOD",
            "interpretation": "Child is progressing well with some areas requiring continued practice.",
        },
        goals_config=[
            {
                "domain": "Cognition",
                "current_level": "Developing",
                "short_term": "Improve object counting and sorting.",
                "long_term": "Complete age-appropriate early learning activities independently.",
                "milestones": [
                    {
                        "title": "Sort objects",
                        "description": "Sort objects by color or shape.",
                        "status": "COMPLETED",
                        "days_ago": 18,
                    },
                    {
                        "title": "Count objects",
                        "description": "Count a small group of objects.",
                        "status": "IN_PROGRESS",
                    },
                    {
                        "title": "Identify numbers",
                        "description": "Identify basic numbers during activities.",
                        "status": "PENDING",
                    },
                ],
            },
            {
                "domain": "Self-help",
                "current_level": "Good",
                "short_term": "Improve dressing independence.",
                "long_term": "Complete basic dressing routines independently.",
                "milestones": [
                    {
                        "title": "Put on shirt",
                        "description": "Put on a simple shirt with minimal help.",
                        "status": "COMPLETED",
                        "days_ago": 14,
                    },
                    {
                        "title": "Dress independently",
                        "description": "Complete most dressing steps independently.",
                        "status": "IN_PROGRESS",
                    },
                ],
            },
        ],
        recommendation_config={
            "domain": "Cognition",
            "recommendation": "Use counting games, sorting activities and simple number exercises.",
            "reason": "Early learning skills need reinforcement.",
            "priority": "MEDIUM",
            "therapist_note": "Continue cognitive stimulation activities at home.",
        },
    )

    print("")
    print("=" * 60)
    print("SEED COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print("")
    print("ADMIN")
    print("  admin@test.com")
    print("")
    print("PARENTS")
    print("  parent1@test.com  -> Arjun, Diya, Kavin")
    print("  parent2@test.com  -> Meera, Rohan")
    print("  parent3@test.com  -> Ananya, Vishal")
    print("")
    print("THERAPISTS")
    print("  therapist1@test.com")
    print("  therapist2@test.com")
    print("  therapist3@test.com")
    print("")
    print("Children: 7")
    print("Parents: 3")
    print("Therapists: 3")
    print("Assessments: 3")
    print("Multiple therapist-child assignments created.")
    print("Multiple goals and milestone statuses created.")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        db.rollback()
        print("")
        print("SEED FAILED")
        print(type(e).__name__, ":", e)
        raise

    finally:
        db.close()
