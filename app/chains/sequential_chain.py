class SequentialChain:
    def __init__(self, model, embedding, vector_store):
        self.model = model
        self.embedding = embedding
        self.vector_store = vector_store

    def run(self, input_text):
        embedded_text = self.embedding.embed(input_text)
        best_matches = self.vector_store.query(embedded_text)
        result = self.model.call(best_matches)
        return result
