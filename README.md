# TimeFun Sniper Bot

[![en](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![cn](https://img.shields.io/badge/语言-中文-red.svg)](README_CN.md)

This is a bot that monitors Twitter and automatically buys time coins on the time.fun website.

> **Development Status**: [COMPLETE] Auto-buying functionality is complete and tested successfully. [COMPLETE] Twitter monitoring functionality is complete.

## Features

- Monitors @timedotfun Twitter account for retweets
- Automatically identifies promoted usernames
- Automatically buys time coins for the promoted users on time.fun
- Connects to your existing Chrome session to avoid Cloudflare detection
- Supports two-step purchase confirmation process

## [SAFE]Security Notice

**IMPORTANT:** This bot requires access to your Chrome browser and TimeFun account. Please review the following security considerations:

- The bot connects to your Chrome browser with remote debugging enabled, which could potentially expose your browser to other applications
- Your Chrome user data directory contains sensitive information including cookies and saved passwords
- The `.env.utf8` file contains configuration settings
- Never share your `.env.utf8` file, debug screenshots, or Chrome user data directory
- Review the code before running it to ensure it meets your security requirements

## Installation

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env.utf8` file with the necessary configuration (see Configuration section)

## Configuration

Configure the following in your `.env.utf8` file (note: do not add comments after values as this may cause parsing errors):

```
# Buy settings
BUY_AMOUNT=2
MAX_BUY_ATTEMPTS=3
BUY_DELAY=2

# Monitor settings
CHECK_INTERVAL=60
HEADLESS=False

# Chrome settings
# IMPORTANT: You MUST set this to your Chrome user data directory
CHROME_USER_DATA_DIR=C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data
```

### Chrome User Data Directory

The `CHROME_USER_DATA_DIR` setting is **required** and must point to your Chrome user data directory:

- **Windows:** Usually `C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data`
- **Mac:** Usually `~/Library/Application Support/Google/Chrome`
- **Linux:** Usually `~/.config/google-chrome`

Make sure to use double backslashes (`\\`) in Windows paths.

### Configuration Details

- `BUY_AMOUNT`: Amount of USDC to buy each time
- `MAX_BUY_ATTEMPTS`: Maximum number of buy attempts
- `BUY_DELAY`: Delay between buy operations (seconds)
- `CHECK_INTERVAL`: Interval to check Twitter (seconds)
- `HEADLESS`: Should be set to False when using existing Chrome session

## Chrome Setup

The bot can either connect to an already running Chrome instance or start Chrome automatically:

### Option 1: Manual Chrome Start (Recommended)

1. Close all Chrome windows
2. Start Chrome with remote debugging enabled using this command:

   **Windows:**
   ```
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data"
   ```

   **Mac:**
   ```
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="~/Library/Application Support/Google/Chrome"
   ```

   **Linux:**
   ```
   google-chrome --remote-debugging-port=9222 --user-data-dir="~/.config/google-chrome"
   ```

3. In the opened Chrome window, navigate to https://time.fun and log in
4. Keep Chrome open and running
5. Then run the bot

### Option 2: Automatic Chrome Start

The bot can now automatically start Chrome with the correct parameters if:
- Chrome is not already running with remote debugging
- You have correctly set the `CHROME_USER_DATA_DIR` in your `.env.utf8` file

## Usage

The program provides the following operation modes:

### 1. Monitor Mode (Main Function)

Use `timefun_buyer_en.py` to monitor Twitter and auto-buy:

```bash
python timefun_buyer_en.py [options]
```

Available options:
- `--username` or `-u`: Set Twitter username to monitor (default: timedotfun)
- `--interval` or `-i`: Set check interval in seconds (default: 30)
- `--timezone` or `-t`: Set timezone offset (default: 8 for Beijing time)
- `--max-tweets` or `-m`: Set maximum tweets to check each time (default: 5)
- `--skip-login-check`: Skip login verification

### 2. Direct Buy Mode

Use `timefun_buyer_en.py` to buy time coins for a specific user:

```bash
python timefun_buyer_en.py --buy USERNAME [--skip-login-check]
```

### 3. Verify Mode

Verify if a user exists on time.fun:

```bash
python timefun_buyer_en.py --verify USERNAME
```

## Troubleshooting

### Login Detection Issues

If the bot fails to detect that you're logged in even though you are, use the `--skip-login-check` flag:

```bash
python timefun_buyer_en.py --skip-login-check
```

### Button Detection Issues

If the bot cannot find the Buy button:
1. Check the debug screenshots saved in the project directory (debug_screenshot_*.png)
2. Review the console output for button text information
3. Make sure you're logged into TimeFun in your Chrome session

## File Descriptions

- `timefun_buyer_en.py` - Main program with monitoring and buying functionality
- `test_buy_en.py` - Buying functionality test script
- `.env.utf8` - Environment variables configuration file

## Development Status

Current version: 1.0.0

### Completed Features
- [COMPLETE] Auto-buying functionality
  - Chrome integration and remote debugging
  - Automatic Chrome startup
  - Market page navigation
  - Two-step purchase process
  - Detailed error logging and screenshots
- [COMPLETE] Twitter monitoring functionality
  - Real-time monitoring of @timedotfun account
  - Automatic identification of promoted usernames

### Planned Features
- [PLANNED] Web interface for monitoring and control
- [PLANNED] Support for multiple accounts

## Important Notes

- Ensure your TimeFun account has sufficient USDC balance
- Using automated trading tools carries risks
- Start with small amounts to test functionality before increasing
- This bot is provided for educational purposes only
- The developers are not responsible for any financial losses or account issues

## License

[MIT License](LICENSE) 