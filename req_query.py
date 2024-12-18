import requests

# API endpoints
LOGIN_URL = "http://127.0.0.1:5000/login"
API_URL = "http://127.0.0.1:5000/query"

def login(username: str, password: str):
    try:
        login_payload = {"username": username, "password": password}
        response = requests.post(LOGIN_URL, json=login_payload)

        if response.status_code == 200:
            token = response.json().get('access_token')
            return {"access_token": token} 
        else:
            return {"error": f"Login failed: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def ask_question(question: str, token: str):
    try:
        payload = {"question": question}
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(API_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API responded with status code {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Credentials
    username = "admin"
    password = "password"

    print("Logging in...")
    token_response = login(username, password)

    if "access_token" in token_response: 
        print("!!Successfully Logged In!!")
        token = token_response["access_token"]

        question1 = "Who is president of india?"
        question2 = "Which vendor is associated with invoice 123?"

        print("Question 1:", question1)
        response1 = ask_question(question1, token)
        print("Response 1:", response1)

        print("\nQuestion 2:", question2)
        response2 = ask_question(question2, token)
        print("Response 2:", response2)
    else:
        print("Error:", token_response["error"])
