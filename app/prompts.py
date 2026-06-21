APPLICANT_PROFILE_PROMPT = "Analyze applicant: Age: {age}, Income: ${income}, Employment: {employment}. Return JSON: income_stability_score (0-100), employment_risk (Low/Med/High), flags (list)"

FINANCIAL_RISK_PROMPT = "Analyze financial risk: Credit Score: {credit_score}, Loan: ${loan_amount}, Liabilities: ${liabilities}, DTI: {dti}. Return JSON: dti_risk, credit_risk, loan_risk, anomalies (list), reasoning"

LOAN_DECISION_PROMPT = "Make loan decision: Profile: {profile_analysis} Financial: {financial_analysis} Rules: CS>700=good, DTI<0.43=good, Income>70=positive. Return JSON: classification (Approve/Reject/Review), risk_score (0-100), confidence (0-100), key_factors (top 3), explanation"

COMPLIANCE_PROMPT = "Generate compliance action: Decision: {classification}, Risk: {risk_score}, AppID: {application_id}. Return JSON: action_taken, notification_message, case_id, timestamp, compliance_summary"
