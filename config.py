import os
from dotenv import load_dotenv

# Load .env into environment variables
load_dotenv()

# Set API keys
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# Embedding & model names
EMBEDDING_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-2.5-flash"

# Chunking config
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
