from services.nvidia_service import call_nvidia_image


def generate_image(prompt: str, style: str) -> dict:
    generated = call_nvidia_image(prompt, style)
    if generated:
        return {"status": "generated", "image": generated, "provider": "nvidia"}

    encoded_prompt = prompt.replace(" ", "%20")
    return {
        "status": "placeholder",
        "provider": "local-fallback",
        "image": f"https://dummyimage.com/1200x720/101827/ffffff&text={encoded_prompt[:80]}",
        "prompt": prompt,
    }
