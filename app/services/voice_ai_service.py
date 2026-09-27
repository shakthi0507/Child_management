def generate_voice_insights(
    transcription: str,
    domain: str | None,
    matched_goal_title: str | None,
) -> dict[str, str]:
    text = transcription.strip()
    subject = domain or "general development"

    if not text:
        return {
            "ai_summary": "No speech was detected in the recording.",
            "ai_suggestion": "Record a clear note with the child's activity and observed response.",
        }

    goal_text = f" related to '{matched_goal_title}'" if matched_goal_title else ""
    return {
        "ai_summary": f"Voice note captured {subject} information{goal_text}: {text}",
        "ai_suggestion": f"Review this {subject} observation with the therapist and continue tracking the child's response.",
    }
