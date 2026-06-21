APPLICANT_PROFILE_PROMPT = """Analyze this applicant profile and return ONLY valid JSON, no other text:
Age: {age}
Income: ${income}
Employment: {employment}

Return this exact JSON structure (valid JSON only):
{{
  "income_stability_score": <number 0-100>,
  "employment_risk": "<Low or Medium or High>",
  "flags": []
}}"""

FINANCIAL_RISK_PROMPT = """Analyze financial risk and return ONLY valid JSON, no other text:
Credit Score: {credit_score}
Loan Amount: ${loan_amount}
Liabilities: ${liabilities}
DTI: {dti}

Return this exact JSON structure (valid JSON only):
{{
  "dti_risk": "<Low or Medium or High>",
  "credit_risk": "<Low or Medium or High>",
  "loan_risk": "<Low or Medium or High>",
  "anomalies": [],
  "reasoning": "<brief assessment>"
}}"""

LOAN_DECISION_PROMPT = """Make a loan decision based on this analysis. Return ONLY valid JSON:

Profile Analysis:
{profile_analysis}

Financial Analysis:
{financial_analysis}

Decision Rules:
- Credit Score > 700 = good
- DTI < 0.43 = good
- Income > 70000 = positive
- Employment Risk Low = positive
- Any High risk = negative

Return this exact JSON structure (valid JSON only):
{{
  "classification": "<Approve or Reject or Review>",
  "risk_score": <number 0-100>,
  "confidence": <number 0-100>,
  "key_factors": ["factor1", "factor2", "factor3"],
  "explanation": "<why this decision was made>"
}}"""

COMPLIANCE_PROMPT = """Generate compliance record. Return ONLY valid JSON, no other text:
Decision: {classification}
Risk Score: {risk_score}
Application ID: {application_id}

Return this exact JSON structure (valid JSON only):
{{
  "action_taken": "<action description>",
  "notification_message": "<notification text>",
  "case_id": "{application_id}",
  "timestamp": "<current timestamp>",
  "compliance_summary": "<summary>"
}}"""
