"""
CDTMP Complete End-to-End API Test

Flow:
Login
 -> Users
 -> Child
 -> Assessment
 -> Start Assessment
 -> Submit Responses
 -> Complete Assessment
 -> Get Result
 -> Generate Development Profile
 -> Confirm Profile
 -> Generate Goal Recommendation
 -> Create Goal
 -> Create Goal Milestone

Update only the response/question logic if your assessment engine requires
specific question IDs and answers.
"""

import requests
import sys


BASE_URL = "http://127.0.0.1:8000"

TOKENS = {}


def check(name, response):
    print("\n" + "=" * 80)
    print(name)
    print("STATUS:", response.status_code)

    try:
        data = response.json()
        print(data)
        return data if response.status_code < 400 else None
    except Exception:
        print(response.text)
        return None


def login(username, password, role):
    r = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    data = check(f"{role} Login", r)

    if data:
        TOKENS[role] = data["access_token"]

    return data


def headers(role):
    return {
        "Authorization": f"Bearer {TOKENS[role]}"
    }


def main():

    # -------------------------
    # Login
    # -------------------------
    if not login("admin@test.com", "Admin@123", "ADMIN"):
        return

    if not login("therapist1@test.com", "Therapist@123", "THERAPIST"):
        return

    if not login("parent1@test.com", "Parent@123", "PARENT"):
        return


    # -------------------------
    # Users
    # -------------------------
    check(
        "Get Users",
        requests.get(
            f"{BASE_URL}/auth/users",
            headers=headers("ADMIN")
        )
    )


    # -------------------------
    # Child
    # -------------------------
    children = check(
        "Get Children",
        requests.get(
            f"{BASE_URL}/children",
            headers=headers("PARENT")
        )
    )

    child_id = children[0]["id"]


    # -------------------------
    # Assessment
    # -------------------------
    assessments = check(
        "Get Assessments",
        requests.get(
            f"{BASE_URL}/assessments/",
            headers=headers("THERAPIST")
        )
    )

    assessment_id = assessments[0]["id"]


    # -------------------------
    # Start Assessment
    # -------------------------
    session = check(
        "Start Assessment",
        requests.post(
            f"{BASE_URL}/assessments/start",
            json={
                "child_id": child_id,
                "assessment_id": assessment_id
            },
            headers=headers("THERAPIST")
        )
    )

    session_id = session["id"]


    # -------------------------
    # Submit Assessment Responses
    # -------------------------
    # Update this payload based on your question/response schema.
    #
    # Example:
    # {
    #   "session_id": session_id,
    #   "question_id": 1,
    #   "answer": "YES"
    # }
    #
    # Add multiple responses if needed.

    print("\nSubmit assessment responses here based on Swagger schema.")


    # -------------------------
    # Complete Assessment
    # -------------------------
    check(
        "Complete Assessment",
        requests.post(
            f"{BASE_URL}/assessments/{session_id}/complete",
            params={
                "child_id": child_id
            },
            headers=headers("THERAPIST")
        )
    )

    # -------------------------
    # Result
    # -------------------------
    check(
        "Assessment Result",
        requests.get(
            f"{BASE_URL}/assessment-result/{session_id}",
            headers=headers("THERAPIST")
        )
    )


    # -------------------------
    # Development Profile
    # -------------------------
    profile = check(
        "Generate Development Profile",
        requests.post(
            f"{BASE_URL}/development-profile/generate/{session_id}",
            headers=headers("THERAPIST")
        )
    )

    profiles = profile.get("profiles", [])

    if not profiles:
        print("No profile generated. Check assessment responses.")
        return

    profile_id = profiles[0]["id"]


    check(
        "Confirm Development Profile",
        requests.put(
            f"{BASE_URL}/development-profile/{profile_id}/confirm",
            json={
                "confirmed": True
            },
            headers=headers("THERAPIST")
        )
    )


    # -------------------------
    # Recommendations
    # -------------------------
    check(
        "Generate Goal Recommendations",
        requests.post(
            f"{BASE_URL}/goal-recommendations/{child_id}",
            headers=headers("THERAPIST")
        )
    )


    # -------------------------
    # Goal Creation
    # -------------------------
    goal = check(
        "Create Goal",
        requests.post(
            f"{BASE_URL}/goals/",
            json={
                "child_id": child_id,
                "therapist_id": 2,
                "assessment_session_id": session_id,
                "domain": "Speech & Language",
                "current_level": "Beginner",
                "short_term_goal": "Improve word combination",
                "long_term_goal": "Improve communication skills",
                "duration_days": 90
            },
            headers=headers("THERAPIST")
        )
    )

    if goal:
        goal_id = goal["id"]

        check(
            "Create Goal Milestone",
            requests.post(
                f"{BASE_URL}/goal-milestones/",
                json={
                    "goal_id": goal_id,
                    "title": "Practice two word combinations"
                },
                headers=headers("THERAPIST")
            )
        )


    print("\nCOMPLETE FLOW TEST FINISHED")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Backend is not running.")
        print("Run: uvicorn main:app --reload")
        sys.exit(1)
