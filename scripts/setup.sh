#!/bin/bash
echo "Installing Loan Approval System..."
pip install -r requirements.txt
echo "Installation complete!"
echo "Next steps:"
echo "1. export ANTHROPIC_API_KEY='your-key'"
echo "2. python -m app.main (Terminal 1)"
echo "3. streamlit run ui/streamlit_app.py (Terminal 2)"
