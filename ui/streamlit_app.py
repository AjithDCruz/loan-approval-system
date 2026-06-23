import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import time
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Smart Loan Approval",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800;900&display=swap');

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        background: linear-gradient(135deg, #0a0820 0%, #1a1040 25%, #0d1b45 50%, #1a0840 75%, #0a0820 100%);
        font-family: 'Inter', sans-serif;
        color: #ffffff;
        min-height: 100vh;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0820 0%, #1a1040 25%, #0d1b45 50%, #1a0840 75%, #0a0820 100%) !important;
    }

    .main {
        background: linear-gradient(135deg, #0a0820 0%, #1a1040 25%, #0d1b45 50%, #1a0840 75%, #0a0820 100%) !important;
        padding: 0;
    }

    /* TEXT VISIBILITY */
    .stMarkdown, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown h4, .stMarkdown p, .stText {
        color: #ffffff !important;
    }

    .stSlider label, .stNumberInput label, .stSelectbox label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    div { color: #ffffff !important; }
    span { color: #ffffff !important; }

    input, select {
        color: #1a1a1a !important;
    }

    /* RADIO AND SELECTBOX STYLING */
    .stRadio label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    .stRadio > div[role="radiogroup"] > label {
        color: #ffffff !important;
    }

    .stSelectbox > div > div > select {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    .stSelectbox > div > div {
        background-color: #1a1a1a !important;
    }

    /* Selectbox options styling */
    select option {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* HEADER - PREMIUM GLASS */
    .header-premium {
        background: rgba(79, 172, 254, 0.08);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 2px solid rgba(79, 172, 254, 0.2);
        padding: 60px 50px;
        border-radius: 30px;
        margin: 30px auto;
        max-width: 1250px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(79, 172, 254, 0.15),
                    inset 0 1px 1px rgba(255, 255, 255, 0.3),
                    0 0 40px rgba(79, 172, 254, 0.1);
        transform: perspective(1200px) rotateX(-1deg);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        border-radius: 30px;
        position: relative;
        overflow: hidden;
    }

    .header-premium::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 50%, rgba(79, 172, 254, 0.1), transparent);
        pointer-events: none;
    }

    .header-premium:hover {
        box-shadow: 0 30px 80px rgba(79, 172, 254, 0.25),
                    inset 0 1px 1px rgba(255, 255, 255, 0.4),
                    0 0 60px rgba(79, 172, 254, 0.15);
        transform: perspective(1200px) translateY(-5px) rotateX(-1deg);
    }

    .header-title-premium {
        font-size: 52px;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1px;
        text-shadow: 0 0 40px rgba(79, 172, 254, 0.3);
    }

    .header-subtitle-premium {
        font-size: 16px;
        margin: 15px 0 0 0;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* FORM CONTAINER */
    .form-premium {
        background: rgba(79, 172, 254, 0.06);
        backdrop-filter: blur(20px);
        padding: 50px;
        border-radius: 25px;
        margin: 40px auto;
        max-width: 1250px;
        box-shadow: 0 15px 50px rgba(79, 172, 254, 0.12),
                    inset 0 1px 1px rgba(255, 255, 255, 0.2),
                    0 0 30px rgba(79, 172, 254, 0.08);
        border: 1.5px solid rgba(79, 172, 254, 0.15);
        transition: all 0.4s ease;
    }

    .form-premium:hover {
        box-shadow: 0 20px 60px rgba(79, 172, 254, 0.18),
                    inset 0 1px 1px rgba(255, 255, 255, 0.25),
                    0 0 40px rgba(79, 172, 254, 0.12);
    }

    .form-title-premium {
        font-size: 36px;
        font-weight: 800;
        margin: 0 0 35px 0;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.5px;
    }

    .section-header-premium {
        font-size: 18px;
        font-weight: 700;
        margin: 30px 0 20px 0;
        color: #4facfe !important;
        padding-bottom: 12px;
        border-bottom: 3px solid;
        border-image: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) 1;
        text-shadow: 0 2px 8px rgba(79, 172, 254, 0.2);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-size: 14px;
    }

    /* INPUT STYLING */
    .stNumberInput input, .stSelectbox select {
        background: rgba(255, 255, 255, 0.92) !important;
        color: #1a1a1a !important;
        border: 2px solid #4facfe !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.1) !important;
    }

    .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #00f2fe !important;
        box-shadow: 0 6px 25px rgba(79, 172, 254, 0.25) !important;
    }

    /* SLIDER STYLING */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%) !important;
    }

    /* METRIC CARDS - PREMIUM */
    .metric-card-premium {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.15) 0%, rgba(0, 242, 254, 0.1) 100%);
        padding: 35px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 50px rgba(79, 172, 254, 0.2),
                    0 0 0 1.5px rgba(79, 172, 254, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
        height: 100%;
        transform: perspective(1000px) rotateY(0deg);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        backdrop-filter: blur(15px);
        border: 1.5px solid rgba(79, 172, 254, 0.2);
        position: relative;
        overflow: hidden;
    }

    .metric-card-premium::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), transparent);
        pointer-events: none;
    }

    .metric-card-premium:hover {
        transform: perspective(1000px) translateZ(25px) rotateY(-5deg);
        box-shadow: 0 25px 70px rgba(79, 172, 254, 0.3),
                    0 0 0 1.5px rgba(0, 242, 254, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.4);
    }

    .metric-label-premium {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.8) !important;
        margin-bottom: 15px;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
    }

    .metric-value-premium {
        font-size: 40px;
        font-weight: 900;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1px;
    }

    /* DECISION BANNERS */
    .decision-approved-premium {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 60px;
        border-radius: 25px;
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        margin: 30px 0;
        box-shadow: 0 20px 60px rgba(17, 153, 142, 0.3),
                    0 0 40px rgba(17, 153, 142, 0.2),
                    inset 0 2px 0 rgba(255, 255, 255, 0.4);
        transform: perspective(1200px) rotateX(-2deg);
        animation: slideInBig 0.6s cubic-bezier(0.23, 1, 0.32, 1);
        letter-spacing: 2px;
    }

    .decision-rejected-premium {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        color: white;
        padding: 60px;
        border-radius: 25px;
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        margin: 30px 0;
        box-shadow: 0 20px 60px rgba(235, 51, 73, 0.3),
                    0 0 40px rgba(235, 51, 73, 0.2),
                    inset 0 2px 0 rgba(255, 255, 255, 0.4);
        transform: perspective(1200px) rotateX(-2deg);
        animation: slideInBig 0.6s cubic-bezier(0.23, 1, 0.32, 1);
        letter-spacing: 2px;
    }

    .decision-review-premium {
        background: linear-gradient(135deg, #f77062 0%, #fe5196 100%);
        color: white;
        padding: 60px;
        border-radius: 25px;
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        margin: 30px 0;
        box-shadow: 0 20px 60px rgba(247, 112, 98, 0.3),
                    0 0 40px rgba(247, 112, 98, 0.2),
                    inset 0 2px 0 rgba(255, 255, 255, 0.4);
        transform: perspective(1200px) rotateX(-2deg);
        animation: slideInBig 0.6s cubic-bezier(0.23, 1, 0.32, 1);
        letter-spacing: 2px;
    }

    @keyframes slideInBig {
        from {
            opacity: 0;
            transform: perspective(1200px) rotateX(10deg) translateY(30px);
        }
        to {
            opacity: 1;
            transform: perspective(1200px) rotateX(-2deg) translateY(0);
        }
    }

    /* EXPLANATION & FACTOR BOXES */
    .explanation-premium {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.12) 0%, rgba(0, 242, 254, 0.08) 100%);
        padding: 28px;
        border-radius: 18px;
        border-left: 5px solid #4facfe;
        margin: 25px 0;
        color: #ffffff !important;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.15);
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
    }

    .explanation-premium:hover {
        box-shadow: 0 12px 35px rgba(79, 172, 254, 0.25);
    }

    .explanation-premium strong {
        color: #ffffff !important;
    }

    .factor-premium {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.05) 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 4px solid #4facfe;
        margin: 15px 0;
        color: #ffffff !important;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.1);
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
        backdrop-filter: blur(10px);
    }

    .factor-premium strong {
        color: #00f2fe !important;
        font-weight: 700;
    }

    .factor-premium:hover {
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.2);
        transform: translateX(8px);
    }

    /* ANALYTICS CARDS */
    .analytics-card-premium {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.15) 0%, rgba(0, 242, 254, 0.1) 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 50px rgba(79, 172, 254, 0.2),
                    0 0 0 1.5px rgba(79, 172, 254, 0.2);
        height: 100%;
        transform: perspective(1000px) rotateY(0deg);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        backdrop-filter: blur(15px);
        border: 1.5px solid rgba(79, 172, 254, 0.2);
    }

    .analytics-card-premium:hover {
        transform: perspective(1000px) translateZ(20px) rotateY(-3deg);
        box-shadow: 0 22px 65px rgba(79, 172, 254, 0.3),
                    0 0 0 1.5px rgba(0, 242, 254, 0.4);
    }

    .analytics-label-premium {
        font-size: 13px;
        color: rgba(255, 255, 255, 0.85) !important;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
    }

    .analytics-value-premium {
        font-size: 36px;
        font-weight: 900;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 12px;
    }

    /* BUTTON STYLING */
    .stButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 50%, #4facfe 100%) !important;
        color: #000 !important;
        border: none !important;
        padding: 18px 50px !important;
        border-radius: 15px !important;
        font-size: 16px !important;
        font-weight: 900 !important;
        width: 100% !important;
        height: 60px !important;
        cursor: pointer !important;
        box-shadow: 0 12px 35px rgba(79, 172, 254, 0.3),
                    0 0 0 1.5px rgba(255, 255, 255, 0.2) !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .stButton > button:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 18px 50px rgba(79, 172, 254, 0.5),
                    0 0 0 1.5px rgba(255, 255, 255, 0.3) !important;
    }

    .stButton > button:active {
        transform: translateY(-2px) !important;
    }

    /* TABS STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(79, 172, 254, 0.08);
        padding: 12px;
        border-radius: 20px;
        margin: 30px auto;
        max-width: 1250px;
        backdrop-filter: blur(15px);
        border: 1.5px solid rgba(79, 172, 254, 0.15);
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.1);
    }

    .stTabs [data-baseweb="tab"] {
        padding: 16px 28px;
        font-weight: 700;
        color: rgba(255, 255, 255, 0.7) !important;
        border-radius: 15px;
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 13px;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: #000 !important;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.4);
        font-weight: 900;
    }

    /* DIVIDER */
    .stDivider {
        border-color: rgba(79, 172, 254, 0.2) !important;
    }

    /* FOOTER */
    .footer-premium {
        text-align: center;
        padding: 50px 20px;
        color: rgba(255, 255, 255, 0.5);
        margin-top: 80px;
        border-top: 1.5px solid rgba(79, 172, 254, 0.15);
    }

    .footer-text {
        font-size: 14px;
        margin: 8px 0;
        letter-spacing: 0.5px;
    }

    /* ===================== AUDIT TRAIL SECTION ===================== */

    /* JSON DISPLAY */
    .stJson {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(15px) !important;
        border: 1.5px solid rgba(79, 172, 254, 0.2) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin: 20px 0 !important;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.1) !important;
    }

    .stJson pre {
        background: rgba(255, 255, 255, 0.02) !important;
        color: #00f2fe !important;
        padding: 20px !important;
        border-radius: 12px !important;
        font-size: 13px !important;
        font-family: 'Monaco', 'Courier New', monospace !important;
        line-height: 1.6 !important;
        overflow-x: auto !important;
        border: 1px solid rgba(79, 172, 254, 0.1) !important;
    }

    .stJson pre::-webkit-scrollbar {
        height: 8px;
        background: rgba(79, 172, 254, 0.1);
    }

    .stJson pre::-webkit-scrollbar-thumb {
        background: rgba(79, 172, 254, 0.3);
        border-radius: 4px;
    }

    /* CODE BLOCKS */
    .stCode {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1.5px solid rgba(79, 172, 254, 0.15) !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        margin: 20px 0 !important;
    }

    .stCode code {
        background: transparent !important;
        color: #00f2fe !important;
        padding: 20px !important;
        display: block !important;
        overflow-x: auto !important;
        font-size: 13px !important;
        line-height: 1.7 !important;
        font-family: 'Monaco', 'Courier New', monospace !important;
    }

    .stCode code::-webkit-scrollbar {
        height: 8px;
        background: rgba(79, 172, 254, 0.1);
    }

    .stCode code::-webkit-scrollbar-thumb {
        background: rgba(79, 172, 254, 0.3);
        border-radius: 4px;
    }

    /* JSON TEXT COLOR FIX */
    .stJson * {
        color: #ffffff !important;
    }

    /* AUDIT SECTION STYLING */
    .audit-section {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.08) 0%, rgba(0, 242, 254, 0.05) 100%);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 18px;
        border: 1.5px solid rgba(79, 172, 254, 0.15);
        margin: 25px 0 20px 0;
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.1);
    }

    .audit-title {
        color: #4facfe !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        margin: 0 !important;
    }

    /* AUDIT TRAIL INFO BOX */
    .audit-info {
        background: linear-gradient(135deg, rgba(79, 172, 254, 0.08) 0%, rgba(0, 242, 254, 0.05) 100%);
        backdrop-filter: blur(15px);
        padding: 25px;
        border-radius: 18px;
        border-left: 4px solid #4facfe;
        margin: 30px 0;
        color: #ffffff;
    }

    .audit-info strong {
        color: #4facfe;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* ===================== END AUDIT TRAIL SECTION ===================== */

    /* ===================== CRITICAL CODE FIX ===================== */

    /* Force all code text to be visible */
    .stCode {
        background: rgba(10, 8, 32, 0.95) !important;
        border: 2px solid #4facfe !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin: 20px 0 !important;
    }

    .stCode code {
        background: rgba(10, 8, 32, 0.95) !important;
        color: #00f2fe !important;
        padding: 20px !important;
        font-size: 13px !important;
        line-height: 1.8 !important;
        font-family: 'Monaco', 'Courier New', monospace !important;
        display: block !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        overflow-x: auto !important;
    }

    /* Force text color in code blocks */
    .stCode * {
        color: #00f2fe !important;
    }

    /* Make sure all pre elements are visible */
    .stCode pre {
        background: rgba(10, 8, 32, 0.95) !important;
        color: #00f2fe !important;
        padding: 20px !important;
    }

    /* Highlight specific JSON elements */
    .stCode .hljs-string {
        color: #38ef7d !important;
    }

    .stCode .hljs-number {
        color: #ff9a56 !important;
    }

    .stCode .hljs-literal {
        color: #4facfe !important;
    }

    .stCode .hljs-attr {
        color: #4facfe !important;
    }

    /* ===================== END CRITICAL CODE FIX ===================== */

    /* ===================== DROPDOWN VISIBILITY FIX - AGGRESSIVE ===================== */

    /* AGGRESSIVE SELECTBOX FIX */
    .stSelectbox {
        background: transparent !important;
    }

    .stSelectbox label {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    /* Target all div levels in selectbox */
    .stSelectbox > div {
        background: transparent !important;
    }

    .stSelectbox > div > div {
        background: transparent !important;
    }

    /* CRITICAL: All select elements */
    select, .stSelectbox select, [role="listbox"] {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
        border: 2px solid #4facfe !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        appearance: none !important;
        -webkit-appearance: none !important;
        -moz-appearance: none !important;
    }

    /* Select on hover */
    select:hover, .stSelectbox select:hover, [role="listbox"]:hover {
        border-color: #00f2fe !important;
        box-shadow: 0 6px 25px rgba(79, 172, 254, 0.3) !important;
        background-color: #ffffff !important;
    }

    /* Select on focus */
    select:focus, .stSelectbox select:focus, [role="listbox"]:focus {
        outline: none !important;
        border-color: #00f2fe !important;
        box-shadow: 0 6px 25px rgba(79, 172, 254, 0.4) !important;
        color: #1a1a1a !important;
    }

    /* OPTIONS - Most critical for visibility */
    select option, .stSelectbox option, [role="option"] {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
        padding: 8px 12px !important;
        line-height: 1.5 !important;
    }

    /* Selected option */
    select option:checked, .stSelectbox option:checked, [role="option"][aria-selected="true"] {
        background: linear-gradient(#4facfe, #4facfe) !important;
        background-color: #4facfe !important;
        color: #ffffff !important;
    }

    /* Ensure text renders */
    .stSelectbox * {
        color: inherit !important;
    }

    /* Override any parent styles */
    .stSelectbox > div > div > select,
    .stSelectbox > div > div select,
    .stSelectbox input,
    .stSelectbox select {
        color: #1a1a1a !important;
        background: #ffffff !important;
        text-color: #1a1a1a !important;
    }

    /* ===================== END DROPDOWN VISIBILITY FIX ===================== */

    /* ===================== CUSTOM BUTTON STYLING FOR DROPDOWNS ===================== */

    /* AGGRESSIVE BUTTON TEXT FIX */
    button {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }

    button * {
        color: #1a1a1a !important;
    }

    /* Style all buttons in the dropdown section */
    .stButton > button {
        background: #ffffff !important;
        color: #1a1a1a !important;
        border: 2px solid #4facfe !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        height: auto !important;
        width: 100% !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-align: center !important;
    }

    .stButton > button * {
        color: #1a1a1a !important;
        font-weight: 700 !important;
    }

    .stButton > button span {
        color: #1a1a1a !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover {
        background: #e8f4ff !important;
        color: #1a1a1a !important;
        border-color: #00f2fe !important;
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.3) !important;
    }

    .stButton > button:hover * {
        color: #1a1a1a !important;
    }

    .stButton > button:hover span {
        color: #1a1a1a !important;
    }

    .stButton > button:active {
        background: #4facfe !important;
        color: #ffffff !important;
        border-color: #00f2fe !important;
    }

    .stButton > button:active * {
        color: #ffffff !important;
    }

    .stButton > button:active span {
        color: #ffffff !important;
    }

    /* Force text visibility */
    .stButton button {
        color: #1a1a1a !important;
    }

    .stButton button:not(:active) {
        color: #1a1a1a !important;
    }

    .stButton button:not(:active) * {
        color: #1a1a1a !important;
    }

    /* ===================== END CUSTOM BUTTON STYLING ===================== */
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

if 'result' not in st.session_state:
    st.session_state.result = None
if 'app_id' not in st.session_state:
    st.session_state.app_id = None
if 'application_history' not in st.session_state:
    st.session_state.application_history = {}
if 'employment' not in st.session_state:
    st.session_state.employment = "Salaried"
if 'location' not in st.session_state:
    st.session_state.location = "New York"

st.markdown("""
<div class="header-premium">
    <h1 class="header-title-premium">SMART LOAN APPROVAL</h1>
    <p class="header-subtitle-premium">Intelligent Multi-Agent Evaluation System</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Application Form", "Decision Results", "Analytics", "Audit Trail", "Applicant Comparison", "Export & Tools", "Advanced Analytics", "Batch Processing"])

with tab1:
    st.markdown("""
    <div class="form-premium">
    <h2 class="form-title-premium">Loan Application Form</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown('<div class="section-header-premium">Personal Profile</div>', unsafe_allow_html=True)
        st.write("")
        name = st.text_input("Applicant Name", value="", placeholder="Enter full name")
        age = st.slider("Age", min_value=18, max_value=100, value=35, step=1)
        income = st.number_input("Annual Income (USD)", min_value=20000, value=100000, step=5000)

        employment = st.radio("Employment Type", ["Salaried", "Self-Employed", "Contract"], index=["Salaried", "Self-Employed", "Contract"].index(st.session_state.employment) if st.session_state.employment in ["Salaried", "Self-Employed", "Contract"] else 0, horizontal=True)

    with col2:
        st.markdown('<div class="section-header-premium">Financial Profile</div>', unsafe_allow_html=True)
        st.write("")
        credit_score = st.slider("Credit Score (300-850)", min_value=300, max_value=850, value=720, step=10)
        liabilities = st.number_input("Existing Liabilities (USD)", min_value=0, value=30000, step=5000)

        locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Miami", "Boston", "Seattle"]
        location = st.radio("Location", locations, index=locations.index(st.session_state.location) if st.session_state.location in locations else 0, horizontal=True)

    st.divider()

    col3, col4 = st.columns(2, gap="large")

    with col3:
        loan_amount = st.number_input("Loan Amount (USD)", min_value=5000, value=250000, step=10000)

    with col4:
        tenure = st.slider("Loan Tenure (Months)", min_value=12, max_value=360, value=60, step=12)

    st.divider()

    monthly_income = income / 12 if income > 0 else 0
    total_debt = liabilities + loan_amount
    dti = total_debt / income if income > 0 else 0

    st.markdown('<div class="section-header-premium">Application Summary</div>', unsafe_allow_html=True)
    st.write("")

    col_s1, col_s2, col_s3, col_s4 = st.columns(4, gap="medium")

    with col_s1:
        st.markdown(f"""
        <div class="metric-card-premium">
            <div class="metric-label-premium">DTI Ratio</div>
            <div class="metric-value-premium">{dti:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_s2:
        st.markdown(f"""
        <div class="metric-card-premium">
            <div class="metric-label-premium">Monthly Income</div>
            <div class="metric-value-premium">${monthly_income:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_s3:
        st.markdown(f"""
        <div class="metric-card-premium">
            <div class="metric-label-premium">Total Debt</div>
            <div class="metric-value-premium">${total_debt:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_s4:
        st.markdown(f"""
        <div class="metric-card-premium">
            <div class="metric-label-premium">Credit Score</div>
            <div class="metric-value-premium">{credit_score}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.write("")

    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

    with col_btn2:
        submit_button = st.button("SUBMIT APPLICATION", use_container_width=True)

    if submit_button:
        progress_placeholder = st.empty()
        status_placeholder = st.empty()

        # FEATURE 1: REAL-TIME PROCESSING STATUS
        steps = [
            "Initializing application...",
            "Analyzing applicant profile...",
            "Calculating financial risk...",
            "Making decision...",
            "Generating compliance report...",
            "Finalizing results..."
        ]

        for i, step in enumerate(steps):
            progress_placeholder.progress((i + 1) / len(steps))
            status_placeholder.write(f"📊 Status: {step}")
            time.sleep(0.3)

        try:
            if not name or name.strip() == "":
                st.error("❌ Please enter applicant name")
            else:
                payload = {
                    "name": name,
                    "age": int(age),
                    "income": int(income),
                    "employment": employment,
                    "credit_score": int(credit_score),
                    "loan_amount": int(loan_amount),
                    "tenure_months": int(tenure),
                    "liabilities": int(liabilities),
                    "location": location
                }

                response = requests.post("http://127.0.0.1:8000/submit", json=payload, timeout=15)

                if response.status_code == 200:
                    result = response.json()
                    st.session_state.result = result['result']
                    st.session_state.app_id = result['application_id']

                    app_id = result['application_id']
                    st.session_state.application_history[app_id] = {
                        "result": result['result'],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "decision": result['result'].get('decision', 'Unknown'),
                        "risk_score": result['result'].get('risk_score', 0),
                        "confidence": result['result'].get('confidence', 0),
                        "applicant_name": name,
                        "age": int(age),
                        "income": int(income),
                        "credit_score": int(credit_score),
                        "loan_amount": int(loan_amount),
                        "liabilities": int(liabilities)
                    }

                    progress_placeholder.empty()
                    status_placeholder.empty()
                    st.success(f"✅ Application {app_id[:12]} for {name} processed successfully!")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Error: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

with tab2:
    st.markdown('<div class="form-title-premium">Decision Results & Application Lookup</div>', unsafe_allow_html=True)

    search_col1, search_col2 = st.columns([2, 1])

    with search_col1:
        search_name = st.text_input("🔍 Search Application by Applicant Name", value="", placeholder="Enter applicant name to find previous applications")

    with search_col2:
        search_btn = st.button("Search", use_container_width=True)

    if search_btn and search_name:
        try:
            search_response = requests.get(f"http://127.0.0.1:8000/apps/search/{search_name}")
            if search_response.status_code == 200:
                search_results = search_response.json()
                if search_results['results_count'] > 0:
                    st.success(f"✅ Found {search_results['results_count']} application(s) for '{search_name}'")
                    for idx, app in enumerate(search_results['applications'], 1):
                        col_a, col_b, col_c = st.columns(3)
                        with col_a:
                            st.markdown(f"""
                            <div class="metric-card-premium">
                                <div class="metric-label-premium">App #{idx}</div>
                                <div class="metric-value-premium">{app.get('application_id', 'N/A')[:8]}...</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_b:
                            decision = app.get('decision', 'Unknown')
                            st.markdown(f"""
                            <div class="metric-card-premium">
                                <div class="metric-label-premium">Decision</div>
                                <div class="metric-value-premium">{decision}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_c:
                            st.markdown(f"""
                            <div class="metric-card-premium">
                                <div class="metric-label-premium">Risk Score</div>
                                <div class="metric-value-premium">{app.get('risk_score', 'N/A')}/100</div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.write("")
                        st.caption(f"📅 {app.get('timestamp', 'N/A')} | 📊 Confidence: {app.get('confidence', 'N/A')}%")
                        st.write("")
                else:
                    st.warning(f"⚠️ No applications found for '{search_name}'. Try a different spelling or partial name.")
        except Exception as e:
            st.error(f"❌ Search error: {str(e)}")

    st.divider()

    if st.session_state.result is not None:
        result = st.session_state.result
        decision = result.get('decision', 'UNKNOWN')
        risk_score = result.get('risk_score', 0)
        confidence = result.get('confidence', 0)

        if decision == 'Approve':
            st.markdown('<div class="decision-approved-premium">✅ APPROVED</div>', unsafe_allow_html=True)
        elif decision == 'Reject':
            st.markdown('<div class="decision-rejected-premium">❌ REJECTED</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="decision-review-premium">⚠️ REVIEW REQUIRED</div>', unsafe_allow_html=True)

        st.write("")

        col1, col2, col3, col4 = st.columns(4, gap="medium")

        with col1:
            st.markdown(f"""
            <div class="metric-card-premium">
                <div class="metric-label-premium">Decision</div>
                <div class="metric-value-premium">{decision}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card-premium">
                <div class="metric-label-premium">Risk Score</div>
                <div class="metric-value-premium">{risk_score}/100</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card-premium">
                <div class="metric-label-premium">Confidence</div>
                <div class="metric-value-premium">{confidence}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            case_id = result.get('case_id', 'N/A')[:12] if result.get('case_id') else 'N/A'
            st.markdown(f"""
            <div class="metric-card-premium">
                <div class="metric-label-premium">Case ID</div>
                <div class="metric-value-premium" style="font-size: 18px;">{case_id}...</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        col_exp1, col_exp2 = st.columns(2, gap="large")

        with col_exp1:
            st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">Decision Explanation</h3>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="explanation-premium">
                {result.get('explanation', 'No explanation available')}
            </div>
            """, unsafe_allow_html=True)

        with col_exp2:
            st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">Key Factors</h3>', unsafe_allow_html=True)
            factors = result.get('key_factors', [])
            if factors:
                for idx, factor in enumerate(factors, 1):
                    st.markdown(f"""
                    <div class="factor-premium">
                        <strong>Factor {idx}:</strong> {factor}
                    </div>
                    """, unsafe_allow_html=True)

        st.divider()
        st.write("")

        st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">Risk Assessment</h3>', unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#4facfe"},
                'steps': [
                    {'range': [0, 30], 'color': "#11998e"},
                    {'range': [30, 70], 'color': "#ffd166"},
                    {'range': [70, 100], 'color': "#eb3349"}
                ]
            }
        ))
        fig.update_layout(height=450, margin=dict(l=10, r=10, t=50, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=14))
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.write("")

        st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">Confidence Level</h3>', unsafe_allow_html=True)
        fig2 = go.Figure(data=[
            go.Bar(
                x=['Confidence'],
                y=[confidence],
                marker=dict(
                    color=['#11998e' if confidence < 50 else '#ffd166' if confidence < 80 else '#4facfe']
                ),
                text=[f'{confidence}%'],
                textposition='auto',
                textfont=dict(size=24, color='white')
            )
        ])
        fig2.update_layout(
            height=350,
            yaxis=dict(range=[0, 100]),
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=14),
            showlegend=False
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.divider()
        st.write("")

        # FEATURE 2: APPLICATION RATING SYSTEM
        st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">Application Strength Rating</h3>', unsafe_allow_html=True)

        strength_score = 0
        credit_score_val = result.get('credit_score', 650) if 'credit_score' in result else (st.session_state.application_history[st.session_state.app_id].get('credit_score', 650) if st.session_state.app_id in st.session_state.application_history else 650)
        income_val = result.get('income', 100000) if 'income' in result else (st.session_state.application_history[st.session_state.app_id].get('income', 100000) if st.session_state.app_id in st.session_state.application_history else 100000)
        dti_val = (result.get('liabilities', 0) if 'liabilities' in result else st.session_state.application_history[st.session_state.app_id].get('liabilities', 0)) + (result.get('loan_amount', 250000) if 'loan_amount' in result else st.session_state.application_history[st.session_state.app_id].get('loan_amount', 250000))
        dti_val = dti_val / income_val if income_val > 0 else 0

        if credit_score_val >= 750:
            strength_score += 1.5
        if income_val >= 100000:
            strength_score += 1
        if dti_val < 2.5:
            strength_score += 1
        if employment == "Salaried":
            strength_score += 0.5
        liabilities_val = result.get('liabilities', 0) if 'liabilities' in result else st.session_state.application_history[st.session_state.app_id].get('liabilities', 0)
        if liabilities_val < 50000:
            strength_score += 0.5

        strength_score = min(5, strength_score)
        stars = int(strength_score)
        partial = strength_score - stars
        star_display = "⭐" * stars + ("✨" if partial > 0.3 else "")

        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: rgba(79, 172, 254, 0.1); border-radius: 15px; border: 1.5px solid rgba(79, 172, 254, 0.2);">
            <div style="font-size: 40px; margin-bottom: 10px;">{star_display}</div>
            <div style="font-size: 24px; color: #ffd166; font-weight: 700;">Strength Score: {strength_score:.1f} / 5.0</div>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        # FEATURE 3: RISK PROFILE SUMMARY
        st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">Risk Profile Summary</h3>', unsafe_allow_html=True)

        risk_summary = ""
        if risk_score <= 20:
            risk_summary = "✅ Excellent applicant with minimal risk. Strong financials and excellent credit history."
        elif risk_score <= 40:
            risk_summary = "✅ Good applicant with low risk. Solid financial profile and stable employment."
        elif risk_score <= 60:
            risk_summary = "⚠️ Moderate applicant with acceptable risk. Some concerns but generally manageable."
        elif risk_score <= 80:
            risk_summary = "⚠️ Higher risk applicant. Notable concerns in financial profile. Requires monitoring."
        else:
            risk_summary = "❌ High risk applicant. Significant concerns. Recommend manual review."

        st.info(risk_summary)

        st.write("")

        # FEATURE 4: LOAN RECOMMENDATION
        st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">Recommended Loan Terms</h3>', unsafe_allow_html=True)

        recommended_amount = income_val * 3
        recommended_tenure = 60
        recommended_rate_adjustment = risk_score / 100

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(17, 153, 142, 0.2) 0%, rgba(0, 242, 254, 0.1) 100%); padding: 25px; border-radius: 15px; border-left: 4px solid #11998e;">
            <strong style="color: #11998e; font-size: 16px; text-transform: uppercase;">RECOMMENDED LOAN TERMS:</strong><br><br>
            <span style="color: #ffffff;">
            <strong>💰 Safe Loan Amount:</strong> ${recommended_amount:,.0f}<br>
            <strong>⏱️ Recommended Tenure:</strong> {recommended_tenure} months<br>
            <strong>📊 Interest Rate Adjustment:</strong> {recommended_rate_adjustment:.1f}%<br>
            <br>
            Your requested loan of ${result.get('loan_amount', loan_amount) if 'loan_amount' in result else loan_amount:,.0f} is <span style="color: #4facfe;"><strong>{'within recommended range' if result.get('loan_amount', loan_amount) <= recommended_amount else 'above recommended amount'}</strong></span>.
            </span>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.write("")

        st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">AI-Powered Insights</h3>', unsafe_allow_html=True)
        st.write("")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            dti = total_debt / income if income > 0 else 0
            credit_grade = "Excellent" if credit_score >= 750 else "Good" if credit_score >= 700 else "Fair" if credit_score >= 650 else "Poor"
            income_level = "High" if income >= 150000 else "Medium" if income >= 75000 else "Low"

            strengths = []
            if credit_score >= 700:
                strengths.append(f"Excellent credit score ({credit_score})")
            if dti < 2.5:
                strengths.append(f"Healthy DTI ratio ({dti:.2f})")
            if income >= 100000:
                strengths.append(f"Strong income (${income:,})")

            strength = strengths[0] if strengths else "Stable employment"

            st.markdown(f"""
            <div class="explanation-premium">
                <strong style="color: #00f2fe; font-size: 16px;">KEY STRENGTH</strong><br>
                {strength}
                <br><br>
                <strong style="color: #4facfe;">Why this matters:</strong> This factor significantly increases your approval chances by approximately 30-40 percent.
            </div>
            """, unsafe_allow_html=True)

        with col2:
            weaknesses = []
            if credit_score < 700:
                weaknesses.append(f"Credit score ({credit_score}) is below 700")
            if dti > 3.0:
                weaknesses.append(f"DTI ratio ({dti:.2f}) is higher than ideal")
            if income < 60000:
                weaknesses.append(f"Income level (${income:,}) is moderate")

            weakness = weaknesses[0] if weaknesses else "Could improve some factors"
            improvement = ""

            if dti > 3.0:
                improvement = f"Reducing debt by 20 percent would lower DTI to {dti*0.8:.2f}"
            elif credit_score < 700:
                improvement = "Improving credit score by 50 points would enhance approval chances"
            elif income < 100000:
                improvement = "Increasing income would strengthen your application"

            st.markdown(f"""
            <div class="explanation-premium">
                <strong style="color: #ff9a56; font-size: 16px;">KEY WEAKNESS</strong><br>
                {weakness}
                <br><br>
                <strong style="color: #4facfe;">Improvement path:</strong> {improvement}
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        col1, col2, col3 = st.columns(3, gap="small")

        with col1:
            approval_prob = 50
            if credit_score >= 750:
                approval_prob += 20
            elif credit_score >= 700:
                approval_prob += 15
            elif credit_score >= 650:
                approval_prob += 10

            if dti < 2.0:
                approval_prob += 15
            elif dti < 2.5:
                approval_prob += 10
            elif dti < 3.0:
                approval_prob += 5

            if income >= 150000:
                approval_prob += 10
            elif income >= 100000:
                approval_prob += 5

            approval_prob = min(99, max(10, approval_prob))

            st.markdown(f"""
            <div class="metric-card-premium">
                <div class="metric-label-premium">Approval Probability</div>
                <div class="metric-value-premium">{approval_prob}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            percentile = 50
            if credit_score >= 750:
                percentile += 20
            if dti < 2.5:
                percentile += 15
            if income >= 120000:
                percentile += 15

            percentile = min(99, percentile)
            percentile_label = "Top 10 percent" if percentile >= 90 else "Top 25 percent" if percentile >= 75 else "Top 50 percent" if percentile >= 50 else "Bottom 50 percent"

            st.markdown(f"""
            <div class="metric-card-premium">
                <div class="metric-label-premium">Applicant Percentile</div>
                <div class="metric-value-premium">{percentile_label}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            risk_category = "Low Risk" if risk_score <= 30 else "Medium Risk" if risk_score <= 60 else "High Risk"
            risk_color = "#11998e" if risk_score <= 30 else "#ffd166" if risk_score <= 60 else "#eb3349"

            st.markdown(f"""
            <div class="metric-card-premium">
                <div class="metric-label-premium">Risk Category</div>
                <div class="metric-value-premium" style="color: {risk_color};">{risk_category}</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.write("")

        st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">Decision Factor Analysis</h3>', unsafe_allow_html=True)
        st.write("")

        dti = total_debt / income if income > 0 else 0
        credit_strength = (credit_score - 300) / 5.5
        income_strength = min(100, (income / 2000))
        dti_strength = max(0, 100 - (dti * 20))
        employment_strength = 80 if employment == "Salaried" else 60 if employment == "Self-Employed" else 70
        assets_strength = min(100, (liabilities / 10000) + 50)

        factors = {
            "Credit Score": credit_strength,
            "Income Level": income_strength,
            "DTI Ratio": dti_strength,
            "Employment Stability": employment_strength,
            "Financial Assets": assets_strength
        }

        fig_factors = go.Figure()

        fig_factors.add_trace(go.Bar(
            y=list(factors.keys()),
            x=list(factors.values()),
            orientation='h',
            marker=dict(
                color=list(factors.values()),
                colorscale='RdYlGn',
                line=dict(color='rgba(255,255,255,0.3)', width=2),
                cmin=0,
                cmax=100
            ),
            text=[f"{v:.0f}%" for v in factors.values()],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Strength: %{x:.1f}%<extra></extra>'
        ))

        fig_factors.update_layout(
            showlegend=False,
            height=350,
            margin=dict(l=150, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            xaxis=dict(
                range=[0, 100],
                ticktext=['0%', '25%', '50%', '75%', '100%'],
                tickvals=[0, 25, 50, 75, 100],
                gridcolor='rgba(255,255,255,0.1)'
            ),
            yaxis=dict(
                tickfont=dict(size=14, color='white')
            )
        )

        st.plotly_chart(fig_factors, use_container_width=True)

        st.info("Factor Strength Analysis - Green: Strong (100 percent) | Yellow: Moderate (50 percent) | Red: Weak (0 percent). Each factor contributes to the final decision. Stronger factors increase approval chances.")

        st.divider()
        st.write("")

        st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">What-If Scenario Analysis</h3>', unsafe_allow_html=True)
        st.write("Explore how changes to your application would affect the decision")
        st.write("")

        scenario_tabs = st.tabs(["Improve Credit Score", "Increase Income", "Reduce Debt", "Combined Scenario"])

        dti = total_debt / income if income > 0 else 0
        approval_prob = 50
        if credit_score >= 750:
            approval_prob += 20
        elif credit_score >= 700:
            approval_prob += 15
        elif credit_score >= 650:
            approval_prob += 10

        if dti < 2.0:
            approval_prob += 15
        elif dti < 2.5:
            approval_prob += 10
        elif dti < 3.0:
            approval_prob += 5

        if income >= 150000:
            approval_prob += 10
        elif income >= 100000:
            approval_prob += 5

        approval_prob = min(99, max(10, approval_prob))

        with scenario_tabs[0]:
            col1, col2 = st.columns([2, 1])

            with col1:
                scenario_credit = st.slider(
                    "Adjust Credit Score:",
                    min_value=300,
                    max_value=850,
                    value=credit_score,
                    step=10,
                    key="credit_scenario"
                )

            with col2:
                credit_change = scenario_credit - credit_score
                if credit_change > 0:
                    st.markdown(f"""
                    <div style="background: rgba(17, 153, 142, 0.3); padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="color: #38ef7d; font-size: 24px; font-weight: bold;">+{credit_change}</div>
                        <div style="color: #ffffff; font-size: 12px;">Point increase</div>
                    </div>
                    """, unsafe_allow_html=True)
                elif credit_change < 0:
                    st.markdown(f"""
                    <div style="background: rgba(235, 51, 73, 0.3); padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="color: #f45c43; font-size: 24px; font-weight: bold;">{credit_change}</div>
                        <div style="color: #ffffff; font-size: 12px;">Point decrease</div>
                    </div>
                    """, unsafe_allow_html=True)

            new_approval_prob = approval_prob + (scenario_credit - credit_score) / 10
            new_approval_prob = min(99, max(10, new_approval_prob))

            result_text = "This would likely result in APPROVAL" if new_approval_prob >= 75 else "Still borderline" if new_approval_prob >= 50 else "Would likely be REJECTED"

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(79, 172, 254, 0.15) 0%, rgba(0, 242, 254, 0.1) 100%); padding: 20px; border-radius: 15px; border-left: 5px solid #4facfe;">
                <strong style="color: #4facfe; font-size: 14px;">SCENARIO RESULT:</strong><br>
                <div style="margin-top: 10px; color: #ffffff;">
                    With credit score of <strong>{scenario_credit}</strong>:
                </div>
                <div style="margin-top: 8px;">
                    <strong style="color: #00f2fe; font-size: 18px;">Approval Probability: {new_approval_prob:.0f}%</strong>
                </div>
                <div style="margin-top: 8px; color: #ffffff; font-size: 13px;">
                    {result_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with scenario_tabs[1]:
            col1, col2 = st.columns([2, 1])

            with col1:
                scenario_income = st.slider(
                    "Adjust Annual Income:",
                    min_value=20000,
                    max_value=500000,
                    value=income,
                    step=10000,
                    key="income_scenario"
                )

            with col2:
                income_change = scenario_income - income
                if income_change > 0:
                    st.markdown(f"""
                    <div style="background: rgba(17, 153, 142, 0.3); padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="color: #38ef7d; font-size: 18px; font-weight: bold;">+${income_change:,}</div>
                        <div style="color: #ffffff; font-size: 12px;">Income increase</div>
                    </div>
                    """, unsafe_allow_html=True)

            new_dti = total_debt / scenario_income if scenario_income > 0 else dti
            new_approval_prob = approval_prob + ((income - scenario_income) / 100000) * 5
            new_approval_prob = min(99, max(10, new_approval_prob))

            result_text = "This would likely result in APPROVAL" if new_approval_prob >= 75 else "Still borderline" if new_approval_prob >= 50 else "Would likely be REJECTED"

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(79, 172, 254, 0.15) 0%, rgba(0, 242, 254, 0.1) 100%); padding: 20px; border-radius: 15px; border-left: 5px solid #4facfe;">
                <strong style="color: #4facfe; font-size: 14px;">SCENARIO RESULT:</strong><br>
                <div style="margin-top: 10px; color: #ffffff;">
                    With annual income of <strong>${scenario_income:,}</strong>:
                </div>
                <div style="margin-top: 8px;">
                    <strong style="color: #00f2fe;">New DTI Ratio: {new_dti:.2f}</strong><br>
                    <strong style="color: #00f2fe; font-size: 18px;">Approval Probability: {new_approval_prob:.0f}%</strong>
                </div>
                <div style="margin-top: 8px; color: #ffffff; font-size: 13px;">
                    {result_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with scenario_tabs[2]:
            col1, col2 = st.columns([2, 1])

            with col1:
                debt_reduction = st.slider(
                    "Reduce Debt by (%):",
                    min_value=0,
                    max_value=100,
                    value=0,
                    step=5,
                    key="debt_scenario"
                )

            with col2:
                if debt_reduction > 0:
                    st.markdown(f"""
                    <div style="background: rgba(17, 153, 142, 0.3); padding: 15px; border-radius: 10px; text-align: center;">
                        <div style="color: #38ef7d; font-size: 20px; font-weight: bold;">-{debt_reduction}%</div>
                        <div style="color: #ffffff; font-size: 12px;">Debt reduction</div>
                    </div>
                    """, unsafe_allow_html=True)

            new_total_debt = total_debt * (1 - debt_reduction / 100)
            new_dti = new_total_debt / income if income > 0 else dti
            new_approval_prob = approval_prob + (dti - new_dti) * 15
            new_approval_prob = min(99, max(10, new_approval_prob))

            result_text = "This would likely result in APPROVAL" if new_approval_prob >= 75 else "Still borderline" if new_approval_prob >= 50 else "Would likely be REJECTED"

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(79, 172, 254, 0.15) 0%, rgba(0, 242, 254, 0.1) 100%); padding: 20px; border-radius: 15px; border-left: 5px solid #4facfe;">
                <strong style="color: #4facfe; font-size: 14px;">SCENARIO RESULT:</strong><br>
                <div style="margin-top: 10px; color: #ffffff;">
                    After reducing debt by <strong>{debt_reduction}%</strong>:
                </div>
                <div style="margin-top: 8px;">
                    <strong style="color: #00f2fe;">New Total Debt: ${new_total_debt:,.0f}</strong><br>
                    <strong style="color: #00f2fe;">New DTI Ratio: {new_dti:.2f}</strong><br>
                    <strong style="color: #00f2fe; font-size: 18px;">Approval Probability: {new_approval_prob:.0f}%</strong>
                </div>
                <div style="margin-top: 8px; color: #ffffff; font-size: 13px;">
                    {result_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with scenario_tabs[3]:
            st.write("Combine multiple improvements to see cumulative impact")

            col1, col2, col3 = st.columns(3)

            with col1:
                combo_credit = st.slider("Credit Score:", 300, 850, credit_score, key="combo_credit")
            with col2:
                combo_income = st.slider("Annual Income:", 20000, 500000, income, key="combo_income")
            with col3:
                combo_debt = st.slider("Reduce Debt (%):", 0, 100, 0, key="combo_debt")

            new_dti_combo = ((total_debt * (1 - combo_debt / 100)) / combo_income) if combo_income > 0 else dti

            credit_impact = (combo_credit - credit_score) / 10
            income_impact = ((combo_income - income) / 100000) * 5
            debt_impact = ((dti - new_dti_combo) * 15) if new_dti_combo < dti else 0

            new_approval_prob_combo = approval_prob + credit_impact + income_impact + debt_impact
            new_approval_prob_combo = min(99, max(10, new_approval_prob_combo))

            result_text = "HIGHLY LIKELY TO APPROVE!" if new_approval_prob_combo >= 90 else "This would likely result in APPROVAL" if new_approval_prob_combo >= 75 else "Still borderline" if new_approval_prob_combo >= 50 else "Would likely be REJECTED"

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(79, 172, 254, 0.15) 0%, rgba(0, 242, 254, 0.1) 100%); padding: 20px; border-radius: 15px; border-left: 5px solid #4facfe;">
                <strong style="color: #4facfe; font-size: 14px;">COMBINED SCENARIO RESULT:</strong><br>
                <div style="margin-top: 10px; color: #ffffff;">
                    <strong>Credit Score:</strong> {combo_credit}<br>
                    <strong>Annual Income:</strong> ${combo_income:,}<br>
                    <strong>DTI Ratio:</strong> {new_dti_combo:.2f}
                </div>
                <div style="margin-top: 12px;">
                    <strong style="color: #00f2fe; font-size: 20px;">Approval Probability: {new_approval_prob_combo:.0f}%</strong>
                </div>
                <div style="margin-top: 8px; color: #ffffff; font-size: 13px;">
                    {result_text}
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown('<div style="color: white; padding: 40px; text-align: center; font-size: 18px;">No results yet. Submit an application to see results!</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<h3 style="color: #4facfe; font-size: 24px; text-transform: uppercase; letter-spacing: 1px;">Analytics Dashboard</h3>', unsafe_allow_html=True)
    st.write("")

    app_history = st.session_state.get("application_history", {})
    total_apps = len(app_history)

    approved = 0
    rejected = 0
    under_review = 0

    for app_id, app_data in app_history.items():
        decision = app_data.get("decision", "Unknown")
        if decision == "Approve":
            approved += 1
        elif decision == "Reject":
            rejected += 1
        elif decision == "Review":
            under_review += 1

    approval_rate = (approved / total_apps * 100) if total_apps > 0 else 0

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown(f"""
        <div class="analytics-card-premium">
            <div class="analytics-label-premium">Total Applications</div>
            <div class="analytics-value-premium">{total_apps}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="analytics-card-premium">
            <div class="analytics-label-premium">Approval Rate</div>
            <div class="analytics-value-premium">{approval_rate:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="analytics-card-premium">
            <div class="analytics-label-premium">Processing Time</div>
            <div class="analytics-value-premium">2.5s</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.write("")

    # FEATURE 5: QUICK STATISTICS BOX
    st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">Quick Statistics</h3>', unsafe_allow_html=True)

    if total_apps > 0:
        avg_risk = sum([a.get("risk_score", 0) for a in app_history.values()]) / max(1, total_apps)
        avg_confidence = sum([a.get("confidence", 0) for a in app_history.values()]) / max(1, total_apps)

        col1, col2, col3, col4 = st.columns(4, gap="medium")

        with col1:
            st.metric("Avg Risk Score", f"{avg_risk:.0f}/100")

        with col2:
            st.metric("Avg Confidence", f"{avg_confidence:.0f}%")

        with col3:
            st.metric("Total Cases", total_apps)

        with col4:
            st.metric("Approval Rate", f"{approval_rate:.1f}%")
    else:
        st.info("Submit applications to see statistics.")

    st.divider()
    st.write("")

    if total_apps > 0:
        st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">Decision Distribution</h3>', unsafe_allow_html=True)
        decision_counts = {
            'Approved': approved,
            'Rejected': rejected,
            'Review': under_review
        }
        df = pd.DataFrame({
            'Decision': list(decision_counts.keys()),
            'Count': list(decision_counts.values())
        })
        fig = px.pie(df, values='Count', names='Decision',
                    color_discrete_sequence=['#11998e', '#eb3349', '#f77062'],
                    height=450)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=12))
        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.write("")

        st.markdown('<h3 style="color: #4facfe; font-size: 20px; text-transform: uppercase; letter-spacing: 1px;">Risk Trends</h3>', unsafe_allow_html=True)
        app_ids = [app_id[:8] for app_id in app_history.keys()]
        risk_scores = [app_data.get('risk_score', 0) for app_data in app_history.values()]

        df_risk = pd.DataFrame({
            'Application': app_ids,
            'Risk Score': risk_scores
        })
        fig = px.bar(df_risk, x='Application', y='Risk Score',
                    color='Risk Score',
                    color_continuous_scale=['#11998e', '#ffd166', '#eb3349'],
                    height=400)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=12), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Submit applications to see analytics data")

with tab4:
    st.markdown('<h3 style="color: #4facfe; font-size: 24px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 30px;">Audit Trail</h3>', unsafe_allow_html=True)
    st.write("")

    if "result" in st.session_state and st.session_state.result is not None:
        result = st.session_state.result

        st.markdown('<div class="audit-section"><div class="audit-title">Application Details</div></div>', unsafe_allow_html=True)

        app_details = {
            "Application ID": str(result.get('application_id', 'N/A')),
            "Case ID": str(result.get('case_id', 'N/A')),
            "Decision": str(result.get('decision', 'N/A')),
            "Risk Score": str(result.get('risk_score', 'N/A')),
            "Confidence": f"{result.get('confidence', 'N/A')}%",
            "Timestamp": str(result.get('timestamp', 'N/A'))
        }

        app_json_str = json.dumps(app_details, indent=2)
        st.markdown(f"""
        <div style="
            background: rgba(10, 8, 32, 0.9);
            border: 2px solid #4facfe;
            border-radius: 15px;
            padding: 25px;
            color: #00f2fe;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.8;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 20px 0;
        ">
{app_json_str}
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.markdown('<div class="audit-section"><div class="audit-title">Agent Analysis</div></div>', unsafe_allow_html=True)

        agent_analysis = {
            "Explanation": str(result.get('explanation', 'N/A')),
            "Key Factors": result.get('key_factors', []),
            "Notification": str(result.get('notification', 'N/A'))
        }

        agent_json_str = json.dumps(agent_analysis, indent=2)
        st.markdown(f"""
        <div style="
            background: rgba(10, 8, 32, 0.9);
            border: 2px solid #4facfe;
            border-radius: 15px;
            padding: 25px;
            color: #00f2fe;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.8;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 20px 0;
        ">
{agent_json_str}
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.write("")

        st.markdown('<div class="audit-section"><div class="audit-title">Complete Audit Log (JSON)</div></div>', unsafe_allow_html=True)
        st.write("")

        full_audit_str = json.dumps(result, indent=2)
        st.markdown(f"""
        <div style="
            background: rgba(10, 8, 32, 0.9);
            border: 2px solid #4facfe;
            border-radius: 15px;
            padding: 25px;
            color: #00f2fe;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 13px;
            line-height: 1.8;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
            margin: 20px 0;
            max-height: 600px;
            overflow-y: auto;
        ">
{full_audit_str}
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(79, 172, 254, 0.08) 0%, rgba(0, 242, 254, 0.05) 100%);
            backdrop-filter: blur(15px);
            padding: 25px;
            border-radius: 18px;
            border-left: 4px solid #4facfe;
            margin-top: 30px;
            color: #ffffff;
            font-size: 14px;
            line-height: 1.8;
        ">
            <strong style="color: #4facfe; text-transform: uppercase; letter-spacing: 1px;">Audit Trail Information:</strong><br>
            All loan application decisions are recorded in this complete audit trail for compliance and traceability purposes.
            Each application receives a unique Case ID and Application ID for tracking. The timestamp records when the decision
            was made, and the agent analysis shows the exact reasoning behind the decision.
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.05) 100%);
            backdrop-filter: blur(15px);
            padding: 60px;
            border-radius: 20px;
            text-align: center;
            color: #ffffff;
            font-size: 18px;
            border: 1.5px solid rgba(79, 172, 254, 0.2);
            margin: 40px 0;
        ">
            <p style="margin: 0; font-weight: 600; color: #4facfe; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">No Audit Data Yet</p>
            <p style="margin: 0; color: rgba(255, 255, 255, 0.7);">Submit an application to see the complete audit trail</p>
        </div>
        """, unsafe_allow_html=True)

# ===== FEATURE 6: APPLICANT COMPARISON =====
with tab5:
    st.markdown('<h3 style="color: #4facfe; font-size: 24px; text-transform: uppercase; letter-spacing: 1px;">Applicant Comparison</h3>', unsafe_allow_html=True)
    st.write("")

    app_history = st.session_state.get("application_history", {})

    if "result" in st.session_state and st.session_state.result and len(app_history) > 1:
        result = st.session_state.result
        current_risk = result.get('risk_score', 0)
        current_confidence = result.get('confidence', 0)

        avg_risk = sum([a.get("risk_score", 0) for a in app_history.values()]) / len(app_history)
        avg_confidence = sum([a.get("confidence", 0) for a in app_history.values()]) / len(app_history)

        st.markdown('<h4 style="color: #4facfe;">How You Compare:</h4>', unsafe_allow_html=True)
        st.write("")

        col1, col2 = st.columns(2, gap="large")

        with col1:
            col1a, col1b = st.columns(2, gap="medium")
            with col1a:
                st.markdown(f"""
                <div class="metric-card-premium">
                    <div class="metric-label-premium">Your Risk Score</div>
                    <div class="metric-value-premium">{current_risk}</div>
                </div>
                """, unsafe_allow_html=True)
            with col1b:
                st.markdown(f"""
                <div class="metric-card-premium">
                    <div class="metric-label-premium">Average Risk</div>
                    <div class="metric-value-premium">{avg_risk:.0f}</div>
                </div>
                """, unsafe_allow_html=True)

            risk_diff = current_risk - avg_risk
            if risk_diff < -5:
                st.success(f"✅ Better than average (−{abs(risk_diff):.0f} points)")
            elif risk_diff > 5:
                st.warning(f"⚠️ Higher than average (+{risk_diff:.0f} points)")
            else:
                st.info(f"ℹ️ Close to average (±{abs(risk_diff):.0f} points)")

        with col2:
            col2a, col2b = st.columns(2, gap="medium")
            with col2a:
                st.markdown(f"""
                <div class="metric-card-premium">
                    <div class="metric-label-premium">Your Confidence</div>
                    <div class="metric-value-premium">{current_confidence}%</div>
                </div>
                """, unsafe_allow_html=True)
            with col2b:
                st.markdown(f"""
                <div class="metric-card-premium">
                    <div class="metric-label-premium">Average Confidence</div>
                    <div class="metric-value-premium">{avg_confidence:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)

            conf_diff = current_confidence - avg_confidence
            if conf_diff > 5:
                st.success(f"✅ More confident than average (+{conf_diff:.0f}%)")
            elif conf_diff < -5:
                st.warning(f"⚠️ Less confident than average (−{abs(conf_diff):.0f}%)")
            else:
                st.info(f"ℹ️ Close to average (±{abs(conf_diff):.0f}%)")

        st.divider()
        st.write("")

        # FEATURE 8: DECISION HISTORY TIMELINE
        st.markdown('<h4 style="color: #4facfe;">Decision Timeline (Last 10 Applications):</h4>', unsafe_allow_html=True)

        timeline_data = []
        for app_id, app_data in list(app_history.items())[-10:]:
            timeline_data.append({
                "Time": app_data.get("timestamp", "N/A"),
                "Decision": app_data.get("decision", "Unknown"),
                "Risk": app_data.get("risk_score", 0),
                "Confidence": f"{app_data.get('confidence', 0)}%"
            })

        df_timeline = pd.DataFrame(timeline_data)
        st.dataframe(df_timeline, use_container_width=True, hide_index=True)

    else:
        st.info("📊 Submit at least 2 applications to see comparison metrics and timeline")

# ===== FEATURE 7: EXPORT & TOOLS =====
with tab6:
    st.markdown('<h3 style="color: #4facfe; font-size: 24px; text-transform: uppercase; letter-spacing: 1px;">Export & Tools</h3>', unsafe_allow_html=True)
    st.write("")

    if "result" in st.session_state and st.session_state.result is not None:
        result = st.session_state.result

        # FEATURE 7: EXPORT DECISION TO PDF (as text report)
        st.markdown('<h4 style="color: #4facfe;">📄 Export Decision Report</h4>', unsafe_allow_html=True)

        report = f"""LOAN DECISION REPORT
=====================================

Application ID: {result.get('application_id', 'N/A')}
Case ID: {result.get('case_id', 'N/A')}
Date: {result.get('timestamp', 'N/A')}

DECISION SUMMARY
=====================================
Decision: {result.get('decision', 'N/A')}
Risk Score: {result.get('risk_score', 'N/A')}/100
Confidence: {result.get('confidence', 'N/A')}%

EXPLANATION
=====================================
{result.get('explanation', 'N/A')}

KEY FACTORS
=====================================
"""
        for i, factor in enumerate(result.get('key_factors', []), 1):
            report += f"{i}. {factor}\n"

        col1, col2 = st.columns(2, gap="medium")

        with col1:
            st.download_button(
                label="📥 Download as Text",
                data=report,
                file_name=f"decision_{result.get('application_id', 'report')[:12]}.txt",
                mime="text/plain"
            )

        with col2:
            st.download_button(
                label="📋 Download as JSON",
                data=json.dumps(result, indent=2),
                file_name=f"decision_{result.get('application_id', 'report')[:12]}.json",
                mime="application/json"
            )

        st.divider()
        st.write("")

        # FEATURE 9: BATCH SUMMARY EMAIL
        st.markdown('<h4 style="color: #4facfe;">📧 Email Summary Generator</h4>', unsafe_allow_html=True)

        app_history = st.session_state.get("application_history", {})
        total_apps = len(app_history)
        approved = sum(1 for a in app_history.values() if a.get("decision") == "Approve")
        rejected = sum(1 for a in app_history.values() if a.get("decision") == "Reject")
        under_review = sum(1 for a in app_history.values() if a.get("decision") == "Review")
        approval_rate = (approved / total_apps * 100) if total_apps > 0 else 0

        if st.button("Generate Email Summary"):
            email_summary = f"""Subject: Loan Application Summary Report

Hello,

Please find below the loan application processing summary for your records:

=== APPLICATION STATISTICS ===
Total Applications Processed: {total_apps}
Approved: {approved}
Rejected: {rejected}
Under Review: {under_review}
Approval Rate: {approval_rate:.1f}%

=== PERFORMANCE METRICS ===
Average Risk Score: {sum([a.get('risk_score', 0) for a in app_history.values()]) / max(1, total_apps):.1f}
Average Confidence: {sum([a.get('confidence', 0) for a in app_history.values()]) / max(1, total_apps):.1f}%

=== RECENT DECISIONS ==="""

            for app_id, app_data in list(app_history.items())[-5:]:
                email_summary += f"\n- {app_data.get('timestamp', 'N/A')}: {app_data.get('decision', 'Unknown')} (Risk: {app_data.get('risk_score', 0)})"

            email_summary += """

Best Regards,
Smart Loan Approval System
Powered by Advanced AI
"""
            st.text_area("📨 Email Summary (Copy & Paste)", email_summary, height=250)

        st.divider()
        st.write("")

        # FEATURE 10: AGENT INSIGHTS
        st.markdown('<h4 style="color: #4facfe;">🤖 Agent Decision Insights</h4>', unsafe_allow_html=True)

        st.write("📋 **APPLICANT PROFILE AGENT**")
        st.write("Analyzed employment stability, income consistency, and career longevity. Evaluated whether the applicant has stable, verifiable income sources and reasonable employment duration.")

        st.write("")
        st.write("💰 **FINANCIAL RISK AGENT**")
        st.write("Evaluated debt-to-income ratio, credit score history, existing liabilities, and overall financial health. Assessed the applicant's ability to manage additional loan obligations.")

        st.write("")
        st.write("✅ **LOAN DECISION AGENT**")
        st.write("Made the final approval decision by synthesizing all analysis from profile and financial risk agents. Applied decision rules based on comprehensive financial metrics and risk assessment.")

        st.write("")
        st.write("⚖️ **COMPLIANCE AGENT**")
        st.write("Verified all regulatory requirements, generated compliance documentation, created audit trails, and ensured the decision meets all legal and compliance standards.")

        st.write("")
        st.write(f"**Final Decision:** {result.get('decision', 'N/A')}")
        st.write("All agents unanimously contributed to this decision based on the applicant's comprehensive profile and financial analysis.")

    else:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, rgba(79, 172, 254, 0.1) 0%, rgba(0, 242, 254, 0.05) 100%);
            backdrop-filter: blur(15px);
            padding: 60px;
            border-radius: 20px;
            text-align: center;
            color: #ffffff;
            font-size: 18px;
            border: 1.5px solid rgba(79, 172, 254, 0.2);
            margin: 40px 0;
        ">
            <p style="margin: 0; font-weight: 600; color: #4facfe; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">No Data Available</p>
            <p style="margin: 0; color: rgba(255, 255, 255, 0.7);">Submit an application to access export options and tools</p>
        </div>
        """, unsafe_allow_html=True)

# ===== FEATURE 11: PREDICTIVE TREND ANALYSIS =====
with tab7:
    st.markdown('<h3 style="color: #4facfe; font-size: 24px; text-transform: uppercase; letter-spacing: 1px;">Advanced Analytics</h3>', unsafe_allow_html=True)
    st.write("")

    app_history = st.session_state.get("application_history", {})
    total_apps = len(app_history)

    if total_apps > 5:
        # FEATURE 11: PREDICTIVE TREND ANALYSIS
        st.markdown('<h4 style="color: #4facfe;">📈 Approval Trends (Rolling Average)</h4>', unsafe_allow_html=True)

        apps_list = list(app_history.values())
        approvals_rolling = []
        app_numbers = []

        for i in range(len(apps_list)):
            window = apps_list[max(0, i-4):i+1]
            app_count = len(window)
            app_approved = sum(1 for a in window if a.get("decision") == "Approve")
            rate = (app_approved / app_count * 100) if app_count > 0 else 0
            approvals_rolling.append(rate)
            app_numbers.append(i + 1)

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=app_numbers,
            y=approvals_rolling,
            mode='lines+markers',
            name='Approval Rate',
            line=dict(color='#4facfe', width=3),
            marker=dict(size=8, color='#00f2fe')
        ))

        fig.update_layout(
            title="Approval Rate Trend (5-App Rolling Window)",
            xaxis_title="Application Number",
            yaxis_title="Approval Rate (%)",
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

        st.divider()
        st.write("")

        # FEATURE 13: APPLICANT SEGMENTATION
        st.markdown('<h4 style="color: #4facfe;">👥 Applicant Risk Segmentation</h4>', unsafe_allow_html=True)

        low_risk = sum(1 for a in app_history.values() if a.get("risk_score", 0) <= 30)
        medium_risk = sum(1 for a in app_history.values() if 30 < a.get("risk_score", 0) <= 60)
        high_risk = sum(1 for a in app_history.values() if a.get("risk_score", 0) > 60)

        col1, col2, col3 = st.columns(3, gap="medium")

        with col1:
            st.markdown(f"""
            <div class="metric-card-premium">
                <div class="metric-label-premium">Low Risk</div>
                <div class="metric-value-premium" style="color: #11998e;">{low_risk}</div>
                <div style="text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 12px; margin-top: 8px;">{(low_risk/total_apps*100):.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card-premium">
                <div class="metric-label-premium">Medium Risk</div>
                <div class="metric-value-premium" style="color: #ffd166;">{medium_risk}</div>
                <div style="text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 12px; margin-top: 8px;">{(medium_risk/total_apps*100):.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card-premium">
                <div class="metric-label-premium">High Risk</div>
                <div class="metric-value-premium" style="color: #eb3349;">{high_risk}</div>
                <div style="text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 12px; margin-top: 8px;">{(high_risk/total_apps*100):.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.write("")

        # Segmentation pie chart
        st.markdown('<h4 style="color: #4facfe;">Risk Distribution</h4>', unsafe_allow_html=True)

        seg_data = pd.DataFrame({
            'Risk Level': ['Low Risk', 'Medium Risk', 'High Risk'],
            'Count': [low_risk, medium_risk, high_risk]
        })

        fig_seg = px.pie(seg_data, values='Count', names='Risk Level',
                        color_discrete_sequence=['#11998e', '#ffd166', '#eb3349'],
                        height=400)
        fig_seg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white', size=12))
        st.plotly_chart(fig_seg, use_container_width=True)

        st.divider()
        st.write("")

        # FEATURE 14: DECISION EXPLANATION VIDEO SCRIPT
        st.markdown('<h4 style="color: #4facfe;">🎬 Generate Explanation Script</h4>', unsafe_allow_html=True)

        if "result" in st.session_state and st.session_state.result:
            result = st.session_state.result

            if st.button("Generate Speaking Points Script"):
                script = f"""LOAN DECISION EXPLANATION SCRIPT
{'='*50}

OPENING:
"Good day. We have reviewed the loan application and reached a decision."

MAIN DECISION POINT:
"The decision is {result.get('decision', 'UNKNOWN')} with a risk score of {result.get('risk_score', 0)} out of 100."

CONFIDENCE LEVEL:
"Our decision confidence level is {result.get('confidence', 0)}%, which indicates {'high confidence' if result.get('confidence', 0) >= 75 else 'moderate confidence' if result.get('confidence', 0) >= 50 else 'lower confidence'} in this decision."

KEY FACTORS ANALYSIS:
"This decision is based on the following key factors:"
"""

                for i, factor in enumerate(result.get('key_factors', []), 1):
                    script += f"\n  {i}. {factor}"

                script += f"""

DETAILED EXPLANATION:
"{result.get('explanation', 'N/A')}"

RISK ASSESSMENT:
"The risk score of {result.get('risk_score', 0)} indicates a {'low-risk' if result.get('risk_score', 0) <= 30 else 'moderate-risk' if result.get('risk_score', 0) <= 60 else 'high-risk'} profile."

CLOSING:
"Thank you for considering our decision. We will provide further details and next steps shortly. If you have any questions, please feel free to reach out."

{'='*50}
NOTES FOR PRESENTER:
- Speak clearly and maintain professional tone
- Allow time for questions after each section
- Have supporting documentation ready
- Emphasize key factors that led to this decision
"""

                st.text_area("📝 Speaking Script (Ready to Copy)", script, height=350)

    else:
        st.info("📊 Submit at least 6 applications to view advanced trend analysis and segmentation")

# ===== FEATURE 12: BATCH UPLOAD & FEATURE 15: MONTHLY REPORT =====
with tab8:
    st.markdown('<h3 style="color: #4facfe; font-size: 24px; text-transform: uppercase; letter-spacing: 1px;">Batch Processing & Reports</h3>', unsafe_allow_html=True)
    st.write("")

    # FEATURE 12: BATCH UPLOAD
    st.markdown('<h4 style="color: #4facfe;">📤 Batch Application Upload</h4>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload CSV file with applications", type=['csv'], key="batch_upload")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write(f"📋 Found {len(df)} applications to process")
            st.write("")

            # Show preview
            st.markdown('<h5 style="color: #4facfe;">Preview:</h5>', unsafe_allow_html=True)
            st.dataframe(df.head(), use_container_width=True)

            if st.button("🚀 Process All Applications"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                results_list = []

                for idx, row in df.iterrows():
                    try:
                        payload = {
                            "age": int(row.get("age", 35)),
                            "income": int(row.get("income", 100000)),
                            "employment": row.get("employment", "Salaried"),
                            "credit_score": int(row.get("credit_score", 720)),
                            "loan_amount": int(row.get("loan_amount", 250000)),
                            "tenure_months": int(row.get("tenure_months", 60)),
                            "liabilities": int(row.get("liabilities", 0)),
                            "location": row.get("location", "New York")
                        }

                        response = requests.post("http://127.0.0.1:8000/submit", json=payload, timeout=15)

                        if response.status_code == 200:
                            result = response.json()
                            app_id = result['application_id']
                            st.session_state.application_history[app_id] = {
                                "result": result['result'],
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "decision": result['result'].get('decision', 'Unknown'),
                                "risk_score": result['result'].get('risk_score', 0),
                                "confidence": result['result'].get('confidence', 0),
                                "age": int(row.get("age", 35)),
                                "income": int(row.get("income", 100000)),
                                "credit_score": int(row.get("credit_score", 720)),
                                "loan_amount": int(row.get("loan_amount", 250000)),
                                "liabilities": int(row.get("liabilities", 0))
                            }
                            results_list.append({"Row": idx + 1, "Decision": result['result'].get('decision', 'Unknown'), "Status": "✅ Success"})
                        else:
                            results_list.append({"Row": idx + 1, "Decision": "N/A", "Status": "❌ Failed"})

                    except Exception as e:
                        results_list.append({"Row": idx + 1, "Decision": "N/A", "Status": f"❌ Error: {str(e)[:30]}"})

                    progress_bar.progress((idx + 1) / len(df))
                    status_text.write(f"Processing: {idx + 1}/{len(df)}")

                st.success(f"✅ Batch processing complete! {len(df)} applications processed.")
                st.write("")

                results_df = pd.DataFrame(results_list)
                st.dataframe(results_df, use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Error reading CSV: {str(e)}")

    st.divider()
    st.write("")

    # FEATURE 15: MONTHLY PERFORMANCE REPORT
    st.markdown('<h4 style="color: #4facfe;">📊 Monthly Performance Report Generator</h4>', unsafe_allow_html=True)

    app_history = st.session_state.get("application_history", {})
    total_apps = len(app_history)

    if total_apps > 0:
        approved = sum(1 for a in app_history.values() if a.get("decision") == "Approve")
        rejected = sum(1 for a in app_history.values() if a.get("decision") == "Reject")
        under_review = sum(1 for a in app_history.values() if a.get("decision") == "Review")
        approval_rate = (approved / total_apps * 100) if total_apps > 0 else 0
        avg_risk = sum([a.get('risk_score', 0) for a in app_history.values()]) / max(1, total_apps)
        avg_confidence = sum([a.get('confidence', 0) for a in app_history.values()]) / max(1, total_apps)

        if st.button("Generate Monthly Report"):
            report = f"""LOAN APPROVAL SYSTEM - MONTHLY PERFORMANCE REPORT
{'='*70}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
System: Smart Loan Approval

EXECUTIVE SUMMARY
{'='*70}
Total Applications Processed: {total_apps}
Approved: {approved} ({(approved/total_apps*100):.1f}%)
Rejected: {rejected} ({(rejected/total_apps*100):.1f}%)
Under Review: {under_review} ({(under_review/total_apps*100):.1f}%)
Overall Approval Rate: {approval_rate:.1f}%

PERFORMANCE METRICS
{'='*70}
Average Risk Score: {avg_risk:.2f}/100
Average Decision Confidence: {avg_confidence:.1f}%
Low Risk Applicants: {sum(1 for a in app_history.values() if a.get('risk_score', 0) <= 30)}
Medium Risk Applicants: {sum(1 for a in app_history.values() if 30 < a.get('risk_score', 0) <= 60)}
High Risk Applicants: {sum(1 for a in app_history.values() if a.get('risk_score', 0) > 60)}

DECISION BREAKDOWN
{'='*70}"""

            for decision_type in ['Approve', 'Reject', 'Review']:
                count = sum(1 for a in app_history.values() if a.get('decision') == decision_type)
                percentage = (count / total_apps * 100) if total_apps > 0 else 0
                report += f"\n{decision_type}: {count} applications ({percentage:.1f}%)"

            report += f"""

KEY INSIGHTS
{'='*70}
1. System processed {total_apps} applications this period
2. Approval success rate is {approval_rate:.1f}%
3. Average decision confidence level is {avg_confidence:.1f}%
4. Risk assessment shows {'predominantly low-risk' if avg_risk <= 35 else 'balanced risk profile' if avg_risk <= 55 else 'higher risk applications'} portfolio
5. System performance indicates {'excellent' if approval_rate >= 70 else 'good' if approval_rate >= 50 else 'moderate'} approval accuracy

RECOMMENDATIONS
{'='*70}
1. Continue monitoring approval trends
2. Review all high-risk applications ({sum(1 for a in app_history.values() if a.get('risk_score', 0) > 60)} cases) manually
3. Update risk models if needed
4. Consider increasing approved loan amount if trends remain positive
5. Implement quarterly reviews of decision patterns

COMPLIANCE NOTES
{'='*70}
- All decisions logged with full audit trail
- Each application has unique Case ID for tracking
- Complete compliance documentation available
- Regular model validation recommended

{'='*70}
Report prepared by: Smart Loan Approval System
Multi-Agent Architecture
{'='*70}
"""

            st.text_area("📋 Monthly Report (Copy & Download)", report, height=400)

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="📥 Download as Text",
                    data=report,
                    file_name=f"monthly_report_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )
            with col2:
                st.download_button(
                    label="📋 Download as JSON",
                    data=json.dumps({
                        "report_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "total_applications": total_apps,
                        "approved": approved,
                        "rejected": rejected,
                        "under_review": under_review,
                        "approval_rate": approval_rate,
                        "average_risk_score": avg_risk,
                        "average_confidence": avg_confidence
                    }, indent=2),
                    file_name=f"monthly_report_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )

    else:
        st.info("📊 Submit applications to generate performance reports")

st.markdown("""
<div class="footer-premium">
    <p class="footer-text">🏦 Smart Loan Approval System</p>
    <p class="footer-text">Advanced Multi-Agent Architecture for Intelligent Decision Making</p>
</div>
""", unsafe_allow_html=True)
