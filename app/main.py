from app.api import app as api_app
import uvicorn

if __name__ == "__main__":
    print("Starting Loan Approval API (Claude Haiku 4.5)...")
    print("API running on http://127.0.0.1:8000")
    uvicorn.run(api_app, host="127.0.0.1", port=8000)
