from __future__ import annotations

from pathlib import Path

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from .config import settings


class Week14Router:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model_dir = Path(settings.router_model_dir)
        if not model_dir.exists():
            raise FileNotFoundError(f"Week 14 model folder not found: {model_dir}")

        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_dir,
            local_files_only=True,
        )
        self.model.to(self.device)
        self.model.eval()

        raw_id2label = self.model.config.id2label
        self.id2label = {int(k): v for k, v in raw_id2label.items()}

    @torch.inference_mode()
    def predict_batch(self, messages: list[str]) -> list[dict]:
        encoded = self.tokenizer(
            messages,
            padding=True,
            truncation=True,
            max_length=settings.router_max_length,
            return_tensors="pt",
        )
        encoded = {k: v.to(self.device) for k, v in encoded.items()}

        logits = self.model(**encoded).logits
        probabilities = torch.softmax(logits, dim=-1)
        confidence, predicted = probabilities.max(dim=-1)

        results = []
        for idx, conf in zip(predicted.cpu().tolist(), confidence.cpu().tolist()):
            results.append(
                {
                    "agent": self.id2label[int(idx)],
                    "confidence": float(conf),
                    "needs_review": conf < settings.router_confidence_threshold,
                }
            )
        return results
