# -*- coding: utf-8 -*-
import os
import time
import sys
import random
import socket
import subprocess
import re
from datetime import datetime, timezone, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import argparse

class TimeFunBuyer:
    def __init__(self, use_existing_session=True):
        load_dotenv(dotenv_path=".env.utf8")
        
        # Get TimeFun account information
        self.email = os.getenv('TIMEFUN_EMAIL')
        self.password = os.getenv('TIMEFUN_PASSWORD')
        
        # Buy settings
        try:
            self.buy_amount = float(os.getenv('BUY_AMOUNT', '10').strip())
            self.max_buy_attempts = int(os.getenv('MAX_BUY_ATTEMPTS', '3').strip())
            self.buy_delay = int(os.getenv('BUY_DELAY', '2').strip())
        except ValueError as e:
            print(f"Error parsing configuration: {e}")
            print("Please make sure your .env.utf8 file does not contain comments after values.")
            raise
        
        # Browser settings
        self.headless = os.getenv('HEADLESS', 'True').lower().strip() == 'true'
        self.use_existing_session = use_existing_session
        self.chrome_process = None
        self.setup_browser()
        
        # Login status
        self.is_logged_in = False
    
    def find_chrome_debugging_port(self):
        """Find an available port for Chrome debugging"""
        # Find an available port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()
        return port
    
    def is_chrome_running_with_debugging(self):
        """Check if Chrome is already running with remote debugging enabled"""
        # Common debugging ports
        common_ports = [9222, 9223, 9224, 9225, 9226, 9227, 9228, 9229, 9230]
        
        for port in common_ports:
            try:
                # Try to connect to the port
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1', port))
                sock.close()
                
                if result == 0:  # Port is open
                    # Try to access the Chrome DevTools JSON API
                    try:
                        import requests
                        response = requests.get(f"http://localhost:{port}/json/version", timeout=1)
                        if response.status_code == 200 and "Chrome" in response.text:
                            print(f"Found Chrome running with debugging on port {port}")
                            return port
                    except:
                        pass
            except:
                pass
        
        return None
    
    def setup_browser(self):
        """Connect to an already running Chrome instance or start a new one"""
        if self.use_existing_session:
            # First check if Chrome is already running with debugging
            debug_port = self.is_chrome_running_with_debugging()
            
            if debug_port is None:
                print("No Chrome instance with debugging found. Starting Chrome...")
                
                # Get Chrome executable path
                if os.name == 'nt':  # Windows
                    chrome_paths = [
                        os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Google\\Chrome\\Application\\chrome.exe'),
                        os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Google\\Chrome\\Application\\chrome.exe'),
                        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google\\Chrome\\Application\\chrome.exe')
                    ]
                    chrome_exe = next((path for path in chrome_paths if os.path.exists(path)), None)
                else:  # Linux/Mac
                    chrome_candidates = ['google-chrome', 'chrome', 'chromium', 'chromium-browser']
                    chrome_exe = next((c for c in chrome_candidates if subprocess.call(['which', c], stdout=subprocess.PIPE) == 0), None)
                
                # Get user data directory
                chrome_data_dir = os.getenv('CHROME_USER_DATA_DIR')
                if not chrome_data_dir:
                    # Default locations for Chrome user data
                    if os.name == 'nt':  # Windows
                        chrome_data_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')
                    else:  # Linux/Mac
                        chrome_data_dir = os.path.join(os.environ['HOME'], '.config', 'google-chrome')
                
                # Start Chrome with remote debugging
                cmd = f'"{chrome_exe}" --remote-debugging-port=9222 --user-data-dir="{chrome_data_dir}"'
                print(f"Starting Chrome with command: {cmd}")
                self.chrome_process = subprocess.Popen(cmd)
                
                # Wait for Chrome to start
                print("Waiting for Chrome to start...")
                time.sleep(5)
                
                # Try to find the debugging port again
                debug_port = self.is_chrome_running_with_debugging()
                if debug_port is None:
                    raise Exception("Failed to start Chrome with remote debugging")
            
            try:
                # Connect to the running Chrome instance
                chrome_options = Options()
                chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")
                
                # Path to Chrome driver
                driver_path = os.path.join(os.getcwd(), "drivers", "chromedriver.exe")
                
                # Check if driver exists
                if not os.path.exists(driver_path):
                    raise FileNotFoundError(f"Chrome driver not found at {driver_path}. Please download it from https://chromedriver.chromium.org/downloads")
                
                # Create service
                service = Service(driver_path)
                
                # Initialize the driver
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.wait = WebDriverWait(self.driver, 10)
                print("Successfully connected to Chrome session")
            except Exception as e:
                print(f"Failed to connect to Chrome session: {e}")
                raise
        else:
            # Standard setup for new browser instance
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Basic settings
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Add SSL-related options
            chrome_options.add_argument("--ignore-certificate-errors")
            chrome_options.add_argument("--ignore-ssl-errors")
            chrome_options.add_argument("--allow-insecure-localhost")
            chrome_options.add_argument("--disable-web-security")
            
            # Advanced settings to bypass Cloudflare
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            
            # Randomize user agent
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
            ]
            chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            # Path to Chrome driver
            driver_path = os.path.join(os.getcwd(), "drivers", "chromedriver.exe")
            
            # Check if driver exists
            if not os.path.exists(driver_path):
                raise FileNotFoundError(f"Chrome driver not found at {driver_path}. Please download it from https://chromedriver.chromium.org/downloads")
            
            # Create service
            service = Service(driver_path)
            
            # Initialize the driver
            try:
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                
                # Modify navigator properties to avoid detection
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                self.wait = WebDriverWait(self.driver, 10)
                print("Browser setup successful")
            except Exception as e:
                print(f"Failed to initialize browser: {e}")
                raise
    
    def is_element_present(self, by, value):
        """Check if an element is present on the page"""
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False
    
    def check_login_status(self):
        """Check if already logged in to TimeFun"""
        try:
            # Visit TimeFun homepage
            print("Navigating to TimeFun homepage...")
            self.driver.get("https://time.fun")
            time.sleep(5)  # Wait longer for page to load
            
            # Print current URL for debugging
            print(f"Current URL: {self.driver.current_url}")
            
            # Print page title for debugging
            print(f"Page title: {self.driver.title}")
            
            # Check for various login indicators
            login_indicators = [
                (By.XPATH, "//a[contains(@href, '/profile')]", "Profile link"),
                (By.XPATH, "//button[contains(text(), 'Disconnect')]", "Disconnect button"),
                (By.XPATH, "//div[contains(@class, 'avatar')]", "Avatar element"),
                (By.XPATH, "//a[contains(text(), 'Profile')]", "Profile text link")
            ]
            
            for by, value, name in login_indicators:
                if self.is_element_present(by, value):
                    print(f"Login indicator found: {name}")
                    self.is_logged_in = True
                    return True
            
            # Check if we're on the login page
            if self.is_element_present(By.ID, "email") or "login" in self.driver.current_url.lower():
                print("Not logged in, on login page")
                return False
            
            # Additional check: Try to access a page that requires login
            print("Checking access to a protected page...")
            self.driver.get("https://time.fun/home")
            time.sleep(3)
            
            # If we're redirected to login, we're not logged in
            if "login" in self.driver.current_url.lower():
                print("Redirected to login page, not logged in")
                return False
            
            # If we can access the home page, we're probably logged in
            if "home" in self.driver.current_url.lower():
                print("Successfully accessed home page, assuming logged in")
                self.is_logged_in = True
                return True
            
            # If we can't determine the status, assume not logged in
            print("Login status unknown, assuming not logged in")
            return False
        except Exception as e:
            print(f"Error checking login status: {e}")
            return False
    
    def login(self):
        """Login to TimeFun website or verify existing login"""
        # If using existing session, just check login status
        if self.use_existing_session:
            if self.check_login_status():
                return True
            
            print("Using existing session but not logged in")
            print("Please log in to TimeFun in the Chrome window")
            
            # Open login page
            self.driver.get("https://time.fun/login")
            
            # Wait for user to manually log in
            timeout = 300  # 5 minutes
            print(f"You have {timeout} seconds to log in manually")
            print("The script will continue once you're logged in")
            
            start_time = time.time()
            while time.time() - start_time < timeout:
                if self.check_login_status():
                    print("Login detected!")
                    self.is_logged_in = True
                    return True
                time.sleep(3)
            
            print("Login timeout. Please restart the script after logging in")
            return False
        
        # Standard login process for new browser instance
        if self.is_logged_in:
            return True
        
        try:
            print("Visiting TimeFun login page...")
            self.driver.get("https://time.fun/login")
            
            # Add a small delay to simulate human behavior
            time.sleep(random.uniform(1, 3))
            
            # Check if we need to handle Cloudflare
            if not self.is_element_present(By.ID, "email"):
                print("Cloudflare challenge detected")
                print("Please complete the Cloudflare verification manually")
                print("The script will wait until you complete it")
                
                # Wait for user to manually complete verification
                timeout = 300  # 5 minutes
                start_time = time.time()
                while time.time() - start_time < timeout:
                    if self.is_element_present(By.ID, "email"):
                        print("Cloudflare verification passed!")
                        break
                    time.sleep(3)
                else:
                    print("Cloudflare verification timeout")
                    return False
            
            # Wait for login page to load
            print("Waiting for login page to load...")
            self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            
            # Enter email with human-like typing
            print(f"Entering email: {self.email}")
            email_input = self.driver.find_element(By.ID, "email")
            email_input.clear()
            self.human_like_typing(email_input, self.email)
            
            # Add a small delay before clicking the button
            time.sleep(random.uniform(0.5, 1.5))
            
            # Click "Send Code" button
            print("Clicking Send Code button...")
            send_code_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Send Code')]")
            send_code_button.click()
            
            print(f"Verification code has been sent to: {self.email}")
            
            # Prompt user to enter verification code
            if self.headless:
                print("Warning: Cannot enter verification code in headless mode")
                print("Please run in non-headless mode")
                return False
            
            verification_code = input("Please check your email and enter the verification code: ")
            
            # Enter verification code with human-like typing
            print("Entering verification code...")
            code_input = self.driver.find_element(By.ID, "code")
            code_input.clear()
            self.human_like_typing(code_input, verification_code)
            
            # Add a small delay before clicking the button
            time.sleep(random.uniform(0.5, 1.5))
            
            # Click login button
            print("Clicking login button...")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
            login_button.click()
            
            # Wait for login success
            print("Waiting for login to complete...")
            self.wait.until(EC.url_contains("time.fun/home"))
            
            self.is_logged_in = True
            print("Login successful!")
            return True
        except Exception as e:
            print(f"Login failed: {e}")
            return False
    
    def human_like_typing(self, element, text):
        """Type text into an element with random delays to simulate human typing"""
        for character in text:
            element.send_keys(character)
            time.sleep(random.uniform(0.05, 0.2))  # Random delay between keystrokes
    
    def find_and_click_element(self, xpaths, description, timeout=10):
        """Find an element using multiple XPaths and click it"""
        print(f"Looking for {description}...")
        
        for xpath in xpaths:
            print(f"Trying XPath: {xpath}")
            try:
                # Use a shorter timeout for each attempt
                element = WebDriverWait(self.driver, timeout/len(xpaths)).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                print(f"Found {description} with XPath: {xpath}")
                element.click()
                print(f"Clicked {description}")
                return True
            except Exception as e:
                print(f"Failed to find/click with XPath {xpath}: {e}")
        
        print(f"Could not find {description} with any of the provided XPaths")
        return False
    
    def find_input_element(self, selectors, description, timeout=10):
        """Find an input element using multiple selectors"""
        print(f"Looking for {description}...")
        
        for selector_type, selector_value in selectors:
            print(f"Trying selector: {selector_type} = {selector_value}")
            try:
                # Use a shorter timeout for each attempt
                element = WebDriverWait(self.driver, timeout/len(selectors)).until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                print(f"Found {description} with selector: {selector_type} = {selector_value}")
                return element
            except Exception as e:
                print(f"Failed to find with selector {selector_type} = {selector_value}: {e}")
        
        print(f"Could not find {description} with any of the provided selectors")
        return None
    
    def buy_user(self, username):
        """Buy a specific user on TimeFun"""
        if not self.is_logged_in and not self.login():
            print("Not logged in, cannot perform buy operation")
            return False
        
        try:
            # Check for locally saved page
            local_path = os.path.join(os.getcwd(), f"{username}.html")
            if os.path.exists(local_path):
                print(f"Opening local page: {local_path}")
                self.driver.get(f"file:///{local_path}")
            else:
                # Visit online page
                user_market_url = f"https://time.fun/{username}?tab=market"
                print(f"Visiting user market page: {user_market_url}")
                self.driver.get(user_market_url)
            
            # Wait for page load
            time.sleep(random.uniform(2, 4))
            
            # Print debug info
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page title: {self.driver.title}")
            
            # Save page screenshot
            screenshot_path = f"debug_screenshot_{username}_before.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved: {screenshot_path}")
            
            # Find Buy button (using more general selectors)
            buy_button_xpaths = [
                # Most specific selectors
                "//button[contains(@class, 'inline-flex') and contains(@class, 'bg-controls-primary')]",
                "//button[contains(@class, 'bg-controls-primary')]",
                "//button[contains(@class, 'text-primary-100')]",
                # Class-based selectors
                "//button[contains(@class, 'primary')]",
                "//button[contains(@class, 'buy')]",
                # Text-based selectors
                "//button[text()='Buy']",
                "//button[contains(text(), 'Buy')]",
                # General button selectors
                "//button[contains(@class, 'rounded')]",
                "//div[contains(@class, 'market')]//button",
                # Most general selectors
                "//button"
            ]
            
            if not self.find_and_click_element(buy_button_xpaths, "Buy button"):
                print("Saving page source and screenshot for debugging...")
                page_source = self.driver.page_source
                with open(f"debug_page_source_{username}.html", "w", encoding="utf-8") as f:
                    f.write(page_source)
                print("Page source saved. Analyzing buttons on page...")
                
                # Print all buttons for debugging
                try:
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    print(f"Found {len(buttons)} buttons on page:")
                    for i, button in enumerate(buttons):
                        try:
                            print(f"Button {i+1}:")
                            print(f"Text: {button.text}")
                            print(f"Class: {button.get_attribute('class')}")
                            print(f"Type: {button.get_attribute('type')}")
                            print("---")
                        except:
                            pass
                except Exception as e:
                    print(f"Error analyzing buttons: {e}")
                
                print("Buy button not found after trying all selectors")
                return False
            
            # Wait for buy modal
            print("Waiting for buy modal to appear...")
            time.sleep(2)
            
            # Save modal screenshot
            screenshot_path = f"debug_screenshot_{username}_after_buy_click.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Modal screenshot saved: {screenshot_path}")
            
            # Try to switch to USD
            currency_switch_xpaths = [
                "//button[contains(text(), 'USD')]",
                "//button[contains(@class, 'currency-switch') and contains(text(), 'USD')]",
                "//div[contains(@class, 'modal')]//button[contains(text(), 'USD')]",
                "//div[contains(@class, 'modal')]//div[contains(@class, 'switch')]//button[last()]"
            ]
            
            print("Attempting to switch to USD...")
            self.find_and_click_element(currency_switch_xpaths, "USD switch button")
            time.sleep(1)  # Wait for switch to complete
            
            # Find amount input field
            amount_input_selectors = [
                (By.XPATH, "//div[contains(@class, 'modal')]//input[@type='number']"),
                (By.XPATH, "//input[@type='number']"),
                (By.XPATH, "//div[contains(@class, 'modal')]//input[contains(@class, 'amount')]"),
                (By.XPATH, "//div[contains(@class, 'modal')]//input"),
                (By.CSS_SELECTOR, "div.modal input[type='number']"),
                (By.CSS_SELECTOR, "input.amount"),
                (By.CSS_SELECTOR, "div.modal input")
            ]
            
            amount_input = self.find_input_element(amount_input_selectors, "amount input field")
            
            if not amount_input:
                print("Amount input field not found")
                return False
            
            # Enter buy amount
            print(f"Entering buy amount: {self.buy_amount} USDC")
            amount_input.clear()
            self.human_like_typing(amount_input, str(self.buy_amount))
            
            # Wait for input completion and button update
            print("Waiting for button to update with amount...")
            time.sleep(3)  # Wait longer for button text to update
            
            # Find first Buy button with amount
            print("Looking for initial Buy button...")
            try:
                buttons = self.driver.find_elements(By.TAG_NAME, "button")
                target_button = None
                print("Analyzing all buttons:")
                for button in buttons:
                    try:
                        text = button.text
                        print(f"Button text: {text}")
                        # Look for button that contains both "Buy" and "mins for $"
                        if "Buy" in text and "mins for $" in text:
                            target_button = button
                            print(f"Found matching button: {text}")
                            break
                    except:
                        continue
                
                if target_button:
                    print(f"Clicking initial Buy button with text: {target_button.text}")
                    target_button.click()
                    
                    # Wait for confirmation dialog
                    print("Waiting for confirmation dialog...")
                    time.sleep(2)
                    
                    # Look for Confirm & Buy button
                    print("Looking for Confirm & Buy button...")
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    confirm_button = None
                    for button in buttons:
                        try:
                            text = button.text
                            print(f"Confirm button text: {text}")
                            # Look for button that contains "Confirm & Buy" and "mins for $"
                            if "Confirm" in text and "Buy" in text and "mins for $" in text:
                                confirm_button = button
                                print(f"Found confirm button: {text}")
                                break
                        except:
                            continue
                    
                    if confirm_button:
                        print(f"Clicking final Confirm & Buy button: {confirm_button.text}")
                        confirm_button.click()
                    else:
                        print("Could not find Confirm & Buy button")
                        screenshot_path = f"debug_screenshot_{username}_no_confirm.png"
                        self.driver.save_screenshot(screenshot_path)
                        print(f"Debug screenshot saved: {screenshot_path}")
                        return False
                else:
                    print("Could not find initial Buy button")
                    screenshot_path = f"debug_screenshot_{username}_no_button.png"
                    self.driver.save_screenshot(screenshot_path)
                    print(f"Debug screenshot saved: {screenshot_path}")
                    return False
                
            except Exception as e:
                print(f"Error during buy process: {e}")
                return False
            
            # Wait for transaction
            print("Waiting for transaction to complete...")
            time.sleep(5)
            
            # Save final screenshot
            screenshot_path = f"debug_screenshot_{username}_final.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Final screenshot saved: {screenshot_path}")
            
            print(f"Successfully bought {username}'s time coin!")
            return True
            
        except Exception as e:
            print(f"Error during purchase: {e}")
            try:
                screenshot_path = f"error_screenshot_{username}.png"
                self.driver.save_screenshot(screenshot_path)
                print(f"Error screenshot saved: {screenshot_path}")
            except:
                pass
            return False
    
    def buy_with_retry(self, username):
        """Try to buy multiple times until success or max attempts reached"""
        # First check if user exists on time.fun
        if not self.check_user_exists(username):
            print(f"Cannot buy {username} as they don't exist on time.fun")
            return False
            
        for attempt in range(1, self.max_buy_attempts + 1):
            print(f"Attempting to buy {username} (Attempt {attempt}/{self.max_buy_attempts})")
            
            if self.buy_user(username):
                return True
            
            # If failed and still have attempts, wait a bit before retrying
            if attempt < self.max_buy_attempts:
                wait_time = self.buy_delay * 2
                print(f"Buy failed, retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        
        print(f"Max attempts reached, giving up on buying {username}")
        return False
    
    def close(self):
        """Close browser"""
        if hasattr(self, 'driver'):
            # Don't quit the driver, just close the current window
            # This keeps the Chrome instance running
            try:
                current_handles = self.driver.window_handles
                if len(current_handles) > 1:
                    # If there are multiple windows, close only the current one
                    self.driver.close()
                else:
                    # If this is the last window, just disconnect without closing
                    pass
                print("Disconnected from Chrome session (Chrome is still running)")
            except:
                # If something goes wrong, try to quit the driver
                try:
                    self.driver.quit()
                    print("Chrome session closed")
                except:
                    pass 
    
    def check_user_exists(self, username):
        """Check if a user exists on time.fun platform
        
        Args:
            username: Username to check
            
        Returns:
            bool: True if user exists, False otherwise
        """
        try:
            print(f"Checking if user '{username}' exists on time.fun...")
            # Visit user page
            user_url = f"https://time.fun/{username}"
            self.driver.get(user_url)
            time.sleep(3)  # Wait for page to load or redirect
            
            # Check current URL
            current_url = self.driver.current_url
            print(f"Current URL after check: {current_url}")
            
            # If redirected to explore page, user doesn't exist
            if "explore" in current_url or current_url == "https://time.fun/":
                print(f"User '{username}' does not exist on time.fun")
                return False
                
            # Check if we're on the user's page
            if username.lower() in current_url.lower():
                print(f"User '{username}' exists on time.fun")
                return True
                
            # Additional check for page content
            try:
                # Look for typical elements on user profile
                if self.is_element_present(By.XPATH, f"//h1[contains(text(), '{username}')]") or \
                   self.is_element_present(By.XPATH, "//button[contains(text(), 'Buy Time')]") or \
                   self.is_element_present(By.XPATH, "//div[contains(@class, 'profile')]"):
                    print(f"User '{username}' exists on time.fun (verified by page content)")
                    return True
            except:
                pass
                
            # Default to false if unsure
            print(f"Cannot verify if user '{username}' exists on time.fun")
            return False
            
        except Exception as e:
            print(f"Error checking if user exists: {e}")
            return False
    
    def extract_tweet_time(self, tweet, timezone_offset=8):
        """Extract the timestamp from a tweet and determine if it's recent
        
        Args:
            tweet: The tweet element
            timezone_offset: Hours offset from UTC (default: 8 for Beijing time)
            
        Returns:
            bool: True if the tweet is from the last minute, False otherwise
        """
        try:
            # Look for time element
            time_element = tweet.find_element(By.CSS_SELECTOR, "time")
            
            # Get the timestamp attribute
            timestamp = time_element.get_attribute("datetime")
            if timestamp:
                # Convert to datetime
                tweet_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                
                # Get current time in UTC
                current_time_utc = datetime.now(timezone.utc)
                
                # Calculate time difference in seconds (both in UTC for accurate comparison)
                time_diff = (current_time_utc - tweet_time).total_seconds()
                
                # Format times for logging, converting to local time for better readability
                local_tweet_time = tweet_time + timedelta(hours=timezone_offset)
                local_current_time = current_time_utc + timedelta(hours=timezone_offset)
                
                print(f"Tweet timestamp: {local_tweet_time} (beijing), Current time: {local_current_time} (beijing)")
                print(f"Time difference: {time_diff:.0f} seconds ago")
                
                # Check if it's within the last minute (60 seconds)
                # This calculation is timezone-independent because we're comparing UTC timestamps
                return time_diff <= 60
            
            # If no timestamp attribute, check the text
            relative_time = time_element.text.lower()
            print(f"Tweet relative time: {relative_time}")
            
            # Check common recent time indicators
            recent_indicators = ["just now", "now", "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", 
                                "10s", "20s", "30s", "40s", "50s", "s ago", "just", "刚刚", "秒前"]
            
            for indicator in recent_indicators:
                if indicator in relative_time:
                    print(f"Tweet is recent based on text indicator: {relative_time}")
                    return True
                    
            # If it mentions minutes, check if it's under 1m
            if "m" in relative_time or "min" in relative_time:
                for num in range(2, 60):  # Checking for "2m", "3m", etc.
                    if f"{num}m" in relative_time or f"{num} m" in relative_time or f"{num} min" in relative_time:
                        return False
                
                # If it's "1m" or "1 min", it might be just crossing over the 1-minute threshold
                # Conservatively treat it as recent
                if "1m" in relative_time or "1 min" in relative_time:
                    print("Tweet is from 1 minute ago, considering it recent")
                    return True
            
            # By default, consider it not recent if we can't determine
            return False
                
        except Exception as e:
            print(f"Error extracting tweet time: {e}")
            # If we can't determine the time, default to not recent
            return False
    
    def monitor_tweets(self, username, continuous_monitoring=False, check_interval=30, timezone_offset=8, max_tweets_to_check=5):
        """Monitor tweets of specified user
        
        Args:
            username: Twitter username to monitor
            continuous_monitoring: Whether to continuously monitor (default: False)
            check_interval: Time between checks in seconds (default: 30)
            timezone_offset: Hours offset from UTC (default: 8 for Beijing time)
            max_tweets_to_check: Maximum number of tweets to check each time (default: 5)
        """
        last_tweet_id = None
        processed_tweets = set()  # Track processed tweet IDs
        
        while True:
            try:
                print(f"Starting to monitor @{username}'s tweets...")
                
                # Visit user profile
                url = f"https://x.com/{username}"
                self.driver.get(url)
                time.sleep(5)  # Wait for page load
                
                # Wait for tweets to load
                tweet_selector = "article[data-testid='tweet']"
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, tweet_selector))
                )
                
                # Get all tweets
                all_tweets = self.driver.find_elements(By.CSS_SELECTOR, tweet_selector)
                print(f"Found {len(all_tweets)} tweets on the page")
                
                # Limit to checking only the most recent tweets
                tweets = all_tweets[:max_tweets_to_check] if max_tweets_to_check < len(all_tweets) else all_tweets
                print(f"Checking the {len(tweets)} most recent tweets")
                
                if tweets:
                    found_recent_tweet = False
                    for tweet in tweets:
                        try:
                            # Get tweet ID
                            tweet_id = tweet.get_attribute("data-tweet-id")
                            if tweet_id in processed_tweets:
                                continue
                            
                            # Check if the tweet is recent (within the last minute)
                            if not self.extract_tweet_time(tweet, timezone_offset):
                                print("Skipping tweet - not from the last minute")
                                processed_tweets.add(tweet_id)  # Still mark as processed
                                continue
                                
                            found_recent_tweet = True
                            print("Found recent tweet (within last minute), processing...")
                            
                            # Get tweet text
                            tweet_text = tweet.find_element(By.CSS_SELECTOR, "[data-testid='tweetText']").text
                            print(f"New tweet content: {tweet_text}")
                            
                            # Check if it's a retweet
                            is_retweet = False
                            try:
                                retweet_indicator = tweet.find_element(By.XPATH, 
                                    ".//span[contains(text(), 'Retweeted') or contains(text(), '转发') or contains(text(), 'reposted')]")
                                is_retweet = True
                                print("This is a retweet")
                            except:
                                print("This is an original tweet")
                            
                            # Extract usernames
                            usernames = self.extract_usernames(tweet_text)
                            if usernames:
                                print(f"Extracted usernames: {usernames}")
                                
                                # Try to buy for each username
                                for username_to_buy in usernames:
                                    print(f"Attempting to buy for user: {username_to_buy}")
                                    try:
                                        # First check if user exists on time.fun
                                        if not self.check_user_exists(username_to_buy):
                                            print(f"Skipping {username_to_buy} as they don't exist on time.fun")
                                            continue
                                            
                                        # Use our own buy method directly
                                        success = self.buy_with_retry(username_to_buy)
                                        if success:
                                            print(f"Successfully bought for user: {username_to_buy}")
                                        else:
                                            print(f"Failed to buy for user: {username_to_buy}")
                                    except Exception as e:
                                        print(f"Error buying for user {username_to_buy}: {str(e)}")
                            else:
                                print("No usernames found in tweet")
                                
                            # Mark tweet as processed
                            processed_tweets.add(tweet_id)
                            
                        except Exception as e:
                            print(f"Error processing tweet: {str(e)}")
                            continue
                    
                    if not found_recent_tweet:
                        print("No recent tweets found within the last minute")
                else:
                    print("No tweets found")
                
                if not continuous_monitoring:
                    break
                    
                # Wait before next check
                print(f"Waiting {check_interval} seconds before next check...")
                time.sleep(check_interval)
                
            except Exception as e:
                print(f"Error monitoring tweets: {str(e)}")
                self.save_debug_info("monitor_tweets_error")
                if not continuous_monitoring:
                    break
                time.sleep(check_interval)  # Wait before retrying
                
    def extract_usernames(self, text):
        """Extract usernames from text"""
        # Match @username format
        pattern = r'@(\w+)'
        usernames = re.findall(pattern, text)
        return usernames 

    def save_debug_info(self, prefix):
        """Save debug information including screenshot and page source"""
        try:
            # Save screenshot
            screenshot_path = f"debug_{prefix}_screenshot.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"Debug screenshot saved: {screenshot_path}")
            
            # Save page source
            page_source_path = f"debug_{prefix}_page_source.html"
            with open(page_source_path, "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            print(f"Debug page source saved: {page_source_path}")
        except Exception as e:
            print(f"Error saving debug info: {str(e)}")

def run_monitor(twitter_username="timedotfun", check_interval=30, skip_login_check=True, timezone_offset=8, max_tweets=5):
    """Run the TimeFun Sniper Bot to monitor Twitter and auto-buy
    
    Args:
        twitter_username: Twitter username to monitor (default: timedotfun)
        check_interval: Time between checks in seconds (default: 30)
        skip_login_check: Skip login verification (default: True)
        timezone_offset: Hours offset from UTC (default: 8 for Beijing time)
        max_tweets: Maximum number of tweets to check each time (default: 5)
    """
    print(f"=== TimeFun Sniper Bot ===")
    print(f"Initializing bot to monitor @{twitter_username} tweets and auto-buy...")
    print(f"Check interval: {check_interval} seconds")
    print(f"Timezone: UTC+{timezone_offset} (offset from UTC)")
    print(f"Checking max {max_tweets} recent tweets each time")
    
    # Initialize the buyer
    buyer = TimeFunBuyer(use_existing_session=True)
    
    try:
        # Check login status only if explicitly requested
        if not skip_login_check:
            print("Checking login status...")
            if not buyer.check_login_status():
                print("Not logged in to TimeFun.")
                print("Please log in to TimeFun in your Chrome browser, then restart the bot.")
                return
            print("Login verified. Starting Twitter monitoring...")
        else:
            print("Skipping login check. Starting Twitter monitoring...")
            buyer.is_logged_in = True
        
        # Start monitoring tweets
        buyer.monitor_tweets(twitter_username, continuous_monitoring=True, 
                           check_interval=check_interval, timezone_offset=timezone_offset,
                           max_tweets_to_check=max_tweets)
        
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
    except Exception as e:
        print(f"Error running bot: {e}")
        buyer.save_debug_info("bot_error")
    finally:
        print("Closing browser session...")
        buyer.close()

if __name__ == "__main__":
    # Load environment variables
    load_dotenv(dotenv_path=".env.utf8")
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="TimeFun Sniper Bot")
    parser.add_argument("--username", "-u", default="timedotfun", 
                        help="Twitter username to monitor (default: timedotfun)")
    parser.add_argument("--interval", "-i", type=int, default=30,
                        help="Check interval in seconds (default: 30)")
    parser.add_argument("--check-login", "-c", action="store_true",
                        help="Force login check (default: login check is skipped)")
    parser.add_argument("--timezone", "-t", type=int, default=8,
                        help="Timezone offset from UTC in hours (default: 8 for Beijing)")
    parser.add_argument("--max-tweets", "-m", type=int, default=5,
                        help="Maximum number of tweets to check (default: 5)")
    parser.add_argument("--buy", "-b", metavar="TIMEFUN_USERNAME",
                        help="Directly buy a specific user without monitoring")
    parser.add_argument("--verify", "-v", metavar="TIMEFUN_USERNAME",
                        help="Verify if a user exists on time.fun without buying")
    
    args = parser.parse_args()
    
    # Run in verification-only mode if specified
    if args.verify:
        buyer = TimeFunBuyer(use_existing_session=True)
        try:
            exists = buyer.check_user_exists(args.verify)
            print(f"User '{args.verify}' {'exists' if exists else 'does not exist'} on time.fun")
        finally:
            buyer.close()
    # Run in buy-only mode if specified
    elif args.buy:
        buyer = TimeFunBuyer(use_existing_session=True)
        try:
            if args.check_login and not buyer.check_login_status():
                print("Not logged in to TimeFun. Please log in and try again.")
                sys.exit(1)
            else:
                # Skip login check by default
                buyer.is_logged_in = True
            
            print(f"Attempting to buy user: {args.buy}")
            success = buyer.buy_with_retry(args.buy)
            if success:
                print(f"Successfully bought {args.buy}'s time coin!")
            else:
                print(f"Failed to buy {args.buy}")
        finally:
            buyer.close()
    else:
        # Run in monitor mode
        run_monitor(args.username, args.interval, not args.check_login, 
                  args.timezone, args.max_tweets) 