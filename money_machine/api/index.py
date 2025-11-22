from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # 1. BROWSER TEST (The "Is it working?" check)
    if request.method == 'GET':
        key_status = "Found" if os.environ.get("OPENAI_API_KEY") else "MISSING"
        return jsonify({
            "status": "Online",
            "message": "The API is ready. Send a POST request to clean text.",
            "api_key_check": key_status
        })

    # 2. THE REAL TOOL (POST Request)
    try:
        # Check Key
        my_api_key = os.environ.get("OPENAI_API_KEY")
        if not my_api_key:
            return jsonify({"error": "Configuration Error: OPENAI_API_KEY is missing in Vercel Settings"}), 500

        # Connect
        client = OpenAI(api_key=my_api_key)

        # Get Text
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Please send JSON with a 'text' field"}), 400
        
        messy_text = data['text']

        # Run AI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a data cleaning machine. Output only raw JSON."},
                {"role": "user", "content": f"Extract data and return valid JSON: {messy_text}"}
            ]
        )
        
        return jsonify({"cleaned_data": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": f"AI Processing Failed: {str(e)}"}), 500

# Vercel needs this
if __name__ == '__main__':
    app.run()
