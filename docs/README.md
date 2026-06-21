# Agentic AI Loan Approval System

## Using Claude Haiku 4.5

### Quick Start

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
python -m app.main  # Terminal 1
streamlit run ui/streamlit_app.py  # Terminal 2
```

Visit: http://localhost:8501

### System Architecture

- 4 AI Agents: Using Claude Haiku 4.5
- Backend: FastAPI (port 8000)
- Frontend: Streamlit (port 8501)
- Orchestration: Multi-agent workflow
- Database: In-memory storage

### Features

- Multi-agent loan evaluation
- Explainable decisions
- Risk scoring
- Audit trail logging
- Production-ready code
- Optimized with Haiku 4.5

### Agents

1. **Applicant Profile Agent** - Analyzes age, income, employment
2. **Financial Risk Agent** - Evaluates credit score, DTI, liabilities
3. **Loan Decision Agent** - Synthesizes analysis into decision
4. **Compliance Agent** - Generates notifications and audit records
