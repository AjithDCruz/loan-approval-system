from datetime import datetime
from app.agents import (
    ApplicantProfileAgent,
    FinancialRiskAgent,
    LoanDecisionAgent,
    ComplianceOrchestratorAgent
)

class LoanOrchestrationEngine:
    def __init__(self):
        self.agent1 = ApplicantProfileAgent()
        self.agent2 = FinancialRiskAgent()
        self.agent3 = LoanDecisionAgent()
        self.agent4 = ComplianceOrchestratorAgent()
        self.log = []

    def process(self, app_data):
        try:
            profile = self.agent1.analyze(app_data)
            self.log.append({"step": "profile_analysis", "data": profile, "time": datetime.now().isoformat()})

            financial = self.agent2.analyze(app_data)
            self.log.append({"step": "financial_analysis", "data": financial, "time": datetime.now().isoformat()})

            decision = self.agent3.decide(profile, financial, app_data)
            self.log.append({"step": "loan_decision", "data": decision, "time": datetime.now().isoformat()})

            compliance = self.agent4.orchestrate(decision, app_data, app_data['application_id'])
            self.log.append({"step": "compliance", "data": compliance, "time": datetime.now().isoformat()})

            result = {
                "application_id": app_data['application_id'],
                "decision": decision.get('classification', 'REVIEW'),
                "risk_score": decision.get('risk_score', 0),
                "confidence": decision.get('confidence', 0),
                "explanation": decision.get('explanation', ''),
                "key_factors": decision.get('key_factors', []),
                "case_id": compliance.get('case_id', ''),
                "notification": compliance.get('notification_message', ''),
                "timestamp": datetime.now().isoformat()
            }
            return result
        except Exception as e:
            return {"error": str(e), "application_id": app_data.get('application_id')}
