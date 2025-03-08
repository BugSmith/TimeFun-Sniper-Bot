# -*- coding: utf-8 -*-
import os
import time
import signal
import sys
from twitter_monitor import TwitterMonitor
from timefun_buyer_en import TimeFunBuyer
from dotenv import load_dotenv

def signal_handler(sig, frame):
    """Handle Ctrl+C signal to exit gracefully"""
    print("\nExiting program...")
    if 'buyer' in globals() and buyer is not None:
        buyer.close()
    sys.exit(0)

def handle_new_promotion(username):
    """Handle newly discovered promoted users"""
    print(f"Processing new promoted user: {username}")
    
    # Try to buy the user
    success = buyer.buy_with_retry(username)
    
    if success:
        print(f"Successfully bought {username}'s time coin!")
    else:
        print(f"Failed to buy {username}")

def setup_instructions():
    """Display setup instructions for the user"""
    print("=== TimeFun Sniper Bot - Setup Instructions ===")
    print("This bot connects to your already running Chrome browser.")
    print("Before running this bot, please:")
    print("1. Start Chrome with remote debugging enabled using the command:")
    print('   "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222')
    print("2. Navigate to https://time.fun and log in")
    print("3. Keep Chrome open and running")
    print("\nThe bot will connect to your Chrome session and monitor Twitter for new promotions.")
    
    response = input("Have you completed these steps? (y/n): ")
    return response.lower() == 'y'

if __name__ == "__main__":
    # Load environment variables
    load_dotenv(dotenv_path=".env.utf8")
    
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    print("=== TimeFun Sniper Bot ===")
    
    # Check if we should skip login check
    skip_login_check = "--skip-login-check" in sys.argv
    if skip_login_check:
        print("Login check will be skipped as requested")
    
    # Show setup instructions
    if not setup_instructions():
        print("Program cancelled. Please start Chrome with remote debugging and try again.")
        sys.exit(0)
    
    print("Initializing...")
    
    # Initialize buyer module to connect to existing Chrome
    try:
        print("Connecting to Chrome...")
        buyer = TimeFunBuyer(use_existing_session=True)
    except Exception as e:
        print(f"Failed to connect to Chrome: {e}")
        print("Make sure Chrome is running with remote debugging enabled (--remote-debugging-port=9222)")
        sys.exit(1)
    
    # Check if already logged in
    if not skip_login_check:
        print("Checking login status...")
        if not buyer.check_login_status():
            print("Not logged in to TimeFun.")
            print("Please log in to TimeFun in your Chrome browser, then restart the program.")
            buyer.close()
            sys.exit(1)
        
        print("Successfully connected to Chrome and verified login")
    else:
        print("Skipping login check as requested")
        buyer.is_logged_in = True  # Force login status to true
        print("Assuming you are already logged in")
    
    # Initialize Twitter monitor module
    monitor = TwitterMonitor()
    
    print("Initialization complete, starting monitoring...")
    
    try:
        # Start monitoring Twitter
        monitor.monitor(handle_new_promotion)
    except Exception as e:
        print(f"Error during program execution: {e}")
    finally:
        # Disconnect from Chrome (but don't close it)
        if 'buyer' in locals() and buyer is not None:
            buyer.close() 