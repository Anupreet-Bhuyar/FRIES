from typing import List


class TextChunker:
    def __init__(self, chunk_size: int = 800, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, pages: List[str]) -> List[str]:
        full_text = " ".join(pages)
        chunks = []

        start = 0
        while start < len(full_text):
            end = start + self.chunk_size
            chunk = full_text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.overlap

        return chunks
