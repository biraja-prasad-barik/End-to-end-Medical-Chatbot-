from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# Global variables for RAG components
rag_chain = None
embeddings = None
retriever = None

def initialize_rag():
    """Initialize RAG components with proper error handling"""
    global rag_chain, embeddings, retriever
    
    try:
        print("🔄 Attempting to initialize RAG system...")
        
        # Try to import and initialize embeddings
        from src.helper import download_hugging_face_embeddings
        embeddings = download_hugging_face_embeddings()
        print("✅ Embeddings loaded successfully")
        
        # Try to connect to Pinecone
        from langchain_pinecone import PineconeVectorStore
        index_name = "medicalbot"
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        print("✅ Pinecone connection successful")
        
        # Try to initialize LLM
        from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
        from langchain.chains import create_retrieval_chain
        from langchain.chains.combine_documents import create_stuff_documents_chain
        from langchain_core.prompts import ChatPromptTemplate
        from src.prompt import system_prompt
        
        HUGGINGFACEHUB_API_TOKEN = os.environ.get('HUGGINGFACEHUB_API_TOKEN')
        if not HUGGINGFACEHUB_API_TOKEN:
            raise ValueError("HUGGINGFACEHUB_API_TOKEN not found!")
        
        repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
            temperature=0.7,
            max_new_tokens=512
        )
        print("✅ LLM initialized successfully")
        
        # Create RAG chain
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        print("✅ RAG chain created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ RAG initialization failed: {str(e)}")
        return False

# Simple fallback responses
MEDICAL_FALLBACK = {
    "diabetes": "Diabetes is a condition where blood sugar levels are too high. Common symptoms include increased thirst, frequent urination, and fatigue. Please consult a healthcare provider for proper diagnosis and treatment.",
    "fever": "Fever is a temporary increase in body temperature, often due to infection. Rest, stay hydrated, and consider fever reducers. Seek medical attention if fever is very high or persistent.",
    "headache": "Headaches can be caused by stress, dehydration, or other factors. Try rest, hydration, and pain relievers. Consult a doctor for severe or frequent headaches.",
    "hypertension": "High blood pressure often has no symptoms but can lead to serious health problems. Regular monitoring, healthy diet, exercise, and medication can help manage it.",
    "cold": "Common cold symptoms include runny nose, cough, and sore throat. Rest, fluids, and time usually help. See a doctor if symptoms worsen.",
    "cough": "Cough can be due to cold, allergies, or other conditions. Stay hydrated and avoid irritants. Persistent cough should be evaluated by a healthcare provider."
}

def get_fallback_response(query):
    """Provide fallback medical responses when RAG is not available"""
    query_lower = query.lower()
    
    for condition, response in MEDICAL_FALLBACK.items():
        if condition in query_lower:
            return f"Regarding {condition}: {response}"
    
    return "I understand you have a medical concern. While I can provide general information, please consult with a healthcare professional for proper diagnosis and treatment. Could you be more specific about your symptoms?"

# Try to initialize RAG on startup
rag_available = initialize_rag()

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
        
        # Try RAG first, fallback to simple responses
        if rag_available and rag_chain:
            try:
                response = rag_chain.invoke({"input": msg})
                answer = response.get("answer", "")
                if answer and answer.strip():
                    print(f"RAG Response: {answer}")
                    return str(answer)
                else:
                    print("RAG returned empty response, using fallback")
            except Exception as e:
                print(f"RAG error: {str(e)}, using fallback")
        
        # Use fallback response
        fallback_response = get_fallback_response(msg)
        print(f"Fallback Response: {fallback_response}")
        return str(fallback_response)
        
    except Exception as e:
        print(f"Error in chat route: {str(e)}")
        return "Sorry, I encountered an error. Please try again or consult a healthcare professional."

if __name__ == '__main__':
    if rag_available:
        print("🚀 Starting Medical Chatbot with RAG system")
    else:
        print("🚀 Starting Medical Chatbot with fallback responses")
        print("⚠️  RAG system unavailable - using simple keyword matching")
    
    app.run(host="0.0.0.0", port=8080, debug=True)