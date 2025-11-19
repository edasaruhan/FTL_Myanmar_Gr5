from rag_flow import RAG_pipeline

class RAGChatbot:
    def __init__(self, docs=None):
        self.rag = RAG_pipeline()
        
        if docs:
            self.add_documents(docs)

    def add_documents(self, docs):
        self.rag.add_documents(docs)

    def ask(self, query, k=2):
        response = self.rag.generate(query, k=k)
        return response["answer"]

def main():
    with open("mental_health.txt", "r", encoding="utf-8") as f:
        text = f.read()

    docs = [
        {"id": "doc1", "text": text, "meta": {"title": "Mental Health Overview"}}
    ]

    bot = RAGChatbot(docs)

    query = "i am having a depression now"
    answer = bot.ask(query, k=2)

    print(answer)

if __name__ == "__main__":
    main()
