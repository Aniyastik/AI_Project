import chromadb
from sentence_transformers import SentenceTransformer
import uuid

# 🔹 Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 🔹 Persistent Chroma client
client = chromadb.Client(
    settings={"persist_directory": "./chroma_db"}
)

# 🔹 Get or create collection
collection = client.get_or_create_collection(name="rag_db")


# ✅ ADD DOCUMENTS (run once or when updating data)
def add_documents(docs):
    embeddings = model.encode(docs).tolist()

    ids = [str(uuid.uuid4()) for _ in docs]

    collection.add(
        documents=docs,
        embeddings=embeddings,
        ids=ids
    )

    client.persist()


# ✅ QUERY FUNCTION (used in your API)
def query_db(query_text, n_results=3):
    query_embedding = model.encode([query_text]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )

    return results["documents"][0] if results["documents"] else []