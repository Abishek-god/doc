from __future__ import annotations

import uuid
from typing import Any

from database.supabase import get_supabase_client


def save_document(document: dict[str, Any], user_id: str | None = None) -> str:
    document_id = str(uuid.uuid4())
    client = get_supabase_client()
    if not client:
        return document_id

    client.table("documents").insert(
        {
            "id": document_id,
            "user_id": user_id,
            "title": document.get("title", "Untitled document"),
            "theme": document.get("theme", "modern"),
            "summary": document.get("summary", ""),
        }
    ).execute()

    block_rows = []
    for position, block in enumerate(document.get("blocks", [])):
        block_rows.append(
            {
                "document_id": document_id,
                "block_type": block.get("type", "paragraph"),
                "content": block,
                "position": position,
            }
        )

    if block_rows:
        client.table("document_blocks").insert(block_rows).execute()

    return document_id
