import json
import re
from typing import Any

from services.nvidia_service import call_nvidia_chat
from services.prompt_service import DocumentRequest, build_document_prompt


def generate_document(request: DocumentRequest) -> dict[str, Any]:
    prompt = build_document_prompt(request)
    raw = call_nvidia_chat(prompt)

    if raw:
        parsed = _extract_json(raw)
        if parsed and isinstance(parsed.get("blocks"), list):
            return _normalize_document(parsed, request)

    return _fallback_document(request)


def _extract_json(text: str) -> dict[str, Any] | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return None


def _normalize_document(document: dict[str, Any], request: DocumentRequest) -> dict[str, Any]:
    document.setdefault("title", request.topic.title())
    document.setdefault("theme", request.style)
    document.setdefault("summary", f"A {request.tone} document about {request.topic}.")
    document["blocks"] = document.get("blocks", [])[: max(6, request.pages * 3)]
    return document


def _fallback_document(request: DocumentRequest) -> dict[str, Any]:
    topic_title = request.topic.title()
    labels = ["Discovery", "Adoption", "Optimization", "Scale"]
    multiplier = min(max(request.pages, 1), 10)
    return {
        "title": topic_title,
        "theme": request.style,
        "summary": f"A {request.tone} AI-generated workspace document exploring {request.topic}.",
        "blocks": [
            {
                "type": "hero",
                "eyebrow": f"{request.style.title()} Intelligence Brief",
                "title": topic_title,
                "subtitle": f"A polished {request.pages}-page narrative generated for strategy, communication, and decision support.",
            },
            {
                "type": "paragraph",
                "heading": "Executive Context",
                "content": (
                    f"{topic_title} is becoming a strategic priority as teams look for faster ways to turn research, "
                    "data, and expert judgment into clear operating plans. This document frames the opportunity, "
                    "the practical workflows, and the metrics leaders should monitor."
                ),
            },
            {
                "type": "bullets",
                "heading": "Key Ideas",
                "items": [
                    "Unify scattered knowledge into reusable workspace assets.",
                    "Use AI to draft, structure, and visually refine professional content.",
                    "Combine narrative, charts, and imagery so decisions are easier to scan.",
                    "Preserve review checkpoints for accuracy, compliance, and brand quality.",
                ],
            },
            {
                "type": "stat",
                "label": "Estimated productivity lift",
                "value": f"{24 + multiplier * 3}%",
                "caption": "Modeled impact when research, drafting, and visual formatting happen in one workflow.",
            },
            {
                "type": "chart",
                "heading": "Workspace Maturity Curve",
                "chartType": "bar",
                "labels": labels,
                "data": [22, 41, 64, 82],
            },
            {
                "type": "image",
                "heading": "Suggested Cover Image",
                "prompt": f"Premium editorial cover image for {request.topic}, dark glass workspace, luminous data layers, professional SaaS aesthetic",
            },
            {
                "type": "paragraph",
                "heading": "Recommended Operating Model",
                "content": (
                    "Start with repeatable templates, then add governed AI generation, analytics blocks, export workflows, "
                    "and real-time collaboration. The strongest implementations treat AI as a drafting partner while "
                    "keeping humans in control of claims, tone, and final approval."
                ),
            },
            {
                "type": "summary",
                "heading": "Closing Summary",
                "items": [
                    f"{topic_title} benefits from a workspace that joins writing, design, data, and export.",
                    "Reusable templates keep output consistent while AI accelerates first drafts.",
                    "Dashboards, version history, and collaboration hooks make the platform ready to scale.",
                ],
            },
        ],
    }
