import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from config import GOOGLE_API_KEY, EMBEDDING_MODEL
from data_loader import crawl_and_chunk

# Initialize Chroma DB client
client = chromadb.Client(Settings(persist_directory="./my_amuse_tech_db"))

# Create or get collection with Gemini embeddings
collection = client.get_or_create_collection(
    name="amuse_tech",
    embedding_function=embedding_functions.GoogleGenerativeAiEmbeddingFunction(
        api_key=GOOGLE_API_KEY,
        model_name=EMBEDDING_MODEL
    )
)
def list_all_documents():
    results = collection.get(include=["documents", "metadatas"])
    for i, doc_text in enumerate(results["documents"]):
        metadata = results["metadatas"][i] if results["metadatas"] else {}
        print(f"Doc #{i} Metadata: {metadata}")
        print(f"Text snippet: {doc_text[:200]}...\n")



def load_site_into_db(seed_url):
    chunks = crawl_and_chunk(seed_url, max_pages=100, max_depth=10)
    ids = [str(i) for i in range(len(chunks))]
    collection.add(
        ids=ids,
        documents=chunks
    )
    print(f"✅ Loaded {len(chunks)} chunks from up to 5 pages starting at {seed_url}")
    list_all_documents()
        
def search_chunks(query, top_k=5):
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    print(results)
    return results["documents"][0]
