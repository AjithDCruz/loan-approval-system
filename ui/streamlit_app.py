import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Agentic AI Loan Approval",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'result' not in st.session_state:
    st.session_state.result = None
if 'app_id' not in st.session_state:
    st.session_state.app_id = None

# Custom CSS for stunning design
custom_css = """
<style>
    * {
        margin: 0;
        padding: 0;
    }

    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        margin-bottom: 40px;
        color: white;
        text-align: center;
        animation: slideDown 0.6s ease-out;
    }

    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .header-title {
        font-size: 52px;
        font-weight: 900;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        letter-spacing: 2px;
    }

    .header-subtitle {
        font-size: 18px;
        color: rgba(255,255,255,0.9);
        font-weight: 300;
        letter-spacing: 1px;
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid rgba(255,255,255,0.2);
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }

    .form-container {
        background: rgba(255,255,255,0.97);
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
        border-left: 6px solid #667eea;
    }

    .form-title {
        font-size: 28px;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }

    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, transparent 100%);
        margin: 30px 0;
        border-radius: 2px;
    }

    .decision-approved {
        background: linear-gradient(135deg, #00d084 0%, #00c872 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        box-shadow: 0 20px 50px rgba(0,208,132,0.4);
        margin-bottom: 30px;
        animation: popIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        letter-spacing: 2px;
    }

    .decision-rejected {
        background: linear-gradient(135deg, #ff6b6b 0%, #ff4757 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        box-shadow: 0 20px 50px rgba(255,71,87,0.4);
        margin-bottom: 30px;
        animation: popIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        letter-spacing: 2px;
    }

    .decision-review {
        background: linear-gradient(135deg, #ffa502 0%, #ff8c00 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        box-shadow: 0 20px 50px rgba(255,165,2,0.4);
        margin-bottom: 30px;
        animation: popIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        letter-spacing: 2px;
    }

    @keyframes popIn {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 18px 50px !important;
        border-radius: 12px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 8px 20px rgba(102,126,234,0.4) !important;
        width: 100% !important;
        height: 60px !important;
        letter-spacing: 1px !important;
    }

    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 30px rgba(102,126,234,0.6) !important;
    }

    .factor-box {
        background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%);
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #667eea;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(255,255,255,0.5);
        padding: 10px;
        border-radius: 15px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 12px 30px;
        font-weight: 700;
        border-radius: 10px;
        font-size: 15px;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }

    .footer {
        text-align: center;
        color: rgba(0,0,0,0.5);
        padding: 30px;
        font-size: 14px;
        margin-top: 50px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Header
HTML_HEADER = """
<div class="header-container">
    <h1 class="header-title">🏦 AGENTIC AI LOAN APPROVAL</h1>
    <p class="header-subtitle">Multi-Agent Intelligent Evaluation with Claude Haiku 4.5</p>
