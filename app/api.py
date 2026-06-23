from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from app.orchestration import LoanOrchestrationEngine
from app.manual_review import review_manager

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


# Manual Review Endpoints
@app.get("/reviews/pending")
async def get_pending_reviews():
    """Get all pending reviews"""
    return review_manager.get_pending_reviews()


@app.get("/reviews/ticket/{ticket_id}")
async def get_review_ticket(ticket_id: str):
    """Get specific review ticket"""
    ticket = review_manager.get_ticket(ticket_id)
    if not ticket:
        return {"error": "Ticket not found"}
    return ticket


@app.post("/reviews/assign/{ticket_id}")
async def assign_review(ticket_id: str, reviewer_id: str):
    """Assign review ticket to a reviewer"""
    return review_manager.assign_review(ticket_id, reviewer_id)


@app.get("/reviews/queue/{reviewer_id}")
async def get_reviewer_queue(reviewer_id: str):
    """Get review queue for a specific reviewer"""
    return review_manager.get_reviewer_queue(reviewer_id)


@app.post("/reviews/start/{ticket_id}")
async def start_review(ticket_id: str):
    """Start reviewing a ticket"""
    return review_manager.start_review(ticket_id)


class ReviewDecision(BaseModel):
    decision: str
    notes: str


@app.post("/reviews/complete/{ticket_id}")
async def complete_review(ticket_id: str, review_data: ReviewDecision):
    """Complete a review with decision"""
    return review_manager.complete_review(
        ticket_id,
        review_data.decision,
        review_data.notes
    )


@app.get("/reviews/statistics")
async def get_review_statistics():
    """Get manual review workflow statistics"""
    return review_manager.get_review_statistics()
