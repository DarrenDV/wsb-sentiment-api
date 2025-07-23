# PowerShell script to run FastAPI app on port 8038 for local development
uvicorn main:app --host 127.0.0.1 --port 8038 --reload
