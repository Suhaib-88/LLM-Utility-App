from app.config.config import Config
from langchain_google_genai import ChatGoogleGenerativeAI


def gemini_llm_model(prompt_message):
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    result = llm.invoke(prompt_message)
    return result.content
