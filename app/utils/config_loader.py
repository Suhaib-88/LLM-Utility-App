from utils.helper_functions import load_yaml


def load_component(component_name, component_type):
    if component_type == "model":
        if component_name == "OpenAI":
            from app.models.openai_model import OpenAIModel
            return OpenAIModel()
        elif component_name == "Hugging Face":
            from app.models.hf_model import HuggingFaceModel
            return HuggingFaceModel()
    
    elif component_type == "embedding":
        if component_name == "OpenAI":
            from app.embeddings.openai_embedding import OpenAIEmbedding
            return OpenAIEmbedding()
        elif component_name == "Sentence Transformers":
            from app.embeddings.st_embedding import SentenceTransformerEmbedding
            return SentenceTransformerEmbedding()

    elif component_type == "vector_store":
        if component_name == "FAISS":
            from app.vector_stores.FAISS_store import FAISSStore
            return FAISSStore()
        elif component_name == "Pinecone":
            from app.vector_stores.pinecone_store import PineconeStore
            return PineconeStore()
