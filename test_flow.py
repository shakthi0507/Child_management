import requests


BASE_URL = "http://127.0.0.1:8000"


def print_response(name, response):

    print("\n======================")
    print(name)
    print("======================")

    print("Status:", response.status_code)

    try:
        print(response.json())
    except:
        print(response.text)



# -------------------------
# LOGIN
# -------------------------

def login(email, password):

    response = requests.post(

        f"{BASE_URL}/auth/login",

        data={
            "username": email,
            "password": password
        }

    )

    print_response(
        "LOGIN",
        response
    )

    return response.json()["access_token"]



# -------------------------
# MAIN TEST FLOW
# -------------------------

token = login(
    "therapist1@test.com",
    "Therapist@123"
)


headers = {

    "Authorization":
    f"Bearer {token}"

}



# -------------------------
# GET CHILD PROFILES
# -------------------------

response = requests.get(

    f"{BASE_URL}/development-profile/1",

    headers=headers

)

print_response(
    "GET DEVELOPMENT PROFILE",
    response
)



# -------------------------
# CONFIRM PROFILE
# -------------------------

response = requests.put(

    f"{BASE_URL}/development-profile/1/confirm",

    headers=headers,

    json={

        "therapist_level":
        "MODERATE_DELAY",

        "clinical_interpretation":
        "Needs speech intervention"

    }

)


print_response(
    "CONFIRM PROFILE",
    response
)



# -------------------------
# GENERATE RECOMMENDATION
# -------------------------

response = requests.post(

    f"{BASE_URL}/recommendations/generate/1",

    headers=headers

)


print_response(

    "GENERATE RECOMMENDATION",

    response

)