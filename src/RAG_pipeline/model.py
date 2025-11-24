from sentence_transformers import SentenceTransformer
import torch
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = SentenceTransformer(model_name, device=self.device)
        self.dim = self.model.get_sentence_embedding_dimension()


    def encode(self, texts):
        return self.model.encode(texts, convert_to_numpy=True)

class Generator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI"),
            base_url="https://openrouter.ai/api/v1"
        )

    def generate(self, user_message: str) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
        return completion.choices[0].message.content
