def calculate_score(answer: str):
    normalized_answer = answer.upper().strip().replace(" / ", "/").replace(" ", "_")
    scores = {
        "YES": 2,
        "NO": 0,
        "SOMETIMES/STARTING": 1,
        "SOMETIMES_OR_STARTING": 1,
        "NOT_YET": 0,
        "TRUE": 2,
        "FALSE": 0,
        "ACHIEVED": 2,
        "EMERGING": 1,
        "DELAYED": 0,
        "NOT_APPLICABLE": None,
    }
    return scores.get(normalized_answer)


def calculate_percentage(scores: list[int | None]) -> float:
    scored = [score for score in scores if score is not None]
    maximum = len(scored) * 2
    if maximum == 0:
        return 0.0
    return round((sum(scored) / maximum) * 100, 2)
