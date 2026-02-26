from flask import Flask, render_template, request
import google.genai as genai
import os
from dotenv import load_dotenv
from src.helper import format_medical_response, validate_medical_query, extract_disease_keywords
from src.prompt import MEDICAL_SYSTEM_PROMPT, DISEASE_INFORMATION_PROMPT, SYMPTOM_ANALYSIS_PROMPT, GENERAL_MEDICAL_PROMPT

app = Flask(__name__)

load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("⚠️  GEMINI_API_KEY not found")
    exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

def get_medical_information(query):
    try:
        is_valid, validation_message = validate_medical_query(query)
        if not is_valid:
            return validation_message
        
        disease_keywords = extract_disease_keywords(query)
        
        if disease_keywords:
            primary_disease = disease_keywords[0]
            prompt = DISEASE_INFORMATION_PROMPT.format(disease_name=primary_disease)
        elif any(word in query.lower() for word in ['symptom', 'feel', 'pain', 'hurt', 'ache', 'sick']):
            prompt = SYMPTOM_ANALYSIS_PROMPT.format(symptoms=query)
        else:
            prompt = GENERAL_MEDICAL_PROMPT.format(question=query)
        
        full_prompt = f"{MEDICAL_SYSTEM_PROMPT}\n\n{prompt}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        
        if response and response.text:
            formatted_response = format_medical_response(response.text)
            disclaimer = "\n\n⚠️ Medical Disclaimer: This information is for educational purposes only. Always consult with a qualified healthcare provider."
            return formatted_response + disclaimer
        else:
            return "I couldn't generate a response. Please try again."
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return "I'm having trouble accessing medical information. Please try again later."

def is_medical_query(query):
    medical_terms = [
        'disease', 'symptom', 'treatment', 'medicine', 'doctor', 'hospital',
        'pain', 'fever', 'cough', 'headache', 'diabetes', 'blood pressure',
        'infection', 'virus', 'bacteria', 'allergy', 'rash', 'nausea',
        'fatigue', 'dizziness', 'chest pain', 'shortness of breath'
    ]
    return any(term in query.lower() for term in medical_terms)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    try:
        msg = request.form.get("msg", "").strip()
        
        if not msg:
            return "Please ask a medical question."
        
        if not is_medical_query(msg):
            return "I'm a medical chatbot. Please ask health-related questions."
        
        return get_medical_information(msg)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Technical difficulties. Please try again."

@app.route("/health")
def health_check():
    return {"status": "healthy", "service": "Medical Chatbot"}

if __name__ == '__main__':
    print("🏥 Medical Chatbot Starting...")
    print("🌐 http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)