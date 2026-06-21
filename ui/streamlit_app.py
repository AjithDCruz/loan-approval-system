import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Loan Approval System", page_icon="💳", layout="wide")

st.title("Agentic AI Loan Approval System")
st.markdown("Multi-Agent Evaluation with Claude Haiku 4.5")

tab1, tab2, tab3 = st.tabs(["Submit Application", "View Results", "Audit Trail"])

with tab1:
    st.header("Loan Application Form")
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=35)
        income = st.number_input("Annual Income ($)", min_value=20000, value=75000, step=1000)
        employment = st.selectbox("Employment Type", ["Salaried", "Self-Employed", "Contract"])
        liabilities = st.number_input("Existing Liabilities ($)", min_value=0, value=50000, step=1000)

    with col2:
        credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=720)
        loan_amount = st.number_input("Loan Amount ($)", min_value=5000, value=250000, step=1000)
        tenure = st.number_input("Loan Tenure (months)", min_value=12, max_value=360, value=60)
        location = st.selectbox("Location", ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"])

    if st.button("Submit Application", type="primary", use_container_width=True):
        with st.spinner("Processing with Claude Haiku 4.5..."):
            try:
                payload = {
                    "age": age,
                    "income": income,
                    "employment": employment,
                    "credit_score": credit_score,
                    "loan_amount": loan_amount,
                    "tenure_months": tenure,
                    "liabilities": liabilities,
                    "location": location
                }
                response = requests.post("http://127.0.0.1:8000/submit", json=payload, timeout=15)
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.result = result['result']
                    st.session_state.app_id = result['application_id']
                    st.success("Application Processed!")
                    st.rerun()
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab2:
    if "result" in st.session_state:
        result = st.session_state.result

        decision = result.get('decision', 'UNKNOWN')
        if decision == 'Approve':
            st.success(f"✅ APPROVED")
        elif decision == 'Reject':
            st.error(f"❌ REJECTED")
        else:
            st.warning(f"⚠️ REQUIRES REVIEW")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Decision", decision)
        col2.metric("Risk Score", f"{result.get('risk_score', 0)}/100")
        col3.metric("Confidence", f"{result.get('confidence', 0)}%")
        col4.metric("Case ID", result.get('case_id', 'N/A')[:8])

        st.divider()
        st.subheader("Decision Explanation")
        st.write(result.get('explanation', 'No explanation'))

        st.subheader("Key Decision Factors")
        for factor in result.get('key_factors', []):
            st.write(f"- {factor}")
    else:
        st.info("Submit an application first to see results")

with tab3:
    if "result" in st.session_state:
        st.json(st.session_state.result)
    else:
        st.info("Submit an application first to view audit trail")

st.divider()
st.markdown("<div style='text-align:center;color:#666;font-size:11px;'>Agentic AI Loan Approval System using Claude Haiku 4.5</div>", unsafe_allow_html=True)
