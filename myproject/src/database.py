import sqlalchemy as db
from pathlib import Path
from pydantic import BaseModel
from typing import Optional

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "papers.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

engine = db.create_engine(f"sqlite:///{DB_PATH}", future=True)
metadata = db.MetaData()

data_base = db.Table(
    "papers",
    metadata,
    db.Column("id", db.Integer, primary_key=True),
    db.Column("name", db.Text, nullable=False),
    db.Column("preview", db.Text, nullable=True),
    db.Column("subject", db.Text, nullable=False),
    db.Column("article", db.Text, nullable=False),
    db.Column("text", db.Text, nullable=False),
    db.Column("note", db.Text, nullable=True),
    db.Column("favorite", db.Boolean, nullable=False),
)

users = db.Table(
    "users",
    metadata,
    db.Column("user_id", db.Integer, primary_key=True),
    db.Column("username", db.Text, nullable=False),
    db.Column("password_hash", db.Text, nullable=False),
)


# todo чтобы фастапи понимал, какие данные приходят из админки


class OLIVEGIK(BaseModel):
    name: str
    preview: Optional[str] = None
    subject: str
    article: str
    text: str
    note: Optional[str] = None
    favorite: bool = False


def init_db() -> None:
    metadata.create_all(engine)
