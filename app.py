from flask import Flask, render_template, request, jsonify
import google.genai as genai
import os
from dotenv import load_dotenv
import re
from src.helper import format_medical_response, validate_medical_query, extract_disease_keywords
from src.prompt import MEDICAL_SYSTEM_PROMPT, DISEASE_INFORMATION_PROMPT, SYMPTOM_ANALYSIS_PROMPT, GENERAL_MEDICAL_PROMPT

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Set the API key directly if not loaded from .env
if not os.environ.get('GEMINI_API_KEY'):
    os.environ['GEMINI_API_KEY'] = 'AIzaSyBdi4qkUGuEINL1rOtxNADtv3KzSKuFfLA'

# Configure Gemini API
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("⚠️  GEMINI_API_KEY not found in environment variables")
    print("Please set it using: $env:GEMINI_API_KEY='your_api_key_here'")
    print("Or add it to .env file: GEMINI_API_KEY=your_api_key_here")
    exit(1)

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def get_medical_information(query):
    """
    Get comprehensive medical information using Gemini API with web-sourced knowledge
    """
    try:
        # Validate the query first
        is_valid, validation_message = validate_medical_query(query)
        if not is_valid:
            return validation_message
        
        # Extract disease keywords to determine response type
        disease_keywords = extract_disease_keywords(query)
        
        # Choose appropriate prompt based on query type
        if disease_keywords:
            # If specific disease mentioned, use disease information prompt
            primary_disease = disease_keywords[0]
            prompt = DISEASE_INFORMATION_PROMPT.format(disease_name=primary_disease)
        elif any(word in query.lower() for word in ['symptom', 'feel', 'pain', 'hurt', 'ache', 'sick']):
            # If describing symptoms, use symptom analysis prompt
            prompt = SYMPTOM_ANALYSIS_PROMPT.format(symptoms=query)
        else:
            # General medical question
            prompt = GENERAL_MEDICAL_PROMPT.format(question=query)
        
        # Add system context
        full_prompt = f"{MEDICAL_SYSTEM_PROMPT}\n\n{prompt}"
        
        # Generate response using Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=full_prompt
        )
        
        if response and response.text:
            # Format the response for better readability
            formatted_response = format_medical_response(response.text)
            
            # Add medical disclaimer
            disclaimer = "\n\n⚠️ **Medical Disclaimer**: This information is for educational purposes only and should not replace professional medical advice. Always consult with a qualified healthcare provider for diagnosis and treatment."
            
            return formatted_response + disclaimer
        else:
            return "I apologize, but I couldn't generate a response. Please try rephrasing your question or consult a healthcare professional."
            
    except Exception as e:
        print(f"Error getting medical information: {str(e)}")
        return "I apologize, but I'm having trouble accessing medical information right now. Please try again later or consult a healthcare professional."

def is_medical_query(query):
    """
    Check if the query is medical-related
    """
    medical_terms = [
        'disease', 'symptom', 'treatment', 'medicine', 'doctor', 'hospital',
        'pain', 'fever', 'cough', 'headache', 'diabetes', 'blood pressure',
        'infection', 'virus', 'bacteria', 'allergy', 'rash', 'nausea',
        'fatigue', 'dizziness', 'chest pain', 'shortness of breath'
    ]
    
    query_lower = query.lower()
    return any(term in query_lower for term in medical_terms)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    try:
        msg = request.form.get("msg", "").strip()
        print(f"User query: {msg}")
        
        if not msg:
            return "Please ask a medical question."
        
        # Check if it's a medical query
        if not is_medical_query(msg):
            return "I'm a medical information chatbot. Please ask questions related to health, diseases, symptoms, or medical conditions. For example, you can ask about diabetes, fever, headaches, or any health concerns."
        
        # Get medical information using Gemini
        medical_response = get_medical_information(msg)
        
        print(f"Response generated successfully")
        return medical_response
        
    except Exception as e:
        print(f"Error in chat route: {str(e)}")
        return "I apologize, but I'm experiencing technical difficulties. Please try again later or consult a healthcare professional for medical advice."

@app.route("/health")
def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "Medical Chatbot with Gemini API"}

if __name__ == '__main__':
    print("🏥 Starting Medical Chatbot with Gemini API...")
    print("📝 Make sure to add your GEMINI_API_KEY to the .env file")
    print("🌐 Open http://localhost:8080 in your browser")
    print("💡 Ask about any disease or medical condition for comprehensive information")
    app.run(host="0.0.0.0", port=8080, debug=True)