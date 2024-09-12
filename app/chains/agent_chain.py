class AgentChain:
    def __init__(self, model, embedding, vector_store):
        self.model = model
        self.embedding = embedding
        self.vector_store = vector_store

    def run(self, input_text):
        # Example: dynamically route input to different model/embedding based on input.
        if len(input_text.split()) > 50:
            result = self.model.call(input_text)
        else:
            embedded_text = self.embedding.embed(input_text)
            best_matches = self.vector_store.query(embedded_text)
            result = self.model.call(best_matches)
        return result
