from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/', methods=['POST'])
def clean_data():
    try:
  # Get the messy text from the user
  data = request.get_json()
  messy_text = data.get('text', '')

  if not messy_text:
return jsonify({"error": "No text provided"}), 400

  # The Instruction to the AI
  prompt = f"Extract data from this text and return ONLY valid JSON. No markdown, no conversational text: {messy_text}"

  # Call OpenAI (Using the cheap, fast 4o-mini model)
  response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[
    {"role": "system", "content": "You are a data cleaning machine. Output only raw JSON."},
    {"role": "user", "content": prompt}
]
  )

  cleaned_data = response.choices[0].message.content
  
  # Return the clean result
  return jsonify({"cleaned_data": cleaned_data})

    except Exception as e:
  return jsonify({"error": str(e)}), 500

# For Vercel serverless
if __name__ == '__main__':
    app.run()
