# -*- coding: utf-8 -*-
import sys
import os
from timefun_buyer_en import TimeFunBuyer
from dotenv import load_dotenv
import time

def setup_instructions():
    """Display setup instructions for the user"""
    print("=== TimeFun Sniper Bot - Test Setup Instructions ===")
    print("This test connects to your already running Chrome browser.")
    print("Before running this test, please:")
    print("1. Start Chrome with remote debugging enabled using the command:")
    print('   "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222')
    print("2. Navigate to https://time.fun and log in")
    print("3. Keep Chrome open and running")
    print("\nThe test will connect to your Chrome session and attempt to buy the specified user.")
    
    response = input("Have you completed these steps? (y/n): ")
    return response.lower() == 'y'

def test_buy(username, skip_login_check=False):
    """Test buying a specific user"""
    print(f"=== Testing buy for user: {username} ===")
    
    # Initialize buyer module to connect to existing Chrome
    try:
        print("Connecting to Chrome...")
        buyer = TimeFunBuyer(use_existing_session=True)
    except Exception as e:
        print(f"Failed to connect to Chrome: {e}")
        print("Make sure Chrome is running with remote debugging enabled (--remote-debugging-port=9222)")
        return False
    
    try:
        # Check if already logged in
        if not skip_login_check:
            print("Checking login status...")
            if not buyer.check_login_status():
                print("Not logged in to TimeFun.")
                print("Please log in to TimeFun in your Chrome browser, then restart the test.")
                return False
            
            print("Successfully connected to Chrome and verified login")
        else:
            print("Skipping login check as requested")
            buyer.is_logged_in = True  # Force login status to true
            print("Assuming you are already logged in")
        
        # Try to buy
        success = buyer.buy_with_retry(username)
        
        if success:
            print(f"Test successful: Successfully bought {username}'s time coin!")
        else:
            print(f"Test failed: Failed to buy {username}")
        
        return success
    except Exception as e:
        print(f"Error during test: {e}")
        return False
    finally:
        # Disconnect from Chrome (but don't close it)
        buyer.close()

def test_monitor_tweets():
    buyer = TimeFunBuyer()
    try:
        # Test monitoring @LinqinEth's tweets
        print("Starting to monitor @LinqinEth's tweets...")
        buyer.monitor_tweets("LinqinEth")
    except Exception as e:
        print(f"Error during monitoring: {str(e)}")
    finally:
        buyer.close()

if __name__ == "__main__":
    # Load environment variables from .env.utf8
    load_dotenv(dotenv_path=".env.utf8")
    
    # Run Twitter monitoring test
    test_monitor_tweets() 