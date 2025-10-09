from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from src.prompt import *
import os

# BADLAAV #1: OpenAI ko hata kar LlamaCpp (local model) import karo
from langchain_community.llms import LlamaCpp

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

# BADLAAV #3: Naya Local LLM (LlamaCpp) use karo
print("Local LLM (LlamaCpp) load ho raha hai...")
# Sunishchit karo ki aapka download kiya hua model is path par hai
model_path = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"

llm = LlamaCpp(
    model_path=model_path,
    n_gpu_layers=-1,
    n_batch=512,
    n_ctx=2048,
    f16_kv=True,
    verbose=True,
)
print("Local LLM successfully load ho gaya hai!")

# Final RAG chain banana
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


# --- Flask Routes ---

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(f"User input: {input}")
    response = rag_chain.invoke({"input": msg})
    print(f"Response : {response['answer']}")
    return str(response["answer"])


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)