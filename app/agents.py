from anthropic import Anthropic
import json
import sys
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
        try:
            response = client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.content[0].text.strip()
            if text.startswith('{'):
                return json.loads(text)
            else:
                json_start = text.find('{')
                if json_start != -1:
                    return json.loads(text[json_start:])
        except Exception as e:
            print(f"Profile Agent Error: {e}", file=sys.stderr)

        income_stability = 50 + (min(int(data.get('income', 50000)) / 1000, 50))
        return {
            "income_stability_score": min(int(income_stability), 100),
            "employment_risk": "Medium" if data.get('employment') == 'Self-Employed' else "Low",
            "flags": []
        }

class FinancialRiskAgent:
    def analyze(self, data):
        dti = (data['liabilities'] + data['loan_amount']) / data['income']
        data['dti'] = round(dti, 2)
        prompt = FINANCIAL_RISK_PROMPT.format(**data)
        try:
            response = client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.content[0].text.strip()
            if text.startswith('{'):
                return json.loads(text)
            else:
                json_start = text.find('{')
                if json_start != -1:
                    return json.loads(text[json_start:])
        except Exception as e:
            print(f"Financial Agent Error: {e}", file=sys.stderr)

        credit_score = data.get('credit_score', 650)
        dti_value = data['dti']

        dti_risk = "Low" if dti_value < 0.36 else ("Medium" if dti_value < 0.43 else "High")
        credit_risk = "Low" if credit_score >= 700 else ("Medium" if credit_score >= 650 else "High")
        loan_risk = "Low" if dti_value < 0.30 else ("Medium" if dti_value < 0.50 else "High")

        return {
            "dti_risk": dti_risk,
            "credit_risk": credit_risk,
            "loan_risk": loan_risk,
            "anomalies": [],
            "reasoning": f"DTI: {dti_value}, Credit: {credit_score}"
        }

class LoanDecisionAgent:
    def decide(self, profile, financial, data):
        prompt = LOAN_DECISION_PROMPT.format(
            profile_analysis=json.dumps(profile),
            financial_analysis=json.dumps(financial)
        )
        try:
            response = client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.content[0].text.strip()
            if text.startswith('{'):
                return json.loads(text)
            else:
                json_start = text.find('{')
                if json_start != -1:
                    return json.loads(text[json_start:])
        except Exception as e:
            print(f"Decision Agent Error: {e}", file=sys.stderr)

        credit_score = data.get('credit_score', 650)
        income = data.get('income', 50000)
        dti = (data.get('liabilities', 0) + data.get('loan_amount', 0)) / income

        score_positive = 0
        score_negative = 0
        factors = []

        if credit_score > 700:
            score_positive += 2
            factors.append(f"Good credit score ({credit_score})")
        elif credit_score < 650:
            score_negative += 2
            factors.append(f"Poor credit score ({credit_score})")
        else:
            factors.append(f"Fair credit score ({credit_score})")

        if dti < 0.43:
            score_positive += 2
            factors.append(f"Acceptable DTI ({dti:.2f})")
        else:
            score_negative += 2
            factors.append(f"High DTI ({dti:.2f})")

        if income > 70000:
            score_positive += 1
            factors.append(f"Stable income (${income:,})")
        else:
            factors.append(f"Lower income (${income:,})")

        employment_risk = profile.get('employment_risk', 'Medium')
        if employment_risk == 'Low':
            score_positive += 1
            factors.append("Stable employment")
        elif employment_risk == 'High':
            score_negative += 1
            factors.append("Employment risk")

        if score_negative > score_positive:
            classification = "Reject"
            risk_score = min(80 + (score_negative * 5), 100)
            confidence = 85
        elif score_positive > score_negative + 1:
            classification = "Approve"
            risk_score = max(30 - (score_positive * 5), 0)
            confidence = 85
        else:
            classification = "Review"
            risk_score = 55
            confidence = 70

        return {
            "classification": classification,
            "risk_score": risk_score,
            "confidence": confidence,
            "key_factors": factors[:3],
            "explanation": f"{classification} - {', '.join(factors[:2])}"
        }

class ComplianceOrchestratorAgent:
    def orchestrate(self, decision, data, app_id):
        from datetime import datetime
        prompt = COMPLIANCE_PROMPT.format(
            classification=decision['classification'],
            risk_score=decision['risk_score'],
            application_id=app_id
        )
        try:
            response = client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                messages=[{"role": "user", "content": prompt}]
            )
            text = response.content[0].text.strip()
            if text.startswith('{'):
                return json.loads(text)
            else:
                json_start = text.find('{')
                if json_start != -1:
                    return json.loads(text[json_start:])
        except Exception as e:
            print(f"Compliance Agent Error: {e}", file=sys.stderr)

        classification = decision.get('classification', 'Review')
        action_map = {
            'Approve': 'APPLICATION_APPROVED',
            'Reject': 'APPLICATION_REJECTED',
            'Review': 'REQUIRES_MANUAL_REVIEW'
        }

        return {
            "action_taken": action_map.get(classification, 'PROCESSING'),
            "notification_message": f"Loan application {classification.lower()}ed",
            "case_id": app_id,
            "timestamp": datetime.now().isoformat(),
            "compliance_summary": f"{classification} - Risk Score: {decision.get('risk_score', 0)}"
        }
