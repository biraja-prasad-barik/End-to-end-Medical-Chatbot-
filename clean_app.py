from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Medical Chatbot</title></head>
    <body>
        <h1>Medical Chatbot</h1>
        <div id="chat"></div>
        <input type="text" id="input" placeholder="Ask about acne, diabetes, fever...">
        <button onclick="send()">Send</button>
        
        <script>
            function send() {
                const input = document.getElementById('input');
                const message = input.value;
                
                fetch('/get', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    body: 'msg=' + encodeURIComponent(message)
                })
                .then(r => r.text())
                .then(data => {
                    document.getElementById('chat').innerHTML += '<p><b>You:</b> ' + message + '</p>';
                    document.getElementById('chat').innerHTML += '<p><b>Bot:</b> ' + data + '</p>';
                    input.value = '';
                });
            }
        </script>
    </body>
    </html>
    '''

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"].lower()
    
    if "acne" in msg:
        return "Acne is a common skin condition caused by clogged pores. Keep skin clean, avoid touching face, and consider over-the-counter treatments."
    elif "diabetes" in msg:
        return "Diabetes is a condition where blood sugar levels are too high. Symptoms include increased thirst and frequent urination."
    elif "fever" in msg:
        return "Fever is a temporary increase in body temperature, often due to infection. Rest and stay hydrated."
    else:
        return "I can help with questions about acne, diabetes, fever, and other medical conditions."

if __name__ == '__main__':
    print("🚀 Clean Medical Chatbot running on http://localhost:8081")
    app.run(host="0.0.0.0", port=8081, debug=True)