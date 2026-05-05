from fastapi import FastAPI, Request, Depends, HTTPException, Query
from fastapi.templating import Jinja2Templates
import sqlalchemy as db
from fastapi.staticfiles import StaticFiles
from fastapi.security.api_key import APIKeyHeader
from database import engine, data_base, init_db
from schemas import Papers, UpdatePapers
import os

app = FastAPI(title="Wiki API")

current_dir = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static"
)
templates = Jinja2Templates(directory="templates")


# --- ЭНДПОИНТЫ ---


@app.get("/dashboard")
async def home_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Поиск статей (будет вызываться с сайта в поиске)
@app.get("/api/search")
async def search(q: str = Query(None, min_length=2)):
    # Тут будет логика  из database.py
    with engine.begin() as conn:
        stmt = db.select(data_base).where()
        return {"query": q, "results": []}


# Получение всех статей
@app.get("/api/articles/{category}")
async def get_category_articles(category: str):
    # Тут будет фильтр по категориям
    with engine.begin() as conn:
        stmt = db.select(data_base).where(data_base.c.subject == category).fetchone()
        return {"category": category, "articles": []}


#  Получение конкретной статьи клик на фронтенде
@app.get("/api/article/{article_id}")
async def get_article(article_id: int):
    # Тут будет возврат текста статьи
    with engine.begin() as conn:
        stmt = (
            db.select(data_base.c.text).where(data_base.c.id == article_id).fetchone()
        )
        return {"id": article_id, "title": "Example", "content": stmt}


# Админочкааааааа Добавление новой статьи
@app.post("/api/admin/add", response_model=None)
async def add_article(data: dict):
    with engine.begin() as conn:
        stmt = exists = conn.execute(
            db.select(data_base.c.id).where(data_base.c.id == data.id)
        ).fetchone()
        conn.execute(db.insert(data_base), [data.model_dump()])
        return data, {"status": "added"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
