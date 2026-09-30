from __future__ import annotations

import json

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import settings


LABEL_NAMES = [
    "ACCOUNT",
    "CANCEL",
    "CONTACT",
    "DELIVERY",
    "FEEDBACK",
    "INVOICE",
    "ORDER",
    "PAYMENT",
    "REFUND",
    "SHIPPING",
    "SUBSCRIPTION",
]

FALLBACK_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "router_fallback",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "agent": {"type": "string", "enum": LABEL_NAMES},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            },
            "required": ["agent", "confidence"],
            "additionalProperties": False,
        },
    },
}


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=5),
    reraise=True,
)
def cloud_fallback(message: str) -> dict:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured for the fallback provider.")

    client = OpenAI(api_key=settings.openai_api_key)
    labels = ", ".join(LABEL_NAMES)

    response = client.chat.completions.create(
        model=settings.fallback_openai_model,
        messages=[
            {
                "role": "system",
                "content": "Route the support message to exactly one allowed ShopAssist category.",
            },
            {
                "role": "user",
                "content": f"Allowed categories: {labels}\n\nCustomer message: {message}",
            },
        ],
        temperature=0,
        response_format=FALLBACK_SCHEMA,
    )

    return json.loads(response.choices[0].message.content or "{}")
