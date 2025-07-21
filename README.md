# WSB Sentiment API

A FastAPI-based web service for extracting stock ticker mentions from Reddit's r/wallstreetbets posts and comments. It uses asyncpraw for Reddit API access and provides endpoints for sentiment analysis and ticker extraction.

## Features
- Fetch latest posts and comments from r/wallstreetbets
- Extract and filter valid stock tickers from text
- Custom ticker list and blacklist support
- Dockerized for easy deployment

## Requirements
- Python 3.11+
- Reddit API credentials (client_id, client_secret, user_agent)

## Setup

### 1. Clone the repository
```powershell
git clone https://github.com/DarrenDV/wsb-sentiment-api.git
cd wsb-sentiment-api
```

### 2. Install dependencies
```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the project root with your Reddit API credentials:
```
API_CLIENT=your_client_id
API_SECRET=your_client_secret
USER_AGENT=your_user_agent
```

### 4. Run the API
```powershell
uvicorn main:app --host 0.0.0.0 --port 8000
```

Or use Docker:
```powershell
docker build -t wsb-sentiment-api .
docker run -p 8000:8000 --env-file .env wsb-sentiment-api
```

## API Endpoints
- `GET /` — Welcome message
- `GET /getwsbposts` — Latest r/wallstreetbets posts with tickers
- `GET /getwsbcomments` — Latest r/wallstreetbets comments with tickers
- `GET /checkstringfortickers?body=your_text` — Extract tickers from a string

## Ticker Data
- `tickers.json`: List of valid tickers
- `blacklist.txt`: Words to exclude from ticker extraction

## Tools
- `tools/tickergen.py`: Generate ticker JSON from CSV
- `tools/tickercombine.py`: Combine multiple ticker JSON files

## License
MIT License

---

Feel free to contribute or open issues for improvements!
