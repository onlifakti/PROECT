from fastapi import FastAPI, Request, Depends, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security.api_key import APIKeyHeader
import os

app = FastAPI(title="Animal Wiki API")

current_dir = os.path.dirname(os.path.abspath(__file__))
app.mount(
    "/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static"
)
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))

# --- ЭНДПОИНТЫ ---


@app.get("/dashboard")
async def home_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Поиск статей (будет вызываться с сайта в поиске)
@app.get("/api/search")
async def search_animals(q: str = Query(None, min_length=2)):
    # Тут будет логика  из database.py
    return {"query": q, "results": []}


# Получение всех статей по животным
@app.get("/api/articles/{category}")
async def get_category_articles(category: str):
    # Тут будет фильтр по категориям
    return {"category": category, "articles": []}


#  Получение конкретной статьи клик на фронтенде
@app.get("/api/article/{article_id}")
async def get_article(article_id: int):
    # Тут будет возврат текста статьи
    return {"id": article_id, "title": "Example", "content": "Full text here..."}


# Админочкааааааа Добавление новой статьи
@app.post("/api/admin/add")
async def add_article(data: dict):
    return {"status": "added"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
