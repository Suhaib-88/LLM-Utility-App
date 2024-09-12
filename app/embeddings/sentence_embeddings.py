from sentence_transformers import SentenceTransformer

class SentenceTransformerEmbedding:
    def __init__(self):
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def embed(self, text):
        return self.model.encode(text)
