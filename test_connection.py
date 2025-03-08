# -*- coding: utf-8 -*-
import os
import sys
import requests

def test_connection():
    """Test network connection to time.fun"""
    print("Testing network connection to time.fun...")
    
    try:
        # Disable SSL verification for testing
        response = requests.get("https://time.fun", verify=False, timeout=10)
        
        # Print status code and response
        print(f"Status code: {response.status_code}")
        print(f"Response length: {len(response.text)} bytes")
        
        if response.status_code == 200:
            print("Connection successful!")
            return True
        else:
            print(f"Connection failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False

if __name__ == "__main__":
    # Disable SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    success = test_connection()
    sys.exit(0 if success else 1) 