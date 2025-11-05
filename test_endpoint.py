#!/usr/bin/env python3
"""
Test the Flask endpoint directly
"""

import requests
import time

# Wait a moment for the server to be ready
time.sleep(2)

try:
    # Test the acne query
    response = requests.post(
        'http://localhost:8080/get',
        data={'msg': 'what is acne?'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"Error testing endpoint: {e}")