from fastapi import FastAPI, Request, Depends, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

# Определяем базовую директорию, где лежит этот файл (src)
current_dir = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(title="Animal Wiki API")

# Правильная настройка статики и шаблонов через абсолютные пути
app.mount(
    "/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static"
)
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))


# --- ЭНДПОИНТЫ ---


@app.get("/dashboard")
async def home_page(request: Request):
    # Теперь передаем request отдельным аргументом, как требует новая версия Starlette
    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"request": request}
    )


# Поиск статей
@app.get("/api/search")
async def search_animals(q: str = Query(None, min_length=2)):
    # Тут будет логика из database.py
    return {"query": q, "results": []}


# Получение всех статей по категориям
@app.get("/api/articles/{category}")
async def get_category_articles(category: str):
    return {"category": category, "articles": []}


# Получение конкретной статьи
@app.get("/api/article/{article_id}")
async def get_article(article_id: int):
    return {"id": article_id, "title": "Example", "content": "Full text here..."}


# Админка: Добавление новой статьи
@app.post("/api/admin/add")
async def add_article(data: dict):
    return {"status": "added"}


if __name__ == "__main__":
    import uvicorn

    # Запуск сервера
    uvicorn.run(app, host="127.0.0.1", port=8000)
