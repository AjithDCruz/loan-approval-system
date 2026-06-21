from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from app.orchestration import LoanOrchestrationEngine

app = FastAPI(title="Loan Approval API (Haiku 4.5)")
engine = LoanOrchestrationEngine()
apps_db = {}

class LoanApplication(BaseModel):
    age: int
    income: float
    employment: str
    credit_score: int
    loan_amount: float
    tenure_months: int
    liabilities: float
    location: str

@app.post("/submit")
async def submit(app_data: LoanApplication):
    app_id = str(uuid.uuid4())
    data = {**app_data.dict(), "application_id": app_id}
    result = engine.process(data)
    apps_db[app_id] = result
    return {"application_id": app_id, "status": "processed", "result": result}

@app.get("/app/{app_id}")
async def get_application(app_id: str):
    return apps_db.get(app_id, {"error": "Application not found"})

@app.get("/apps")
async def list_applications():
    return list(apps_db.values())
