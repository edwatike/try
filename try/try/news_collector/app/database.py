import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "news_db"),
    "user": os.getenv("DB_USER", "news_user"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", "5432")
}

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            summary TEXT,
            full_text TEXT,
            published TEXT,
            link TEXT,
            media TEXT[]
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_article(article):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        INSERT INTO articles (title, summary, full_text, published, link, media)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
    """, (article["title"], article["summary"], article["full_text"],
          article["published"], article["link"], article["media"]))
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result

def get_articles():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM articles ORDER BY published DESC;")
    articles = cur.fetchall()
    conn.close()
    return articles

def get_article_by_id(article_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM articles WHERE id = %s;", (article_id,))
    article = cur.fetchone()
    conn.close()
    return article
