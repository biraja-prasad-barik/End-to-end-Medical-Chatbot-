# Medical Chatbot with Gemini API

A Flask-based medical information chatbot that uses Google's Gemini API to provide comprehensive medical information from web sources instead of local medical book data.

## Features

- 🏥 **Comprehensive Medical Information**: Get detailed information about diseases, symptoms, treatments, and prevention
- 🌐 **Web-Based Knowledge**: Uses Gemini API to access current medical information from the web
- 🔍 **Smart Query Processing**: Automatically detects disease names and provides targeted information
- ⚠️ **Medical Disclaimers**: Always includes appropriate medical disclaimers and recommendations to consult healthcare professionals
- 💬 **Interactive Chat Interface**: User-friendly web interface for easy interaction

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Add your Gemini API key to the `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

To get a Gemini API key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and paste it into your `.env` file

### 3. Run the Application
```bash
python app.py
```

### 4. Access the Chatbot
Open your browser and go to: `http://localhost:8080`

## Usage Examples

You can ask about:
- **Specific diseases**: "Tell me about diabetes"
- **Symptoms**: "What causes headaches?"
- **General health**: "How to prevent heart disease?"
- **Medical conditions**: "What is hypertension?"

## Project Structure

```
├── app.py                 # Main Flask application
├── src/
│   ├── helper.py         # Helper functions for formatting and validation
│   ├── prompt.py         # Prompt templates for Gemini API
│   └── __init__.py
├── templates/
│   └── chat.html         # Web interface template
├── static/
│   └── style.css         # Styling for the web interface
├── .env                  # Environment variables (API keys)
├── requirements.txt      # Python dependencies
└── test_gemini_chatbot.py # Test script to verify setup
```

## Testing

Run the test script to verify your setup:
```bash
python test_gemini_chatbot.py
```

## Important Notes

- This chatbot provides general medical information for educational purposes only
- Always consult with qualified healthcare professionals for medical advice
- The information is sourced from Gemini API's web knowledge, not local medical books
- All responses include appropriate medical disclaimers

## API Key Security

- Never commit your API key to version control
- Keep your `.env` file secure and private
- The `.env` file is already added to `.gitignore`