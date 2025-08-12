import google.generativeai as genai
from config import GOOGLE_API_KEY, CHAT_MODEL
from vector_store import search_chunks

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)

def retrieve_answer(user_query):
    # Get relevant chunks
    retrieved_chunks = search_chunks(user_query)
    context = "\n".join(retrieved_chunks)

    prompt = f"""
    You are a helpful assistant that ONLY answers using the content provided below and previous responses and requests.

    Content:
    {context}

    Question:
    {user_query}
    
    """

    model = genai.GenerativeModel(CHAT_MODEL)
    response = model.generate_content(prompt)
    return response.text
