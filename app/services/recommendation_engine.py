def generate_recommendations(profile):

    recommendations = []


    if profile.system_level == "DELAYED":

        if profile.domain == "Speech & Language":

            recommendations.append(
                {
                    "domain":
                    "Speech & Language",

                    "recommendation":
                    "Practice vocabulary building and two-word combinations",

                    "reason":
                    "Speech development is below expected level"
                }
            )


        elif profile.domain == "Motor":

            recommendations.append(
                {
                    "domain":
                    "Motor",

                    "recommendation":
                    "Practice balance and coordination activities",

                    "reason":
                    "Motor skills need improvement"
                }
            )


    return recommendations