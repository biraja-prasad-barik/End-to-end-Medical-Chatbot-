# Helper functions for medical chatbot

def format_medical_response(response_text):
    """
    Format the medical response for better readability
    """
    # Add line breaks for better formatting
    formatted_text = response_text.replace('. ', '.\n\n')
    
    # Add bullet points for lists
    lines = formatted_text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if line and not line.endswith(':'):
            if any(keyword in line.lower() for keyword in ['symptoms:', 'causes:', 'treatment:', 'prevention:']):
                formatted_lines.append(f"\n**{line}**")
            else:
                formatted_lines.append(line)
        elif line:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def validate_medical_query(query):
    """
    Basic validation for medical queries
    """
    if not query or len(query.strip()) < 2:
        return False, "Please enter a valid medical question."
    
    if len(query) > 500:
        return False, "Please keep your question under 500 characters."
    
    return True, "Valid query"

def extract_disease_keywords(query):
    """
    Extract potential disease or medical condition keywords from query
    """
    medical_keywords = [
        'diabetes', 'hypertension', 'fever', 'headache', 'cough', 'cold',
        'flu', 'asthma', 'allergy', 'acne', 'arthritis', 'migraine',
        'pneumonia', 'bronchitis', 'sinusitis', 'gastritis', 'ulcer',
        'depression', 'anxiety', 'insomnia', 'fatigue', 'nausea',
        'diarrhea', 'constipation', 'heartburn', 'rash', 'eczema'
    ]
    
    query_lower = query.lower()
    found_keywords = [keyword for keyword in medical_keywords if keyword in query_lower]
    
    return found_keywords