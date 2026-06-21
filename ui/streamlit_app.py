import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

custom_css = """
<style>
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 0;
        padding: 0;
    }

    .main {
        padding: 0px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    /* Header styling */
    .header-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px 20px;
        border-radius: 20px;
        margin: 20px auto;
        max-width: 1200px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        color: white;
    }

    .header-title {
        font-size: 44px;
        font-weight: 900;
        margin: 0;
        color: #00f2fe;
        text-align: center;
    }

    .header-subtitle {
        font-size: 16px;
        margin: 10px 0 0 0;
        color: rgba(255,255,255,0.9);
        text-align: center;
    }

    /* Form container */
    .form-section {
        background: white;
        padding: 40px;
        border-radius: 15px;
        margin: 30px auto;
        max-width: 1200px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    }

    .form-title {
        font-size: 28px;
        font-weight: 700;
        margin: 0 0 30px 0;
        color: #333;
        text-align: left;
    }

    .section-header {
        font-size: 18px;
        font-weight: 600;
        color: #667eea;
        margin: 20px 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }

    .input-group {
        margin-bottom: 20px;
        padding: 15px;
        background: #f8f9ff;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }

    /* Results section */
    .results-section {
        max-width: 1200px;
        margin: 20px auto;
        padding: 0 20px;
    }

    .decision-banner-approved {
        background: linear-gradient(135deg, #00d084 0%, #00c872 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(0,208,132,0.3);
    }

    .decision-banner-rejected {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff4757 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(255,71,87,0.3);
    }

    .decision-banner-review {
        background: linear-gradient(135deg, #ffa502 0%, #ff8c00 100%);
        color: white;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 10px 30px rgba(255,165,2,0.3);
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102,126,234,0.2);
        height: 100%;
    }

    .metric-label {
        font-size: 14px;
        color: rgba(255,255,255,0.8);
        margin-bottom: 10px;
    }

    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #00f2fe;
    }

    .explanation-box {
        background: #f0f4ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 20px 0;
        color: #333;
    }

    .factor-box {
        background: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        color: #333;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 10px;
        margin: 20px auto;
        max-width: 1200px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 12px 25px;
        font-weight: 600;
        color: white;
        border-radius: 8px;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(102,126,234,0.8);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 40px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: bold;
        width: 100%;
        height: 50px;
        cursor: pointer;
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.6);
    }

    /* Analytics cards */
    .analytics-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(102,126,234,0.2);
    }

    .analytics-label {
        font-size: 14px;
        color: rgba(255,255,255,0.8);
    }

    .analytics-value {
        font-size: 28px;
        font-weight: bold;
        color: #00f2fe;
        margin-top: 10px;
    }

    /* Content container */
    .content-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Initialize session state
if 'result' not in st.session_state:
    st.session_state.result = None

st.markdown("""
<div class="header-section">
    <h1 class="header-title">🏦 AGENTIC AI LOAN APPROVAL</h1>
    <p class="header-subtitle">Multi-Agent Intelligent Evaluation with Claude Haiku 4.5</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["Submit Application", "View Results", "Analytics", "Audit Trail"])

