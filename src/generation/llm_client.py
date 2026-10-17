"""LLM Client for Ollama and local models."""
from __future__ import annotations

import re
import requests
from typing import Optional


class OllamaClient:
    """Client for local Ollama API server."""

    def __init__(
        self,
        model: str = "qwen2.5-coder:7b",
        host: str = "http://localhost:11434",
    ):
        self.model = model
        self.host = host.rstrip("/")

    def is_available(self) -> bool:
        """Check if local Ollama server is running and accessible."""
        try:
            r = requests.get(f"{self.host}/api/tags", timeout=3)
            return r.status_code == 200
        except Exception:
            return False

    def generate(self, prompt: str, timeout: int = 120) -> str:
        """Send prompt to Ollama and return model response."""
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        try:
            r = requests.post(url, json=payload, timeout=timeout)
            r.raise_for_status()
            data = r.json()
            return data.get("response", "")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(
                f"Ollama request failed: {e}. Ensure Ollama is running (`ollama serve`)."
            ) from e


def extract_cobol_code(llm_output: str) -> str:
    """Extract COBOL code block from markdown fences or raw LLM output."""
    match = re.search(r"```(?:cobol)?\s*(.*?)\s*```", llm_output, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    idx = llm_output.upper().find("IDENTIFICATION DIVISION")
    if idx != -1:
        return llm_output[idx:].strip()

    return llm_output.strip()
