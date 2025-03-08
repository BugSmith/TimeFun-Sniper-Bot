# -*- coding: utf-8 -*-
import os
import time
import sys
import random
import json
import socket
import subprocess
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

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
        self.chrome_process = None  # We don't start Chrome, so no process to track
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