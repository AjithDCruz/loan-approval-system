"""
Manual Review Workflow for Loan Applications
Handles cases requiring manual review by human reviewers
"""

from typing import Optional
from datetime import datetime
from enum import Enum
import uuid


class ReviewStatus(Enum):
    """Status of manual review process"""
    PENDING_REVIEW = "PENDING_REVIEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"


class ReviewTicket:
    """Represents a manual review ticket"""

    def __init__(self, application_id: str, decision_data: dict):
        self.ticket_id = f"REVIEW-{uuid.uuid4().hex[:12].upper()}"
        self.application_id = application_id
        self.created_at = datetime.now()
        self.status = ReviewStatus.PENDING_REVIEW
        self.assigned_to = None
        self.assigned_at = None
        self.decision_data = decision_data
        self.risk_score = decision_data.get("risk_score", 0)
        self.confidence = decision_data.get("confidence", 0)
        self.reviewer_notes = ""
        self.reviewer_decision = None
        self.reviewed_at = None
        self.reason_for_review = self._determine_review_reason()

    def _determine_review_reason(self) -> str:
        """Determine why this case needs manual review"""
        reasons = []

        # Low confidence review
        if self.confidence < 70:
            reasons.append(f"Low decision confidence ({self.confidence}%)")

        # Borderline risk score
        if 40 <= self.risk_score <= 60:
            reasons.append(f"Borderline risk score ({self.risk_score}/100)")

        # Very low confidence on approval/rejection
        if self.confidence < 60:
            reasons.append("Very low confidence in automated decision")

        # Edge case - conflicting signals
        if self.confidence == 70 and 45 <= self.risk_score <= 55:
            reasons.append("Conflicting signals in analysis - manual verification needed")

        return " | ".join(reasons) if reasons else "Review requested"

    def assign_to_reviewer(self, reviewer_id: str) -> dict:
        """Assign ticket to a human reviewer"""
        self.assigned_to = reviewer_id
        self.assigned_at = datetime.now()
        self.status = ReviewStatus.ASSIGNED

        return {
            "ticket_id": self.ticket_id,
            "assigned_to": reviewer_id,
            "assigned_at": self.assigned_at.isoformat(),
            "status": self.status.value
        }

    def start_review(self) -> dict:
        """Mark ticket as being reviewed"""
        self.status = ReviewStatus.IN_PROGRESS

        return {
            "ticket_id": self.ticket_id,
            "status": self.status.value,
            "started_at": datetime.now().isoformat(),
            "application_id": self.application_id,
            "decision_data": self.decision_data,
            "reason": self.reason_for_review
        }

    def complete_review(self, decision: str, notes: str) -> dict:
        """Complete the review with reviewer decision"""
        valid_decisions = ["APPROVED", "REJECTED", "ESCALATED"]

        if decision not in valid_decisions:
            return {"error": f"Invalid decision. Must be one of: {valid_decisions}"}

        self.reviewer_decision = decision
        self.reviewer_notes = notes
        self.reviewed_at = datetime.now()

        if decision == "ESCALATED":
            self.status = ReviewStatus.ESCALATED
        elif decision == "APPROVED":
            self.status = ReviewStatus.APPROVED
        else:
            self.status = ReviewStatus.REJECTED

        return {
            "ticket_id": self.ticket_id,
            "application_id": self.application_id,
            "status": self.status.value,
            "decision": decision,
            "notes": notes,
            "reviewed_at": self.reviewed_at.isoformat()
        }

    def to_dict(self) -> dict:
        """Convert ticket to dictionary"""
        return {
            "ticket_id": self.ticket_id,
            "application_id": self.application_id,
            "created_at": self.created_at.isoformat(),
            "status": self.status.value,
            "assigned_to": self.assigned_to,
            "assigned_at": self.assigned_at.isoformat() if self.assigned_at else None,
            "risk_score": self.risk_score,
            "confidence": self.confidence,
            "reason_for_review": self.reason_for_review,
            "reviewer_notes": self.reviewer_notes,
            "reviewer_decision": self.reviewer_decision,
            "reviewed_at": self.reviewed_at.isoformat() if self.reviewed_at else None
        }


