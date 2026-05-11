from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app) # Allows your website to talk to this script

genai.configure(api_key="YOUR_FREE_GEMINI_KEY")
model = genai.GenerativeModel('gemini-pro')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("message")
    
    # Custom instruction to keep the AI focused on HVAC sales
    prompt = (
        "You are a helpful HVAC dispatcher. Be professional and friendly. "
        "Ask for the customer's name, phone number, and service address one by one. "
        "If they provide all info, say 'Perfect! I've sent your details to our technician.'"
        f"\nUser says: {user_input}"
    )
    
    response = model.generate_content(prompt)
    return jsonify({"reply": response.text})

if __name__ == "__main__":
    app.run(debug=True)