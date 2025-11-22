from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize OpenAI only if key exists (prevents crash if key is missing)
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

@app.route('/', methods=['GET', 'POST'])
def handler():
    # 1. Handle Browser Visits (GET)
    if request.method == 'GET':
        if not api_key:
            return "Server is UP, but OpenAI Key is MISSING.", 200
        return "Server is ONLINE. Send a POST request to use.", 200

    # 2. Handle API Requests (POST)
    try:
        data = request.get_json()
        messy_text = data.get('text', '')
        
        if not messy_text:
            return jsonify({"error": "No text provided"}), 400
            
        if not client:
            return jsonify({"error": "Server Misconfigured: No API Key"}), 500

        prompt = f"Extract data from this text and return ONLY valid JSON. No markdown: {messy_text}"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a data cleaning machine. Output only raw JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        return jsonify({"cleaned_data": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# For Vercel
if __name__ == '__main__':
    app.run()
