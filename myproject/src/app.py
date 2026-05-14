from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.templating import Jinja2Templates
import sqlalchemy as db
from fastapi.staticfiles import StaticFiles
import os
from passlib.context import CryptContext
from database import engine, data_base, init_db, users
from schemas import (
    CreatePaper,
    Error,
    PaperResponse,
    UpdatePapers,
    UserLogin,
    UserRegister,
)

# todo Список тегов с описанием для документации
openapi_tags = [
    {"name": "health", "description": "Проверка, что сервер жив"},
    {"name": "students", "description": "Эндпоинты по ученикам"},
    {"name": "teachers", "description": "Эндпоинты по учителям"},
    {"name": "auth", "description": "Регистрация и вход"},
]
app = FastAPI(title="Wiki API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

current_dir = os.path.dirname(os.path.abspath(__file__))

pwd_context = CryptContext(schemes=["bcrypt"])


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# todo при регистрации, превращает пароль в хэш.


#  Функция для проверки
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


init_db()

app.mount(
    "/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static"
)
templates = Jinja2Templates(directory=os.path.join(current_dir, "templates"))


# --- ЭНДПОИНТЫ ---


@app.get("/dashboard")
async def home_page(request: Request):

    with engine.begin() as conn:
        result = conn.execute(db.select(data_base)).mappings().all()

    return templates.TemplateResponse(
        request=request, name="dashboard.html", context={"articles": result}
    )


# POISKOVIK
@app.get("/api/search")
async def search(q: str = Query(None, min_length=2)):
    with engine.begin() as conn:
        stmt = db.select(data_base).where(
            db.or_(data_base.c.name.icontains(q), data_base.c.text.icontains(q))
        )
        results = conn.execute(stmt).mappings().all()
        return {"query": q, "results": results}


# VSE STATIY
@app.get("/api/articles/{category}")
async def get_category_articles(category: str):
    with engine.begin() as conn:
        stmt = db.select(data_base).where(data_base.c.subject == category)
        articles = conn.execute(stmt).mappings().all()
        return {"category": category, "articles": articles}


# JSON STATYA
@app.get("/api/article/{article_id}")
async def get_article(article_id: int):
    with engine.begin() as conn:
        stmt = db.select(data_base).where(data_base.c.id == article_id)
        result = conn.execute(stmt).mappings().fetchone()
        return result


# ааадминочка исправоенная
@app.post("/api/admin/add", response_model=None)
async def add_article(data: UpdatePapers):
    with engine.begin() as conn:
        exists = conn.execute(
            db.select(data_base.c.id).where(data_base.c.id == data.id)
        ).fetchone()

        conn.execute(db.insert(data_base), [data.model_dump()])
        return data, {"status": "added"}


#  ВТОРАЯ СТРАНИЦА
@app.get("/article/{article_id}")
async def article_page(request: Request, article_id: int):
    with engine.begin() as conn:
        stmt = db.select(data_base).where(data_base.c.id == article_id)
        result = conn.execute(stmt).mappings().fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Статья не найдена")

    return templates.TemplateResponse(
        request=request, name="article_detail.html", context={"article": result}
    )


@app.post("/register", tags=["auth"], status_code=201)
def register(payload: UserRegister):

    with engine.begin() as conn:

        # Проверяем - вдруг пользователь с таким именем уже есть?

        exists = conn.execute(
            db.select(users.c.user_id).where(users.c.username == payload.username)
        ).fetchone()

        if exists:
            raise HTTPException(status_code=409, detail="username already taken")
        hashed = pwd_context.hash(payload.password)
        conn.execute(
            db.insert(users),
            [{"username": payload.username, "password_hash": hashed}],
        )

        return {"message": "registered successfully"}


@app.post("/login", tags=["auth"])
def login(payload: UserLogin):
    with engine.begin() as conn:

        # Ищем пользователя по username

        row = conn.execute(
            db.select(users).where(users.c.username == payload.username)
        ).fetchone()

        # Если пользователь не найден ИЛИ пароль неверный - ошибка 401

        if row is None or not pwd_context.verify(
            payload.password, row._mapping["password_hash"]
        ):
            raise HTTPException(status_code=401, detail="invalid username or password")
        return {"message": "login successful", "username": payload.username}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
