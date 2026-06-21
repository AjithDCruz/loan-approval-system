# System Architecture

## Components

### 1. Agents (Claude Haiku 4.5)

**Applicant Profile Agent**
- Analyzes: Age, Income, Employment Type
- Returns: Income Stability Score, Employment Risk, Flags

**Financial Risk Agent**
- Analyzes: Credit Score, Loan Amount, Liabilities, DTI
- Returns: DTI Risk, Credit Risk, Loan Risk, Anomalies

**Loan Decision Agent**
- Synthesizes: Profile + Financial Analysis
- Rules: CS>700=good, DTI<0.43=good, Income>70=positive
- Returns: Approval Decision, Risk Score, Confidence, Explanation

**Compliance Agent**
- Generates: Notifications, Audit Records
- Returns: Action Taken, Case ID, Compliance Summary

### 2. Backend (FastAPI)

Endpoints:
- `POST /submit` - Submit loan application
- `GET /app/{app_id}` - Retrieve application status
- `GET /apps` - List all applications

### 3. Frontend (Streamlit)

Three tabs:
1. **Submit Application** - Form input interface
2. **View Results** - Decision display
3. **Audit Trail** - JSON audit log

### 4. Orchestration Engine

Workflow:
```
User Input → FastAPI → Orchestration Engine
    ↓
    Agent 1: Profile Analysis
    ↓
    Agent 2: Financial Risk
    ↓
    Agent 3: Loan Decision
    ↓
    Agent 4: Compliance
    ↓
Decision → UI Display
```

## Technology Stack

- **Language**: Python 3.10+
- **API Framework**: FastAPI
- **UI Framework**: Streamlit
- **AI Model**: Claude Haiku 4.5
- **SDK**: Anthropic Python SDK
- **HTTP Server**: Uvicorn

## Data Flow

1. User submits application via Streamlit UI
2. Request sent to FastAPI /submit endpoint
3. Orchestration engine invokes agents sequentially
4. Each agent analyzes using Claude Haiku 4.5
5. Final decision synthesized and returned
6. Results displayed in Streamlit UI
7. Full audit trail logged in-memory
