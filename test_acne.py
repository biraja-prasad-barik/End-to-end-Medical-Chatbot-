#!/usr/bin/env python3
"""
Test the acne response function directly
"""

# Copy the function from minimal_app.py
MEDICAL_RESPONSES = {
    "diabetes": "Diabetes is a condition where blood sugar levels are too high. Symptoms include increased thirst, frequent urination, and fatigue. Please consult a healthcare provider for proper diagnosis and treatment.",
    "fever": "Fever is a temporary increase in body temperature, often due to infection. Rest, stay hydrated, and consider fever reducers. Seek medical attention if fever is very high or persistent.",
    "headache": "Headaches can be caused by stress, dehydration, or other factors. Try rest, hydration, and pain relievers. Consult a doctor for severe or frequent headaches.",
    "hypertension": "High blood pressure often has no symptoms but can lead to serious health problems. Regular monitoring, healthy diet, exercise, and medication can help manage it.",
    "cold": "Common cold symptoms include runny nose, cough, and sore throat. Rest, fluids, and time usually help. See a doctor if symptoms worsen.",
    "cough": "Cough can be due to cold, allergies, or other conditions. Stay hydrated and avoid irritants. Persistent cough should be evaluated by a healthcare provider.",
    "acne": "Acne is a common skin condition caused by clogged pores. Keep skin clean, avoid touching face, and consider over-the-counter treatments. Severe cases may need dermatologist care.",
    "asthma": "Asthma causes breathing difficulties due to airway inflammation. Use prescribed inhalers, avoid triggers, and have an action plan. Seek immediate help for severe attacks.",
    "allergy": "Allergies occur when immune system reacts to substances. Identify and avoid triggers, use antihistamines if needed, and consult doctor for severe reactions."
}

def get_medical_response(query):
    """Get medical response based on keywords in query"""
    query_lower = query.lower()
    
    # Check for keywords
    for condition, response in MEDICAL_RESPONSES.items():
        if condition in query_lower:
            return f"Regarding {condition}: {response}"
    
    # Check for symptom keywords
    if any(word in query_lower for word in ["pain", "hurt", "ache"]):
        return "For pain management: Rest the affected area, apply ice or heat as appropriate, and consider over-the-counter pain relievers. Consult a healthcare provider for persistent or severe pain."
    
    if any(word in query_lower for word in ["nausea", "vomit", "sick"]):
        return "For nausea: Stay hydrated with small sips of clear fluids, rest, and avoid strong odors. If vomiting persists or you show signs of dehydration, seek medical attention."
    
    if any(word in query_lower for word in ["tired", "fatigue", "exhausted"]):
        return "For fatigue: Ensure adequate sleep, maintain a balanced diet, stay hydrated, and exercise regularly. Persistent fatigue should be evaluated by a healthcare provider."
    
    # Generic response
    return "I understand you have a medical concern. While I can provide general information, it's important to consult with a healthcare professional for proper diagnosis and treatment. Please describe your symptoms more specifically."

# Test different acne queries
test_queries = [
    "what is acne?",
    "What is acne",
    "acne",
    "I have acne",
    "tell me about acne",
    "ACNE"
]

print("Testing acne queries:")
for query in test_queries:
    try:
        response = get_medical_response(query)
        print(f"Query: '{query}' -> Response: {response[:50]}...")
    except Exception as e:
        print(f"Query: '{query}' -> ERROR: {e}")