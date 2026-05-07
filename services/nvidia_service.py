import os
from typing import Any

import requests


def call_nvidia_chat(prompt: str) -> str | None:
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1").rstrip("/")
    model = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-70b-instruct")
    response = requests.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": "You generate valid JSON for professional document design systems."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 2500,
        },
        timeout=45,
    )
    response.raise_for_status()
    payload: dict[str, Any] = response.json()
    return payload["choices"][0]["message"]["content"]


def call_nvidia_image(prompt: str, style: str) -> str | None:
    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1").rstrip("/")
    model = os.getenv("NVIDIA_IMAGE_MODEL", "stabilityai/stable-diffusion-xl")
    response = requests.post(
        f"{base_url}/images/generations",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "prompt": f"{prompt}. Style: {style}. Premium document design, high resolution.",
            "size": "1024x1024",
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json().get("data", [{}])[0]
    if data.get("url"):
        return data["url"]
    if data.get("b64_json"):
        return f"data:image/png;base64,{data['b64_json']}"
    return None
