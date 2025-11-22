from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handler():
    # 1. Debugging: Check if browser is visiting (GET request)
    if request.method == 'GET':
        return jsonify({"status": "Online", "message": "Send a POST request to use."})

    # 2. Safety Check: Load Key inside the function
    my_api_key = os.environ.get("OPENAI_API_KEY")
    
    if not my_api_key:
        # This will tell us if Vercel can't find the key
        return jsonify({"error": "Critical: OPENAI_API_KEY is missing in Settings."}), 500

    try:
        # 3. Connect to OpenAI only now
        client = OpenAI(api_key=my_api_key)
        
        # 4. Get Data
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON body"}), 400
            
        messy_text = data.get('text', '')
        if not messy_text:
            return jsonify({"error": "No text provided"}), 400

        # 5. The AI Task
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
        # If OpenAI crashes, print the exact error
        return jsonify({"error": f"OpenAI Error: {str(e)}"}), 500

# Required for Vercel
if __name__ == '__main__':
    app.run()
