from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RAGEvaluator:
    def __init__(self, embedder_model="all-MiniLM-L6-v2"):
        self.eval_embedder = SentenceTransformer(embedder_model)

    def recall_at_k(self, retrieved_ids, ground_truth_ids):
        hits = sum([1 for doc_id in retrieved_ids if doc_id in ground_truth_ids])
        return hits / len(ground_truth_ids)

    def precision_at_k(self, retrieved_ids, ground_truth_ids):
        hits = sum([1 for doc_id in retrieved_ids if doc_id in ground_truth_ids])
        return hits / len(retrieved_ids)

    def mrr(self, retrieved_ids, ground_truth_ids):
        for rank, doc_id in enumerate(retrieved_ids, start=1):
            if doc_id in ground_truth_ids:
                return 1 / rank
        return 0.0

    def answer_similarity(self, predicted, reference):
        emb_pred = self.eval_embedder.encode([predicted])
        emb_ref = self.eval_embedder.encode([reference])
        sim = cosine_similarity(emb_pred, emb_ref)[0][0]
        return float(sim)

    def groundedness(self, answer, retrieved_texts):
        answer_emb = self.eval_embedder.encode([answer])
        ctx_emb = self.eval_embedder.encode(retrieved_texts)
        sims = cosine_similarity(answer_emb, ctx_emb)[0]
        return float(np.max(sims))
