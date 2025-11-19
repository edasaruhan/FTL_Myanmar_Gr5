import numpy as np
from sklearn.preprocessing import normalize

try:
    import faiss
    _HAS_FAISS = True
except:
    _HAS_FAISS = False
    from sklearn.neighbors import NearestNeighbors

class VectorStore:
    def __init__(self, dim):
        self.dim = dim
        self.ids = []
        self.metadatas = []
        self.embeddings = None
        self._index = None
        self._use_faiss = _HAS_FAISS

    def add(self, ids, embeddings, metadatas=None):
        if metadatas is None:
            metadatas = [{}] * len(ids)
        embeddings = normalize(embeddings, axis=1)

        if self.embeddings is None:
            self.embeddings = embeddings.astype("float32")
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings.astype("float32")])

        self.ids.extend(ids)
        self.metadatas.extend(metadatas)
        self._index = None

    def _build_index(self):
        if self._index is not None:
            return
        if self._use_faiss:
            index = faiss.IndexFlatIP(self.dim)
            faiss.normalize_L2(self.embeddings)
            index.add(self.embeddings)
            self._index = index
        else:
            nn = NearestNeighbors(n_neighbors=min(10, len(self.embeddings)), metric="cosine")
            nn.fit(self.embeddings)
            self._index = nn

    def search(self, query_embedding, k=4):
        query_embedding = normalize(query_embedding.reshape(1, -1))[0]
        self._build_index()

        if self._use_faiss:
            qn = query_embedding.reshape(1, -1).astype("float32")
            faiss.normalize_L2(qn)
            D, I = self._index.search(qn, k)

            results = []
            for score, idx in zip(D[0], I[0]):
                if idx < 0:
                    continue
                results.append((self.ids[idx], float(score), self.metadatas[idx], idx))
            return results
        else:
            dist, idxs = self._index.kneighbors([query_embedding], n_neighbors=min(k, len(self.ids)))
            results = []
            for d, idx in zip(dist[0], idxs[0]):
                score = 1 - float(d)
                results.append((self.ids[idx], score, self.metadatas[idx], idx))
            results.sort(key=lambda x: x[1], reverse=True)
            return results
