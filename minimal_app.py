from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Simple medical knowledge base
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

@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Medical Chatbot</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            .chat-box { height: 400px; border: 1px solid #ddd; padding: 20px; overflow-y: auto; margin-bottom: 20px; background-color: #fafafa; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user-message { background-color: #007bff; color: white; text-align: right; }
            .bot-message { background-color: #e9ecef; color: #333; }
            .input-area { display: flex; gap: 10px; }
            input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background-color: #0056b3; }
            .disclaimer { margin-top: 20px; padding: 15px; background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 Medical Chatbot</h1>
            <div class="chat-box" id="chatBox">
                <div class="message bot-message">
                    Hello! I'm a medical information chatbot. I can provide general information about common health conditions and symptoms. How can I help you today?
                </div>
            </div>
            <div class="input-area">
                <input type="text" id="messageInput" placeholder="Ask about your symptoms or medical condition..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button onclick="sendMessage()">Send</button>
            </div>
            <div class="disclaimer">
                <strong>⚠️ Medical Disclaimer:</strong> This chatbot provides general health information only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with a qualified healthcare provider for medical concerns.
            </div>
        </div>

        <script>
            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (!message) return;

                // Add user message to chat
                addMessage(message, 'user-message');
                input.value = '';

                // Send to server
                fetch('/get', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: 'msg=' + encodeURIComponent(message)
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(data => {
                    if (data && data.trim()) {
                        addMessage(data, 'bot-message');
                    } else {
                        addMessage('I received an empty response. Please try again.', 'bot-message');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    addMessage('Sorry, I encountered an error: ' + error.message + '. Please try again.', 'bot-message');
                });
            }

            function addMessage(message, className) {
                const chatBox = document.getElementById('chatBox');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message ' + className;
                messageDiv.textContent = message;
                chatBox.appendChild(messageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        </script>
    </body>
    </html>
    '''

@app.route("/get", methods=["POST"])
def chat():
    try:
        print(f"Request form data: {request.form}")
        print(f"Request method: {request.method}")
        print(f"Request headers: {dict(request.headers)}")
        
        msg = request.form.get("msg", "")
        print(f"User input: '{msg}'")
        
        if not msg.strip():
            print("Empty message received")
            return "Please ask a medical question."
        
        response = get_medical_response(msg)
        print(f"Response: {response}")
        return response
        
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return "Sorry, I encountered an error. Please try again."

if __name__ == '__main__':
    print("🚀 Starting Medical Chatbot...")
    print("📝 Using simple keyword-based responses")
    print("🌐 Open http://localhost:8080 in your browser")
    app.run(host="0.0.0.0", port=8080, debug=True)