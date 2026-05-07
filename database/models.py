from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class Document:
    id: str
    user_id: str | None
    title: str
    theme: str
    created_at: datetime | None = None


@dataclass
class DocumentBlock:
    id: str
    document_id: str
    block_type: str
    content: dict[str, Any]
    position: int


@dataclass
class ExportRecord:
    id: str
    document_id: str
    export_type: str
    file_url: str
