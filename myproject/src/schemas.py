from pydantic import BaseModel
from typing import Optional


class Papers:

    id: int
    name: str
    preview: str
    article: str
    text: str
    note: str
    favorite: bool


class UpdatePapers:

    name: Optional[str] = None
    preview: Optional[str] = None
    article: Optional[str] = None
    text: Optional[str] = None
    note: Optional[str] = None
    favorite: Optional[bool] = None


class Error(BaseModel):
    detail: str
