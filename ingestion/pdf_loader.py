import pdfplumber
import re
from typing import List


class PDFLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_text(self) -> List[str]:
        pages_text = []

        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    cleaned = self._clean_text(text)
                    pages_text.append(cleaned)

        return pages_text

    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
