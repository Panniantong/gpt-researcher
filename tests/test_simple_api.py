"""
Simple test script to verify the API is working
"""

import requests
import json

# Test the simple research API
url = "http://localhost:8000/api/research"
payload = {
    "task": "What are the main benefits of solar energy?"
}

print("Testing /api/research endpoint...")
print(f"Request payload: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(url, json=payload)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Status: {data.get('status')}")
        print(f"Report length: {len(data.get('report', ''))} characters")
        print(f"\nFirst 500 characters of report:")
        print(data.get('report', '')[:500] + "...")
        
        if data.get('research_costs'):
            print(f"\nResearch costs: {data['research_costs']}")
    else:
        print(f"Error: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to server. Make sure it's running:")
    print("   python -m uvicorn backend.server.server:app --reload")
except Exception as e:
    print(f"❌ Error: {str(e)}")