import faiss
import numpy as np

class FAISSStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(512)  # Assuming 512 dimensions

    def add(self, embeddings):
        self.index.add(np.array(embeddings))

    def query(self, query_embedding, top_k=5):
        distances, indices = self.index.search(np.array([query_embedding]), top_k)
        return indices
