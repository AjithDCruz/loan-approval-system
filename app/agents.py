from anthropic import Anthropic
import json
from app.config import HAIKU_MODEL, MAX_TOKENS, TEMPERATURE
from app.prompts import (
    APPLICANT_PROFILE_PROMPT,
    FINANCIAL_RISK_PROMPT,
    LOAN_DECISION_PROMPT,
    COMPLIANCE_PROMPT
)

client = Anthropic()

class ApplicantProfileAgent:
    def analyze(self, data):
        prompt = APPLICANT_PROFILE_PROMPT.format(**data)
        response = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            return json.loads(response.content[0].text)
        except:
            return {"income_stability_score": 75, "employment_risk": "Medium", "flags": []}

class FinancialRiskAgent:
    def analyze(self, data):
        dti = (data['liabilities'] + data['loan_amount']) / data['income']
        data['dti'] = round(dti, 2)
        prompt = FINANCIAL_RISK_PROMPT.format(**data)
        response = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            return json.loads(response.content[0].text)
        except:
            return {"dti_risk": "Medium", "credit_risk": "Low", "loan_risk": "Medium", "anomalies": [], "reasoning": "Standard assessment"}

class LoanDecisionAgent:
    def decide(self, profile, financial, data):
        prompt = LOAN_DECISION_PROMPT.format(
            profile_analysis=json.dumps(profile),
            financial_analysis=json.dumps(financial)
        )
        response = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            return json.loads(response.content[0].text)
        except:
            return {"classification": "Review", "risk_score": 55, "confidence": 75, "key_factors": [], "explanation": "Manual review required"}

class ComplianceOrchestratorAgent:
    def orchestrate(self, decision, data, app_id):
        prompt = COMPLIANCE_PROMPT.format(
            classification=decision['classification'],
            risk_score=decision['risk_score'],
            application_id=app_id
        )
        response = client.messages.create(
            model=HAIKU_MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            messages=[{"role": "user", "content": prompt}]
        )
        try:
            return json.loads(response.content[0].text)
        except:
            return {"action_taken": "PROCESSING", "notification_message": "Processing application", "case_id": app_id, "timestamp": "", "compliance_summary": "Application logged"}
