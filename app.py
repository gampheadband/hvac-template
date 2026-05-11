from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Pull the key from Render Environment Variables
key = os.environ.get("GEMINI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Check if key exists
        if not key:
            return jsonify({"reply": "System Error: API Key is missing in Render settings."}), 500
            
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-pro')
        
        data = request.json
        user_message = data.get("message", "")
        
        # Dispatcher instructions
        prompt = f"You are a professional HVAC dispatcher. Assist the customer briefly. User says: {user_message}"
        
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
        
    except Exception as e:
        # This will print the EXACT error to your Render Logs tab
        print(f"BACKEND ERROR: {str(e)}")
        return jsonify({"reply": "The AI is having a momentary glitch. Please try again."}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
