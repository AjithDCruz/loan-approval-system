#!/bin/bash
cd /home/ubuntu/Documents/Loan_Approval_System
source venv/bin/activate
export ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-"your-api-key"}

echo "=========================================="
echo "Loan Approval System - Starting Servers"
echo "=========================================="
echo ""
echo "API Server starting on http://127.0.0.1:8000"
echo "Streamlit UI starting on http://localhost:8501"
echo ""
echo "To access from your local computer, use:"
echo "  ssh -i your-key.pem -L 8501:127.0.0.1:8501 ubuntu@your-instance-ip"
echo ""
echo "Then open: http://localhost:8501"
echo "=========================================="
echo ""

# Start API server in background
python -m app.main &
API_PID=$!
sleep 3

# Start Streamlit in foreground (so we can see logs)
streamlit run ui/streamlit_app.py