with tab1:
    st.markdown("""
    <div class="form-section">
    <h2 class="form-title">Loan Application Form</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("### Personal Information")
        age = st.slider("Age", min_value=18, max_value=100, value=35, step=1)
        income = st.number_input("Annual Income (USD)", min_value=20000, value=100000, step=5000)
        employment = st.selectbox("Employment Type", ["Salaried", "Self-Employed", "Contract"])

    with col2:
        st.markdown("### Financial Information")
        credit_score = st.slider("Credit Score", min_value=300, max_value=850, value=720, step=10)
        liabilities = st.number_input("Existing Liabilities (USD)", min_value=0, value=30000, step=5000)
        location = st.selectbox("Location", ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Miami", "Boston"])

    st.divider()

    col3, col4 = st.columns(2, gap="large")

    with col3:
        loan_amount = st.number_input("Loan Amount (USD)", min_value=5000, value=250000, step=10000)

    with col4:
        tenure = st.slider("Loan Tenure (Months)", min_value=12, max_value=360, value=60, step=12)

    st.divider()

    # Calculate and display application summary
    monthly_income = income / 12
    total_debt = liabilities + loan_amount
    dti = total_debt / income if income > 0 else 0

    col_s1, col_s2, col_s3, col_s4 = st.columns(4, gap="small")

    with col_s1:
        st.markdown(f"""
        <div class="analytics-card">
            <div class="analytics-label">DTI Ratio</div>
            <div class="analytics-value">{dti:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_s2:
        st.markdown(f"""
        <div class="analytics-card">
            <div class="analytics-label">Monthly Income</div>
            <div class="analytics-value">${monthly_income:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_s3:
        st.markdown(f"""
        <div class="analytics-card">
            <div class="analytics-label">Total Debt</div>
            <div class="analytics-value">${total_debt:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_s4:
        st.markdown(f"""
        <div class="analytics-card">
            <div class="analytics-label">Credit Rating</div>
            <div class="analytics-value">{credit_score}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

    with col_btn2:
        submit_button = st.button("SUBMIT APPLICATION", use_container_width=True)

    if submit_button:
        with st.spinner("Processing with Claude Haiku 4.5..."):
            progress_bar = st.progress(0)

            try:
                payload = {
                    "age": int(age),
                    "income": float(income),
                    "employment": employment,
                    "credit_score": int(credit_score),
                    "loan_amount": float(loan_amount),
                    "tenure_months": int(tenure),
                    "liabilities": float(liabilities),
                    "location": location
                }

                for i in range(100):
                    time.sleep(0.02)
                    progress_bar.progress(i + 1)

                response = requests.post("http://127.0.0.1:8000/submit", json=payload, timeout=15)

                if response.status_code == 200:
                    result = response.json()
                    st.session_state.result = result['result']
                    st.session_state.app_id = result['application_id']
                    st.success("Application Processed Successfully!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab2:
    if st.session_state.result is not None:
        result = st.session_state.result
        decision = result.get('decision', 'UNKNOWN')
        risk_score = result.get('risk_score', 0)
        confidence = result.get('confidence', 0)

        if decision == 'Approve':
            st.markdown('<div class="decision-banner-approved">✅ APPROVED</div>', unsafe_allow_html=True)
        elif decision == 'Reject':
            st.markdown('<div class="decision-banner-rejected">❌ REJECTED</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="decision-banner-review">⚠️ REQUIRES REVIEW</div>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4, gap="small")

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">DECISION</div>
                <div class="metric-value">{decision}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            risk_color = "#00d084" if risk_score < 30 else "#ffa502" if risk_score < 70 else "#ff4757"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">RISK SCORE</div>
                <div class="metric-value" style="color: {risk_color};">{risk_score}/100</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">CONFIDENCE</div>
                <div class="metric-value">{confidence}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            case_id = result.get('case_id', 'N/A')[:12]
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">CASE ID</div>
                <div class="metric-value" style="font-size: 18px;">{case_id}...</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        col_exp1, col_exp2 = st.columns(2, gap="large")

        with col_exp1:
            st.markdown("### Decision Explanation")
            st.markdown(f"""
            <div class="explanation-box">
                {result.get('explanation', 'No explanation available')}
            </div>
            """, unsafe_allow_html=True)

        with col_exp2:
            st.markdown("### Key Decision Factors")
            factors = result.get('key_factors', [])
            if factors:
                for idx, factor in enumerate(factors, 1):
                    st.markdown(f"""
                    <div class="factor-box">
                        <strong>Factor {idx}:</strong> {factor}
                    </div>
                    """, unsafe_allow_html=True)

        st.divider()

        st.markdown("### Risk Assessment Gauge")
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 30], 'color': "#00d084"},
                    {'range': [30, 70], 'color': "#ffa502"},
                    {'range': [70, 100], 'color': "#ff4757"}
                ]
            }
        ))
        fig.update_layout(height=400, margin=dict(l=10, r=10, t=50, b=10))
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.markdown("### Confidence Distribution")
        fig2 = go.Figure(data=[
            go.Bar(
                x=['Confidence Level'],
                y=[confidence],
                marker=dict(
                    color=confidence,
                    colorscale='Viridis',
                    showscale=True
                ),
                text=[f'{confidence}%'],
                textposition='auto'
            )
        ])
        fig2.update_layout(height=300, yaxis=dict(range=[0, 100]), margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("No application results yet. Please submit an application first!")

with tab3:
    st.markdown("### Loan Approval Analytics Dashboard")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(f"""
        <div class="analytics-card">
            <div class="analytics-label">Total Applications</div>
            <div class="analytics-value">1</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="analytics-card">
            <div class="analytics-label">Approval Rate</div>
            <div class="analytics-value">100%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="analytics-card">
            <div class="analytics-label">Avg Processing Time</div>
            <div class="analytics-value">2.5s</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    if st.session_state.result is not None:
        st.markdown("### Decision Distribution")
        decision_data = {
            'Decision': ['Approved', 'Rejected', 'Under Review'],
            'Count': [1, 0, 0]
        }
        df = pd.DataFrame(decision_data)
        fig = px.pie(df, values='Count', names='Decision',
                    color_discrete_sequence=['#00d084', '#ff4757', '#ffa502'],
                    height=400)
        st.plotly_chart(fig, use_container_width=True)

        st.divider()

        st.markdown("### Risk Score Trends")
        risk_data = {
            'Application': ['Current'],
            'Risk Score': [st.session_state.result.get('risk_score', 0)]
        }
        df = pd.DataFrame(risk_data)
        fig = px.bar(df, x='Application', y='Risk Score',
                    color='Risk Score',
                    color_continuous_scale='RdYlGn_r',
                    height=400)
        st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.markdown("### Complete Audit Trail")

    if st.session_state.result is not None:
        result = st.session_state.result

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown("#### Application Details")
            app_details = {
                "Application ID": result.get('application_id', 'N/A'),
                "Case ID": result.get('case_id', 'N/A'),
                "Decision": result.get('decision', 'N/A'),
                "Risk Score": result.get('risk_score', 'N/A'),
                "Confidence": result.get('confidence', 'N/A'),
                "Timestamp": result.get('timestamp', 'N/A')
            }
            st.json(app_details)

        with col2:
            st.markdown("#### Agent Analysis")
            agent_analysis = {
                "Explanation": result.get('explanation', 'N/A'),
                "Key Factors": result.get('key_factors', []),
                "Notification": result.get('notification', 'N/A')
            }
            st.json(agent_analysis)

        st.divider()

        st.markdown("#### Full Audit Log (JSON)")
        st.code(json.dumps(result, indent=2), language='json')

    else:
        st.warning("No audit trail available. Please submit an application first!")

st.divider()

st.markdown("""
<div style="text-align: center; padding: 30px; color: rgba(255,255,255,0.7); margin-top: 40px;">
    <p style="margin: 0; font-size: 14px;">🏦 Agentic AI Loan Approval System using Claude Haiku 4.5</p>
    <p style="margin: 10px 0 0 0; font-size: 12px;">Advanced Multi-Agent Architecture for Intelligent Decision Making</p>
</div>
""", unsafe_allow_html=True)
