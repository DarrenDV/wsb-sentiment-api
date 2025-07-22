from fastapi import FastAPI
from dotenv import load_dotenv
import asyncpraw
import re
import os
import json

load_dotenv()

TICKERS_JSON_PATH = os.path.join(os.path.dirname(__file__), 'tickers.json')
BLACKLIST_PATH = os.path.join(os.path.dirname(__file__), 'blacklist.txt')
try:
    with open(TICKERS_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        _VALID_TICKERS_CACHE = set(item['ticker'].upper() for item in data if 'ticker' in item)
except Exception:
    _VALID_TICKERS_CACHE = set()

try:
    with open(BLACKLIST_PATH, 'r', encoding='utf-8') as f:
        _BLACKLIST_TICKERS = set(line.strip().upper() for line in f if line.strip() and not line.startswith('#'))
except Exception:
    _BLACKLIST_TICKERS = set()

API_CLIENT = os.getenv("API_CLIENT")
API_SECRET = os.getenv("API_SECRET")
USER_AGENT = os.getenv("USER_AGENT")

reddit = asyncpraw.Reddit(
    client_id=API_CLIENT,
    client_secret=API_SECRET,
    user_agent=USER_AGENT
)

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Reddit PRAW API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/tickers")
async def get_tickers():
    """
    Returns a list of valid stock tickers.
    """
    return {"tickers": list(_VALID_TICKERS_CACHE)}

@app.get("/blacklist")
async def get_blacklist():
    """
    Returns a list of blacklisted stock tickers.
    """
    return {"blacklist": list(_BLACKLIST_TICKERS)}

@app.get("/get-wsb-posts")
async def get_wsb_posts():
    subreddit = await reddit.subreddit("wallstreetbets")
    posts = []
    async for submission in subreddit.new(limit=100):
        tickers = filter_body_for_tickers(submission.title)
        if not tickers:
            continue

        posts.append({
            "title": submission.title,
            "author": str(submission.author),
            "url": submission.url,
            "score": submission.score,
            "created_utc": submission.created_utc,
            "id": submission.id,
            "tickers": tickers,
            "permalink": submission.permalink,
        })

    return {"posts": posts}

@app.get("/get-wsb-comments")
async def get_wsb_comments():
    subreddit = await reddit.subreddit("wallstreetbets")
    comments = []
    async for comment in subreddit.comments(limit=100):
        tickers = filter_body_for_tickers(comment.body)
        if not tickers:
            continue

        comments.append({
            "body": comment.body,
            "author": str(comment.author),
            "score": comment.score,
            "created_utc": comment.created_utc,
            "id": comment.id,
            "link_id": comment.link_id,
            "tickers": tickers,
            "permalink": comment.permalink,
        })
    return {"comments": comments}

@app.get("/check-string-for-tickers")
def check_string_for_tickers(body: str):
    """
    Check the provided string for stock tickers.
    Returns a list of found tickers.
    """
    tickers = filter_body_for_tickers(body)
    return {"tickers": tickers}

def filter_body_for_tickers(body: str):
    dollar_tickers = re.findall(r'\$([A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*)', body)
    caps_tickers = re.findall(r'\b([A-Z0-9]+(?:\.[A-Z0-9]+)*)\b', body)

    def clean_ticker(ticker):
        ticker = ticker.rstrip('.!?;,')
        if re.fullmatch(r'[A-Z0-9]+(?:\.[A-Z0-9]+)*', ticker, re.IGNORECASE):
            return ticker.upper()
        return None

    tickers = set()
    for t in dollar_tickers + caps_tickers:
        cleaned = clean_ticker(t)
        if cleaned:
            tickers.add(cleaned)

    final_tickers = set(tickers)
    for t in tickers:
        for other in tickers:
            if t != other and t in other:
                final_tickers.discard(t)

    return [t for t in final_tickers if t in _VALID_TICKERS_CACHE and t not in _BLACKLIST_TICKERS]
    