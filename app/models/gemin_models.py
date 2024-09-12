import openai
from app.config.config import Config

class OpenAIModel:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY

    def call(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
