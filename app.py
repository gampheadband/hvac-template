from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Force the SDK to use the stable v1 API
os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "never"

api_key = os.environ.get("GEMINI_API_KEY")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        if not api_key:
            return jsonify({"reply": "Backend Error: Missing API Key in Render."}), 500
            
        genai.configure(api_key=api_key)
        
        # CHANGED: Using the new 2026 stable workhorse model
        model = genai.GenerativeModel('gemini-3.1-flash-lite')
        
        data = request.json
        user_msg = data.get("message", "")
        
        # Refined dispatcher prompt for better local business leads
        prompt = (
            "You are a professional HVAC dispatcher for a local repair company. "
            "Be brief and helpful. Your goal is to get the customer's name, "
            "phone number, and a brief description of their AC/Heating issue. "
            f"Customer says: {user_msg}"
        )
        
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        # If the model still 404s, it's likely a region or library version issue
        return jsonify({"reply": "The AI is resetting. Try sending one more message!"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
