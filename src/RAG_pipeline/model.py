from sentence_transformers import SentenceTransformer
import torch
from openai import OpenAI
from dotenv import load_dotenv
import os


class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(model_name, device=self.device)
        self.dim = self.model.get_sentence_embedding_dimension()


    def encode(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)



class Generator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_base = os.getenv("OPENAI_API_BASE", "https://openrouter.ai/api/v1")

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is missing. Check your .env file.")

        self.client = OpenAI(
            base_url=self.api_base,
            api_key=self.api_key
        )

    def generate(self, user_message: str) -> str:
        """
        Send a user query to the FloodSync chatbot and return the model's response.
        """
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return completion.choices[0].message.content