def calculate_priority(score):


    if score < 40:

        return "HIGH"


    elif score < 70:

        return "MEDIUM"


    else:

        return "LOW"





def generate_goal(domain, level):


    goals = {


        "Speech & Language": {

            "short":
            "Improve expressive communication and vocabulary",

            "long":
            "Achieve age appropriate speech and language skills"

        },


        "Motor": {

            "short":
            "Improve coordination and movement activities",

            "long":
            "Achieve age appropriate motor development"

        },


        "Social": {

            "short":
            "Increase social interaction and engagement",

            "long":
            "Develop age appropriate social skills"

        },


        "Cognition": {

            "short":
            "Improve attention and problem solving skills",

            "long":
            "Develop cognitive abilities according to age"

        },


        "Behaviour": {

            "short":
            "Improve emotional regulation and behaviour patterns",

            "long":
            "Develop adaptive behavioural skills"

        },


        "Self-help": {

            "short":
            "Improve independence in daily activities",

            "long":
            "Achieve age appropriate self-help skills"

        }

    }



    return goals.get(

        domain,

        {

            "short":
            f"Improve {domain} skills",

            "long":
            "Achieve developmental milestones"

        }

    )