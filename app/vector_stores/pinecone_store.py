import pinecone
from app.config.config import Config

class PineconeStore:
    def __init__(self):
        pinecone.init(api_key=Config.PINECONE_API_KEY, environment="us-west1-gcp")
        self.index = pinecone.Index(Config.PINECONE_INDEX)

    def add(self, embeddings, ids):
        vectors = [(str(id), embedding) for id, embedding in zip(ids, embeddings)]
        self.index.upsert(vectors)

    def query(self, query_embedding, top_k=5):
        return self.index.query(query_embedding, top_k=top_k)
