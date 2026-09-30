from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import chromadb
from pypdf import PdfReader
import requests

from .config import settings


def chunk_text(
    text: str,
    chunk_size: int = 900,
    overlap: int = 150,
) -> list[str]:

    text = " ".join(text.split())

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    chunks = []
    start = 0

    while start < len(text):

        end = min(
            start + chunk_size,
            len(text)
        )

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


def extract_text(path: Path) -> str:

    suffix = path.suffix.lower()

    if suffix == ".pdf":

        reader = PdfReader(str(path))

        return "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    if suffix in {".txt", ".md"}:

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    raise ValueError(
        "Unsupported file type. "
        "Upload PDF, TXT, or MD."
    )


class RagStore:

    def __init__(self):

        # Local embedding generator.
        # No external model download is required.
        self.embedding_model = "models/gemini-embedding-001"
        self.client = chromadb.PersistentClient(
            path=settings.chroma_dir
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="week15_documents",
                metadata={
                    "hnsw:space": "cosine"
                },
            )
        )


    def _embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not settings.gemini_api_key:
            raise RuntimeError("GEMINI_API_KEY is missing.")

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-embedding-001:"
        "batchEmbedContents"
    )

    payload = {
        "requests": [
            {
                "model": self.embedding_model,
                "content": {
                    "parts": [
                        {"text": text}
                    ]
                },
                "outputDimensionality": 384,
            }
            for text in texts
        ]
    }

    response = requests.post(
        url,
        headers={
            "x-goog-api-key": settings.gemini_api_key,
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()
    return [
        item["values"]
        for item in data["embeddings"]
    ]