</div>
"""
st.markdown(HTML_HEADER, unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📝 Submit Application", "📊 View Results", "📈 Analytics", "📋 Audit Trail"])

# TAB 1: Submit Application
with tab1:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="form-title">🎯 Loan Application Form</h2>', unsafe_allow_html=True)
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👤 Personal Information")
        age = st.slider("🎂 Age", min_value=18, max_value=100, value=35, help="Applicant age (18-100 years)")
        income = st.number_input("💰 Annual Income ($)", min_value=20000, value=100000, step=5000, help="Total annual household income")
        employment = st.selectbox("💼 Employment Type", ["Salaried", "Self-Employed", "Contract"], help="Current employment status")

    with col2:
        st.markdown("### 📊 Financial Information")
        credit_score = st.slider("📈 Credit Score", min_value=300, max_value=850, value=720, help="Your credit score (300-850)")
        liabilities = st.number_input("💳 Existing Liabilities ($)", min_value=0, value=30000, step=5000, help="Total existing debt/loans")
        location = st.selectbox("📍 Location", ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Miami", "Boston"], help="Application location")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        loan_amount = st.number_input("🏦 Loan Amount ($)", min_value=5000, value=250000, step=10000, help="Requested loan amount")

    with col4:
        tenure = st.slider("⏱️ Loan Tenure (Months)", min_value=12, max_value=360, value=60, step=12, help="Repayment period in months")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Real-time feedback
    st.markdown("### 📊 Application Summary")
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:
        dti = (liabilities + loan_amount) / income if income > 0 else 0
        dti_status = "✅ Good" if dti < 0.43 else "⚠️ High" if dti < 0.50 else "❌ Very High"
        st.metric("Debt-to-Income", f"{dti:.2f}", dti_status)

    with col_f2:
        credit_status = "✅ Excellent" if credit_score >= 750 else "✅ Good" if credit_score >= 700 else "⚠️ Fair" if credit_score >= 650 else "❌ Poor"
        st.metric("Credit Rating", f"{credit_score}", credit_status)

    with col_f3:
        monthly_income = income / 12
        st.metric("Monthly Income", f"${monthly_income:,.0f}", "Monthly")

    with col_f4:
        total_debt = liabilities + loan_amount
        st.metric("Total Obligation", f"${total_debt:,.0f}", "including new loan")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Submit Button
    col_button = st.columns([1, 2, 1])

    with col_button[1]:
        submit_button = st.button("🚀 SUBMIT APPLICATION", use_container_width=True)

    if submit_button:
        with st.spinner("⏳ Processing with Claude Haiku 4.5..."):
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

                # Animated progress
                for i in range(100):
                    time.sleep(0.015)
                    progress_bar.progress(i + 1)

                response = requests.post("http://127.0.0.1:8000/submit", json=payload, timeout=15)

                if response.status_code == 200:
                    result = response.json()
                    st.session_state.result = result['result']
                    st.session_state.app_id = result['application_id']
                    st.session_state.form_submitted = True

                    progress_bar.progress(100)
                    time.sleep(0.5)

                    st.success("✅ Application Processed Successfully!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: View Results
with tab2:
    if st.session_state.result is not None:
        result = st.session_state.result
        decision = result.get('decision', 'UNKNOWN')
        risk_score = result.get('risk_score', 0)
        confidence = result.get('confidence', 0)

        # Decision Display with Color Coding
        if decision == 'Approve':
            st.markdown('<div class="decision-approved">✅ APPROVED</div>', unsafe_allow_html=True)
        elif decision == 'Reject':
            st.markdown('<div class="decision-rejected">❌ REJECTED</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="decision-review">⚠️ REQUIRES REVIEW</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">DECISION</h3>
                <h2 style="margin: 10px 0 0 0; font-size: 36px; color: #00f2fe;">{decision}</h2>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            risk_color = "#00d084" if risk_score < 30 else "#ffa502" if risk_score < 70 else "#ff4757"
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">RISK SCORE</h3>
                <h2 style="margin: 10px 0 0 0; font-size: 36px; color: {risk_color};">{risk_score}/100</h2>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">CONFIDENCE</h3>
                <h2 style="margin: 10px 0 0 0; font-size: 36px; color: #00f2fe;">{confidence}%</h2>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            case_id_short = result.get('case_id', 'N/A')[:12]
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">CASE ID</h3>
                <p style="margin: 10px 0 0 0; font-size: 14px; color: #00f2fe; word-break: break-all;">{case_id_short}...</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Explanation and Factors
        col_exp1, col_exp2 = st.columns([1, 1])

        with col_exp1:
            st.markdown("### 💡 Decision Explanation")
            st.info(result.get("explanation", "No explanation available"))

        with col_exp2:
            st.markdown("### 🎯 Key Decision Factors")
            factors = result.get('key_factors', [])
            if factors:
                for idx, factor in enumerate(factors, 1):
                    st.markdown(f"""
                    <div class="factor-box">
                        <strong>Factor {idx}:</strong> {factor}
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("---")

        # Risk Assessment Gauge
        st.markdown("### 📊 Risk Assessment Gauge")

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Score (0-100)"},
            gauge={
                'axis': {'range': [None, 100], 'tickfont': {'size': 12}},
                'bar': {'color': "#667eea", 'thickness': 0.8},
                'steps': [
                    {'range': [0, 30], 'color': "#00d084"},
                    {'range': [30, 70], 'color': "#ffa502"},
                    {'range': [70, 100], 'color': "#ff4757"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))

        fig.update_layout(height=400, margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#667eea'))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Confidence Distribution
        st.markdown("### 📈 Confidence Level Distribution")

        fig2 = go.Figure(data=[
            go.Bar(
                x=['Confidence Level'],
                y=[confidence],
                marker=dict(
                    color=confidence,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Confidence %", thickness=15, len=0.7)
                ),
                text=[f'{confidence}%'],
                textposition='outside',
                hovertemplate='<b>Confidence:</b> %{y}%<extra></extra>'
            )
        ])

        fig2.update_layout(
            height=350,
            yaxis=dict(range=[0, 100], title="Confidence %"),
            xaxis=dict(title=""),
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#667eea')
        )

        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.warning("⚠️ No Results Yet - Please submit an application first to view results!")

# TAB 3: Analytics Dashboard
with tab3:
    st.markdown("### 📊 Loan Approval Analytics Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">Total Applications</h3>
            <h2 style="margin: 10px 0 0 0; color: #00f2fe; font-size: 32px;">1</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">Approval Rate</h3>
            <h2 style="margin: 10px 0 0 0; color: #00d084; font-size: 32px;">100%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin: 0; font-size: 16px; opacity: 0.9;">Avg Processing Time</h3>
            <h2 style="margin: 10px 0 0 0; color: #00f2fe; font-size: 32px;">2.5s</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("### 🎯 Decision Distribution")

    if st.session_state.result is not None:
        decision_data = {
            'Decision': ['Approved', 'Rejected', 'Under Review'],
            'Count': [1, 0, 0]
        }
        df = pd.DataFrame(decision_data)

        fig = px.pie(df, values='Count', names='Decision',
                    color_discrete_sequence=['#00d084', '#ff4757', '#ffa502'],
                    height=450,
                    hole=0.3)

        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#667eea', size=12),
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.markdown("### 📈 Risk Score Trends")

    if st.session_state.result is not None:
        risk_data = {
            'Application': ['Current'],
            'Risk Score': [st.session_state.result.get('risk_score', 0)]
        }
        df = pd.DataFrame(risk_data)

        fig = px.bar(df, x='Application', y='Risk Score',
                    color='Risk Score',
                    color_continuous_scale='RdYlGn_r',
                    height=400,
                    labels={'Risk Score': 'Risk Score (0-100)'})

        fig.update_layout(
            yaxis=dict(range=[0, 100]),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#667eea'),
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

# TAB 4: Audit Trail
with tab4:
    st.markdown("### 📋 Complete Audit Trail")

    if st.session_state.result is not None:
        result = st.session_state.result

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("#### 📄 Application Details")
            st.json({
                "Application ID": result.get('application_id', 'N/A'),
                "Case ID": result.get('case_id', 'N/A'),
                "Decision": result.get('decision', 'N/A'),
                "Risk Score": result.get('risk_score', 'N/A'),
                "Confidence": result.get('confidence', 'N/A'),
                "Timestamp": result.get('timestamp', 'N/A')
            })

        with col2:
            st.markdown("#### 🤖 Agent Analysis")
            st.json({
                "Explanation": result.get('explanation', 'N/A'),
                "Key Factors": result.get('key_factors', []),
                "Notification": result.get('notification', 'N/A')
            })

        st.markdown("---")

        st.markdown("#### 📊 Full Audit Log (JSON)")
        st.code(json.dumps(result, indent=2), language='json')

    else:
        st.warning("⚠️ No Audit Trail Available - Please submit an application first!")

# Footer
st.markdown("""
<div class="footer">
    <p>🏦 Agentic AI Loan Approval System using Claude Haiku 4.5</p>
    <p>Advanced Multi-Agent Architecture for Intelligent Decision Making</p>
    <p style="font-size: 12px; opacity: 0.6;">© 2026 Loan Approval System - All Rights Reserved</p>
</div>
""", unsafe_allow_html=True)
