import numpy as np
import faiss
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer


class HybridRetriever:
    def __init__(self, chunks):
        self.chunks = chunks
        self.tokenized_chunks = [chunk.split() for chunk in chunks]

        # BM25
        self.bm25 = BM25Okapi(self.tokenized_chunks)

        # Embeddings
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.embeddings = self.model.encode(chunks, convert_to_numpy=True)

        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(self.embeddings)

    def retrieve(self, query, top_k=5):
        # BM25 scores
        tokenized_query = query.split()
        bm25_scores = self.bm25.get_scores(tokenized_query)

        # Embedding similarity
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)

        # Combine scores (simple merge)
        candidate_indices = set(indices[0])
        top_bm25 = np.argsort(bm25_scores)[-top_k:]
        candidate_indices.update(top_bm25)

        results = [(i, self.chunks[i]) for i in candidate_indices]

        return results
