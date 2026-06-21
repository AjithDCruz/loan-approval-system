# How to Run Your Loan Approval System

## Step-by-Step Instructions

### IMPORTANT: You're on AWS (Remote Server)
Since you're on a remote AWS instance, you cannot directly access `http://localhost:8501` from your local browser. You have two options:

## Option 1: SSH Tunneling (Recommended)

On your **local computer**:

```bash
ssh -i your-key.pem -L 8501:127.0.0.1:8501 ubuntu@your-instance-ip
```

Replace:
- `your-key.pem` with your AWS key
- `your-instance-ip` with your instance's IP

Then open: `http://localhost:8501`

## Option 2: Port Forwarding

On your **local computer**:

```bash
ssh -i your-key.pem -L 8000:127.0.0.1:8000 -L 8501:127.0.0.1:8501 ubuntu@your-instance-ip
```

Then open:
- API: `http://localhost:8000`
- UI: `http://localhost:8501`

## Option 3: Public IP Access

If your AWS security group allows:

1. Get your instance public IP
2. Allow traffic on ports 8000 and 8501 in Security Group
3. Start servers on 0.0.0.0 instead of 127.0.0.1

Edit `app/config.py`:
```python
FASTAPI_HOST = "0.0.0.0"  # Instead of 127.0.0.1
```

Start API:
```bash
source venv/bin/activate
export ANTHROPIC_API_KEY="your-key"
python -m app.main
```

Then access: `http://your-public-ip:8000` or `http://your-public-ip:8501`

## On Your AWS Instance

### Terminal 1 - Start API Server:
```bash
cd /home/ubuntu/Documents/Loan_Approval_System
source venv/bin/activate
export ANTHROPIC_API_KEY="your-api-key-here"
python -m app.main
```

Should show:
```
Starting Loan Approval API (Claude Haiku 4.5)...
API running on http://127.0.0.1:8000
INFO: Uvicorn running on http://127.0.0.1:8000
```

### Terminal 2 - Start Streamlit UI:
```bash
cd /home/ubuntu/Documents/Loan_Approval_System
source venv/bin/activate
streamlit run ui/streamlit_app.py
```

Should show:
```
You can now view your Streamlit app in your browser.

  URL: http://localhost:8501
```

## Testing via Command Line (No Browser Needed)

Use curl to test the API directly on the instance:

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

Expected Response:
```json
{
  "application_id": "...",
  "status": "processed",
  "result": {
    "decision": "Approve",
    "risk_score": 45,
    "confidence": 85,
    ...
  }
}
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>
```

### API Key Not Set
```bash
# Verify it's set
echo $ANTHROPIC_API_KEY

# If empty, set it
export ANTHROPIC_API_KEY="your-actual-api-key"
```

### Connection Refused
- Make sure both servers started without errors
- Check firewall/security groups
- Verify ports are not blocked

---

**Which option would you prefer to use?**
