from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.templating import Jinja2Templates
import sqlalchemy as db
from fastapi.staticfiles import StaticFiles
import os

from database import engine, data_base, init_db
from schemas import UpdatePapers

app = FastAPI(title="Wiki API")

current_dir = os.path.dirname(os.path.abspath(__file__))


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
