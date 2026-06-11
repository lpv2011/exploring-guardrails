from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Mapping

import requests


@dataclass(frozen=True)
class OpenRouterConfig:
    api_key: str
    model: str = "openrouter/free"
    site_url: str = "http://localhost"
    app_name: str = "exploring-guardrails"

    @classmethod
    def from_env(cls) -> "OpenRouterConfig":
        key = os.getenv("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("Set OPENROUTER_API_KEY to run live OpenRouter calls.")
        return cls(
            api_key=key,
            model=os.getenv("OPENROUTER_MODEL", "openrouter/free"),
            site_url=os.getenv("OPENROUTER_SITE_URL", "http://localhost"),
            app_name=os.getenv("OPENROUTER_APP_NAME", "exploring-guardrails"),
        )


def chat(messages: List[Mapping[str, str]], config: OpenRouterConfig, temperature: float = 0.0) -> str:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": config.site_url,
            "X-OpenRouter-Title": config.app_name,
        },
        json={"model": config.model, "messages": messages, "temperature": temperature},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["choices"][0]["message"]["content"]
