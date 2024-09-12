import os
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key-here")
    HUGGINGFACE_MODEL = os.getenv("HUGGINGFACE_MODEL", "distilbert-base-uncased")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "your-pinecone-key-here")
    PINECONE_INDEX = os.getenv("PINECONE_INDEX", "your-index-name")