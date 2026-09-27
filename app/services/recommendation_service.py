def generate_recommendations(
    domain_results: list[dict],
    goals: list,
    progress_percentage: float | None,
) -> list[str]:
    """Return rule-based suggestions grounded in recorded profile and progress data."""
    recommendations = []

    domain_suggestions = {
        "Speech & Language": "Practice vocabulary, communication and interaction activities.",
        "Gross Motor": "Include movement, balance and coordination activities.",
        "Fine Motor": "Practice age-appropriate grasping and hand coordination activities.",
        "Motor": "Include movement, balance and coordination activities.",
        "Social & Emotional": "Encourage social play and interaction activities.",
        "Social": "Encourage social play and interaction activities.",
        "Adaptive / Self-Help": "Encourage independent daily living activities.",
        "Self-help": "Encourage independent daily living activities.",
        "Cognition": "Include problem solving and learning activities.",
    }

    for domain in domain_results:
        name = domain.get("domain", "")
        if domain.get("status", "").upper() in {"DELAYED", "LOW"}:
            suggestion = domain_suggestions.get(name)
            if suggestion:
                recommendations.append(suggestion)

    if progress_percentage is not None:
        if progress_percentage < 40:
            recommendations.append("Review current goals with the therapist and maintain consistent practice.")
        elif progress_percentage < 80:
            recommendations.append("Continue therapy activities and monitor improvement.")
        else:
            recommendations.append("Recorded milestone progress is high; continue current activities.")

    if not goals and domain_results:
        recommendations.append("Review the assessment profile with the therapist when planning goals.")

    return recommendations
