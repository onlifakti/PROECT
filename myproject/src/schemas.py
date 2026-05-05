from pydantic import BaseModel
from typing import Optional


# для создания новой статьи
class CreatePaper(BaseModel):
    name: str
    preview: Optional[str] = None
    subject: str
    article: str
    text: str
    note: Optional[str] = None
    favorite: bool = False


class PaperResponse(CreatePaper):
    id: int

    class Config:
        from_attributes = True


class UpdatePapers(BaseModel):
    name: Optional[str] = None
    preview: Optional[str] = None
    subject: Optional[str] = None  # Добавил, если захотим сменить тему вкики
    article: Optional[str] = None
    text: Optional[str] = None
    note: Optional[str] = None
    favorite: Optional[bool] = None


class Error(BaseModel):
    detail: str
