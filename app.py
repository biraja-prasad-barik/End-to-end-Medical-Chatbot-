from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from src.prompt import *
import os

# Import HuggingFace LLM
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

# LangChain ki zaroori cheezein
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate


app = Flask(__name__)

# Sirf .env file load karo
load_dotenv()

# BADLAAV #2: Sirf zaroori API key load karo, extra lines hata do
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')


# --- Ye saara setup ab application ke start hone par ek hi baar hoga ---

print("Embeddings model load ho raha hai...")
embeddings = download_hugging_face_embeddings()

index_name = "medicalbot"

print("Pinecone se connect ho raha hai...")
# Pinecone se existing index ko load karna
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

# Retriever banana
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Prompt template banana
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Use HuggingFace Endpoint instead of local model for better reliability
print("HuggingFace LLM load ho raha hai...")
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint

# Get HuggingFace token from environment
HUGGINGFACEHUB_API_TOKEN = os.environ.get('HUGGINGFACEHUB_API_TOKEN')

if not HUGGINGFACEHUB_API_TOKEN:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in environment variables!")

repo_id = "mistralai/Mistral-7B-Instruct-v0.2"

llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
    temperature=0.7,
    max_new_tokens=512
)
print("HuggingFace LLM successfully load ho gaya hai!")

# Final RAG chain banana
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


# --- Flask Routes ---

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
        
        # Invoke the RAG chain
        response = rag_chain.invoke({"input": msg})
        answer = response.get("answer", "I couldn't generate a response.")
        
        print(f"Response: {answer}")
        return str(answer)
        
    except Exception as e:
        print(f"Error in chat route: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)