import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API Key from the environment
API_KEY = os.getenv("GEMINI_KEY")
model_name = "gemini-1.5-pro-latest"

def get_gemini_recommendation(product_list):
    if not API_KEY:
        print("Error: GEMINI_KEY is not set in the environment.")
        return "Debug: Missing API key."

    # Create a prompt based on the product list for recommendation
    prompt = f"Recommend 3 products based on these: {', '.join(product_list)}"
    print("Prompt:", prompt)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    params = {"key": API_KEY}

    try:
        print("Sending request to Gemini API...")
        response = requests.post(url, headers=headers, json=body, params=params)

        if response.status_code == 200:
            print("Response OK - Status 200")
            try:
                data = response.json()
                print("JSON parsed successfully.")

                # Debugging full response (optional)
                print("Full response:", data)

                candidates = data.get("candidates")
                if candidates and "content" in candidates[0]:
                    text = candidates[0]["content"]["parts"][0]["text"]
                    print("Returning recommendation:", text)
                    return text
                else:
                    print("No 'content' in candidates.")
                    return "No recommendations available at the moment."
            except ValueError:
                print("Error: Failed to parse the JSON response.")
                return "No recommendations available at the moment."
        else:
            print(f"Error: Received a {response.status_code} from the API. {response.text}")
            return "No recommendations available at the moment."
    except requests.exceptions.RequestException as e:
        print(f"Error: A request exception occurred - {e}")
        return "No recommendations available at the moment."

