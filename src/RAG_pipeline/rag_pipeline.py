from rag_flow import RAG_pipeline
# from rag_evaluator import RAGEvaluator

def main():
    with open("mental_health.txt", "r", encoding="utf-8") as f:
        text = f.read()

    docs = [
        {"id": "doc1", "text": text, "meta": {"title": "Mental Health Overview"}}
    ]

    rag = RAG_pipeline()
    rag.add_documents(docs)

    query = "i am having a depression now"
    result = rag.generate(query, k=2)

    print(result["answer"])

if __name__ == "__main__":
    main()
