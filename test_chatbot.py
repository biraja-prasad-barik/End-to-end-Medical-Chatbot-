#!/usr/bin/env python3
"""
Test script to debug the medical chatbot issues
"""

import os
from dotenv import load_dotenv
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt

def test_chatbot():
    print("🔄 Loading environment variables...")
    load_dotenv()
    
    # Check if required environment variables exist
    required_vars = ['PINECONE_API_KEY', 'HUGGINGFACEHUB_API_TOKEN']
    for var in required_vars:
        if not os.environ.get(var):
            print(f"❌ Missing environment variable: {var}")
            return False
        else:
            print(f"✅ Found {var}")
    
    print("\n🔄 Loading embeddings...")
    try:
        embeddings = download_hugging_face_embeddings()
        print("✅ Embeddings loaded successfully")
    except Exception as e:
        print(f"❌ Error loading embeddings: {e}")
        return False
    
    print("\n🔄 Connecting to Pinecone...")
    try:
        index_name = "medicalbot"
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})
        print("✅ Pinecone connection successful")
    except Exception as e:
        print(f"❌ Error connecting to Pinecone: {e}")
        return False
    
    print("\n🔄 Testing document retrieval...")
    try:
        test_docs = retriever.invoke("What is diabetes?")
        print(f"✅ Retrieved {len(test_docs)} documents")
        if test_docs:
            print(f"📄 Sample content: {test_docs[0].page_content[:100]}...")
        else:
            print("⚠️ No documents retrieved - this might be the issue!")
    except Exception as e:
        print(f"❌ Error retrieving documents: {e}")
        return False
    
    print("\n🔄 Loading LLM...")
    try:
        repo_id = "mistralai/Mistral-7B-Instruct-v0.2"
        llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            huggingfacehub_api_token=os.environ.get('HUGGINGFACEHUB_API_TOKEN'),
            temperature=0.7,
            max_new_tokens=512
        )
        print("✅ LLM loaded successfully")
    except Exception as e:
        print(f"❌ Error loading LLM: {e}")
        return False
    
    print("\n🔄 Creating RAG chain...")
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        print("✅ RAG chain created successfully")
    except Exception as e:
        print(f"❌ Error creating RAG chain: {e}")
        return False
    
    print("\n🔄 Testing medical query...")
    try:
        test_queries = [
            "What is diabetes?",
            "What are the symptoms of hypertension?",
            "How to treat fever?"
        ]
        
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            response = rag_chain.invoke({"input": query})
            answer = response.get("answer", "No answer generated")
            print(f"🤖 Answer: {answer[:200]}...")
            
            if not answer or answer.strip() == "":
                print("⚠️ Empty response detected!")
            else:
                print("✅ Response generated successfully")
                
    except Exception as e:
        print(f"❌ Error testing queries: {e}")
        return False
    
    print("\n🎉 All tests completed!")
    return True

if __name__ == "__main__":
    test_chatbot()