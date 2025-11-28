import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
from langsmith import traceable

from .rag_flow import RAG_pipeline

load_dotenv()


class RAGChatbot:
    def __init__(self, docs=None):
        self.rag = RAG_pipeline()

        if docs:
            self.add_documents(docs)

    def add_documents(self, docs):
        self.rag.add_documents(docs)

    @traceable
    def ask(self, query, k=2):
        response = self.rag.generate(query, k=k)
        return response["answer"]
