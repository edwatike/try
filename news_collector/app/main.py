from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .rss_parser import parse_rss
from .translator import translate_article
from .database import init_db, save_article, get_articles, get_article_by_id
import asyncio

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    articles = get_articles()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})

@app.get("/article/{article_id}", response_class=HTMLResponse)
async def read_article(request: Request, article_id: int):
    article = get_article_by_id(article_id)
    return templates.TemplateResponse("article.html", {"request": request, "article": article})

@app.get("/api/articles")
async def api_articles():
    return get_articles()

async def update_news():
    articles = parse_rss()
    for article in articles:
        translated = translate_article(article)
        save_article(translated)

if __name__ == "__main__":
    asyncio.run(update_news())
