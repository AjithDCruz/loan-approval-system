#!/bin/bash
echo "Starting Loan Approval System (Claude Haiku 4.5)..."
echo ""
echo "Starting API server on port 8000..."
python -m app.main &
sleep 2
echo ""
echo "Starting Streamlit UI on port 8501..."
streamlit run ui/streamlit_app.py
