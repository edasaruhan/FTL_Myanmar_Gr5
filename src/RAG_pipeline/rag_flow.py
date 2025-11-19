from model import Embedder, Generator
from vector_store import VectorStore
from sklearn.preprocessing import normalize

class RAG_pipeline:
    def __init__(self):
        self.embedder = Embedder()
        self.generator = Generator()
        self.store = VectorStore(self.embedder.dim)
        self.docs = {}

    def add_documents(self, docs):
        ids, texts, metas = [], [], []
        for d in docs:
            ids.append(d["id"])
            texts.append(d["text"])
            metas.append(d.get("meta", {}))
            self.docs[d["id"]] = d["text"]
        emb = self.embedder.encode(texts)
        self.store.add(ids, emb, metas)

    def retrieve(self, query, k=4):
        q_emb = self.embedder.encode([query])[0]
        results = self.store.search(q_emb, k=k)
        return [
            {
                "id": doc_id,
                "score": score,
                "text": self.docs[doc_id],
                "meta": meta,
            }
            for doc_id, score, meta, _ in results
        ]

    def _build_prompt(self, query, passages):
        context = "".join([f"[{p['id']}] {p['text']}" for p in passages])
        return f"Use the retrieved passages to answer the question. You have a medical knowledge about mind. Answer the user question to motivately and user should be motivated after hearing your answer. {context} Question: {query} Answer:"

    def generate(self, query, k=4):
        retrieved = self.retrieve(query, k)
        prompt = self._build_prompt(query, retrieved)
        answer = self.generator.generate(prompt)
        return {"answer": answer, "retrieved": retrieved, "prompt": prompt}