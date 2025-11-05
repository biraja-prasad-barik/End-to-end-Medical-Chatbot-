from flask import Flask, render_template, jsonify, request
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Simple medical knowledge base (fallback when RAG isn't working)
MEDICAL_KNOWLEDGE = {
    "diabetes": "Diabetes is a condition where your blood sugar levels are too high. Common symptoms include increased thirst, frequent urination, and fatigue. It's important to consult a doctor for proper diagnosis and treatment.",
    "fever": "Fever is a temporary increase in body temperature, often due to an infection. Rest, stay hydrated, and consider over-the-counter fever reducers. Seek medical attention if fever is very high or persistent.",
    "headache": "Headaches can be caused by stress, dehydration, or other factors. Try rest, hydration, and over-the-counter pain relievers. Consult a doctor for severe or frequent headaches.",
    "hypertension": "High blood pressure often has no symptoms but can lead to serious health problems. Regular monitoring, healthy diet, exercise, and medication (if prescribed) can help manage it.",
    "cold": "Common cold symptoms include runny nose, cough, and sore throat. Rest, fluids, and time usually help. See a doctor if symptoms worsen or last more than 10 days.",
    "cough": "Cough can be due to cold, allergies, or other conditions. Stay hydrated, use throat lozenges, and avoid irritants. Persistent cough should be evaluated by a healthcare provider."
}

def get_medical_response(query):
    """Simple keyword-based medical response"""
    query_lower = query.lower()
    
    # Check for keywords in the query
    for condition, response in MEDICAL_KNOWLEDGE.items():
        if condition in query_lower:
            return f"Based on your query about {condition}: {response}"
    
    # Generic medical advice
    return "I understand you have a medical concern. While I can provide general information, it's important to consult with a healthcare professional for proper diagnosis and treatment. Please describe your symptoms more specifically, or consider speaking with a doctor."

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    try:
        msg = request.form["msg"]
        print(f"User input: {msg}")
        
        if not msg.strip():
            return "Please ask a medical question."
        
        # Use simple keyword matching for now
        response = get_medical_response(msg)
        
        print(f"Response: {response}")
        return str(response)
        
    except Exception as e:
        print(f"Error in chat route: {str(e)}")
        return "Sorry, I encountered an error. Please try again."

if __name__ == '__main__':
    print("🚀 Starting Simple Medical Chatbot...")
    print("📝 Note: Using simple keyword matching until RAG is fixed")
    app.run(host="0.0.0.0", port=8080, debug=True)