class ManualReviewManager:
    """Manages manual review workflow"""

    def __init__(self):
        self.review_queue = {}
        self.review_history = {}
        self.pending_reviews = []
        self.assigned_reviews = {}

    def create_review_ticket(self, application_id: str, decision_data: dict) -> ReviewTicket:
        """Create a new review ticket for borderline cases"""
        ticket = ReviewTicket(application_id, decision_data)
        self.review_queue[ticket.ticket_id] = ticket
        self.pending_reviews.append(ticket.ticket_id)

        return ticket

    def get_pending_reviews(self) -> list:
        """Get all pending reviews"""
        pending = []
        for ticket_id in self.pending_reviews:
            if ticket_id in self.review_queue:
                ticket = self.review_queue[ticket_id]
                pending.append(ticket.to_dict())
        return pending

    def assign_review(self, ticket_id: str, reviewer_id: str) -> dict:
        """Assign review to a reviewer"""
        if ticket_id not in self.review_queue:
            return {"error": f"Ticket {ticket_id} not found"}

        ticket = self.review_queue[ticket_id]
        result = ticket.assign_to_reviewer(reviewer_id)

        if reviewer_id not in self.assigned_reviews:
            self.assigned_reviews[reviewer_id] = []

        self.assigned_reviews[reviewer_id].append(ticket_id)

        if ticket_id in self.pending_reviews:
            self.pending_reviews.remove(ticket_id)

        return result

    def get_reviewer_queue(self, reviewer_id: str) -> list:
        """Get review queue for a specific reviewer"""
        if reviewer_id not in self.assigned_reviews:
            return []

        queue = []
        for ticket_id in self.assigned_reviews[reviewer_id]:
            if ticket_id in self.review_queue:
                ticket = self.review_queue[ticket_id]
                if ticket.status in [ReviewStatus.ASSIGNED, ReviewStatus.IN_PROGRESS]:
                    queue.append(ticket.to_dict())

        return queue

    def start_review(self, ticket_id: str) -> dict:
        """Start reviewing a ticket"""
        if ticket_id not in self.review_queue:
            return {"error": f"Ticket {ticket_id} not found"}

        ticket = self.review_queue[ticket_id]
        return ticket.start_review()

    def complete_review(self, ticket_id: str, decision: str, notes: str) -> dict:
        """Complete a review"""
        if ticket_id not in self.review_queue:
            return {"error": f"Ticket {ticket_id} not found"}

        ticket = self.review_queue[ticket_id]
        result = ticket.complete_review(decision, notes)

        if "error" not in result:
            self.review_history[ticket_id] = ticket
            self.pending_reviews = [
                t for t in self.pending_reviews if t != ticket_id
            ]

        return result

    def get_ticket(self, ticket_id: str) -> Optional[dict]:
        """Get ticket details"""
        if ticket_id in self.review_queue:
            return self.review_queue[ticket_id].to_dict()
        if ticket_id in self.review_history:
            return self.review_history[ticket_id].to_dict()
        return None

    def get_review_statistics(self) -> dict:
        """Get review workflow statistics"""
        total_pending = len(self.pending_reviews)
        total_assigned = sum(len(v) for v in self.assigned_reviews.values())
        total_completed = len(self.review_history)
        total_tickets = total_pending + total_assigned + total_completed

        completed_approved = sum(
            1 for t in self.review_history.values()
            if t.reviewer_decision == "APPROVED"
        )
        completed_rejected = sum(
            1 for t in self.review_history.values()
            if t.reviewer_decision == "REJECTED"
        )
        completed_escalated = sum(
            1 for t in self.review_history.values()
            if t.reviewer_decision == "ESCALATED"
        )

        return {
            "total_tickets": total_tickets,
            "pending_reviews": total_pending,
            "assigned_reviews": total_assigned,
            "completed_reviews": total_completed,
            "completed_approved": completed_approved,
            "completed_rejected": completed_rejected,
            "completed_escalated": completed_escalated,
            "approval_rate_on_review": (
                completed_approved / total_completed * 100
                if total_completed > 0 else 0
            ),
            "average_confidence_reviewed": (
                sum(t.confidence for t in self.review_history.values()) / total_completed
                if total_completed > 0 else 0
            )
        }


# Singleton instance
review_manager = ManualReviewManager()
