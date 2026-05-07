from typing import Optional

from pydantic import BaseModel, Field, field_validator


TEMPLATE_LIBRARY = [
    {
        "id": "modern",
        "name": "Modern",
        "accent": "#7c3aed",
        "description": "High-contrast executive documents with bold metrics and glass panels.",
    },
    {
        "id": "corporate",
        "name": "Corporate",
        "accent": "#0ea5e9",
        "description": "Structured board-ready reports with clean hierarchy and conservative visuals.",
    },
    {
        "id": "futuristic",
        "name": "Futuristic",
        "accent": "#22d3ee",
        "description": "Neon strategy decks with cinematic sections and analytics callouts.",
    },
    {
        "id": "minimal",
        "name": "Minimal",
        "accent": "#f8fafc",
        "description": "Quiet editorial pages with generous spacing and focused prose.",
    },
    {
        "id": "startup",
        "name": "Startup",
        "accent": "#fb7185",
        "description": "Pitch-style narratives with traction charts, timelines, and market framing.",
    },
    {
        "id": "academic",
        "name": "Academic",
        "accent": "#a3e635",
        "description": "Research reports with abstracts, evidence blocks, and citation placeholders.",
    },
]


class DocumentRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=160)
    style: str = Field(default="modern", max_length=40)
    pages: int = Field(default=4, ge=1, le=20)
    tone: str = Field(default="professional", max_length=60)
    user_id: Optional[str] = Field(default=None, max_length=128)

    @field_validator("topic", "style", "tone")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


def build_document_prompt(request: DocumentRequest) -> str:
    return f"""
You are an AI document designer for a premium SaaS workspace.
Return valid JSON only. No markdown fences.

Create a visually rich professional document.
Topic: {request.topic}
Theme/style: {request.style}
Tone: {request.tone}
Approximate pages: {request.pages}

Required schema:
{{
  "title": "string",
  "theme": "modern|corporate|futuristic|minimal|startup|academic",
  "summary": "string",
  "blocks": [
    {{"type":"hero","title":"string","subtitle":"string","eyebrow":"string"}},
    {{"type":"paragraph","heading":"string","content":"string"}},
    {{"type":"bullets","heading":"string","items":["string"]}},
    {{"type":"stat","label":"string","value":"string","caption":"string"}},
    {{"type":"chart","heading":"string","chartType":"bar|line|pie","labels":["string"],"data":[number]}},
    {{"type":"image","heading":"string","prompt":"string"}},
    {{"type":"summary","heading":"string","items":["string"]}}
  ]
}}

Include at least one chart, one image prompt, statistics, and an executive summary.
Use concrete, plausible business language. Avoid unsupported real citations.
"""
