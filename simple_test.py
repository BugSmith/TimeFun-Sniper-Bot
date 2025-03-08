# -*- coding: utf-8 -*-
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def main():
    print("Starting simple test...")
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 添加SSL相关选项
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    chrome_options.add_argument("--allow-insecure-localhost")
    chrome_options.add_argument("--disable-web-security")
    
    try:
        # Create drivers directory if it doesn't exist
        if not os.path.exists("drivers"):
            os.makedirs("drivers")
        
        # Path to Chrome driver
        driver_path = os.path.join(os.getcwd(), "drivers", "chromedriver.exe")
        
        # Check if driver exists
        if not os.path.exists(driver_path):
            print(f"Chrome driver not found at {driver_path}")
            print("Please download the appropriate Chrome driver from:")
            print("https://chromedriver.chromium.org/downloads")
            print("and place it in the 'drivers' folder.")
            return False
        
        # Setup Chrome driver
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Visit time.fun
        print("Visiting time.fun...")
        driver.get("https://time.fun")
        
        # Get title
        title = driver.title
        print(f"Page title: {title}")
        
        # Close browser
        driver.quit()
        print("Test completed successfully!")
        return True
    except Exception as e:
        print(f"Error during test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 