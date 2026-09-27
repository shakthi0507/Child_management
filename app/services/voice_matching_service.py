def match_voice_note(
    text: str,
    goals
):


    if not goals:

        return {

            "goal_id": None,

            "domain": None,

            "confidence": 0,

            "title": None

        }



    text = text.lower()



    best_match = None

    highest_score = 0





    for goal in goals:


        score = 0



        # Check domain

        if goal.domain:

            domain = goal.domain.lower()


            if domain in text:

                score += 3





        # Check short term goal

        if goal.short_term_goal:

            words = (
                goal.short_term_goal
                .lower()
                .split()
            )


            for word in words:

                if word in text:

                    score += 1





        # Check long term goal

        if goal.long_term_goal:

            words = (
                goal.long_term_goal
                .lower()
                .split()
            )


            for word in words:

                if word in text:

                    score += 1





        if score > highest_score:

            highest_score = score

            best_match = goal






    if best_match:


        return {


            "goal_id":
                best_match.id,


            "domain":
                best_match.domain,


            "confidence":
                min(
                    highest_score * 20,
                    100
                ),

            "title": best_match.short_term_goal


        }





    return {


        "goal_id":
            None,


        "domain":
            None,


        "confidence": 0,

        "title": None


    }