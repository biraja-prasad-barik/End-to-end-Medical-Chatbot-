#!/usr/bin/env python3
"""
Simple test to check if the chatbot can work without embeddings issues
"""

import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt

def simple_test():
    print("🔄 Loading environment variables...")
    load_dotenv()
    
    # Check if required environment variables exist
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    HUGGINGFACEHUB_API_TOKEN = os.environ.get('HUGGINGFACEHUB_API_TOKEN')
    
    if not PINECONE_API_KEY or not HUGGINGFACEHUB_API_TOKEN:
        print("❌ Missing API keys")
        return False
    
    print("✅ API keys found")
    
    print("\n🔄 Testing LLM directly...")
    try:
        repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN,
            temperature=0.7,
            max_new_tokens=512
        )
        
        # Test direct LLM call
        direct_response = llm.invoke("What is diabetes? Explain in simple terms.")
        print(f"✅ LLM Response: {direct_response[:200]}...")
        
    except Exception as e:
        print(f"❌ LLM Error: {e}")
        return False
    
    print("\n🎉 LLM is working! The issue is likely with embeddings/Pinecone connection.")
    return True

if __name__ == "__main__":
    simple_test()