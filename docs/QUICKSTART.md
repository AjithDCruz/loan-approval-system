# Quick Start (5 Minutes)

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set API Key

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

## 3. Start API Server

Terminal 1:
```bash
python -m app.main
```

Wait for: Uvicorn running on http://127.0.0.1:8000

## 4. Start Streamlit UI

Terminal 2:
```bash
streamlit run ui/streamlit_app.py
```

Browser opens at: http://localhost:8501

## 5. Test the System

- Fill form: Age 35, Income 120k, Credit 750, Loan 300k
- Click Submit
- See decision: APPROVED

## Testing with curl

```bash
curl -X POST http://127.0.0.1:8000/submit \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "income": 120000,
    "employment": "Salaried",
    "credit_score": 750,
    "loan_amount": 300000,
    "tenure_months": 60,
    "liabilities": 50000,
    "location": "New York"
  }'
```
