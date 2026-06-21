#!/usr/bin/env python3
import requests
import json
import time

# Test data
test_app = {
    "age": 35,
    "income": 120000,
    "employment": "Salaried",
    "credit_score": 750,
    "loan_amount": 300000,
    "tenure_months": 60,
    "liabilities": 50000,
    "location": "New York"
}

print("Testing Loan Approval System API...")
print("=" * 60)

# Start API in background
import subprocess
import os

os.chdir("/home/ubuntu/Documents/Loan_Approval_System")

# Kill any existing processes
os.system("pkill -f 'python -m app.main' 2>/dev/null")
time.sleep(1)

# Start API
print("\n1. Starting API server...")
api_process = subprocess.Popen(
    ["bash", "-c", "source venv/bin/activate && python -m app.main"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Wait for server to start
time.sleep(3)

print("✓ API server started")

try:
    # Test API endpoint
    print("\n2. Testing /submit endpoint...")
    response = requests.post(
        "http://127.0.0.1:8000/submit",
        json=test_app,
        timeout=15
    )
    
    print(f"Response Status: {response.status_code}")
    result = response.json()
    
    print("\n3. Decision Result:")
    print("-" * 60)
    print(json.dumps(result, indent=2))
    
    if response.status_code == 200:
        print("\n✅ API TEST PASSED")
        print(f"Decision: {result['result']['decision']}")
        print(f"Risk Score: {result['result']['risk_score']}/100")
        print(f"Confidence: {result['result']['confidence']}%")
    else:
        print(f"\n❌ API ERROR: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Could not connect to API on http://127.0.0.1:8000")
    print("Make sure the API server is running!")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    # Kill the process
    api_process.terminate()
    print("\nAPI server stopped.")
