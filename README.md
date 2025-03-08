# TimeFun Sniper Bot

[![en](https://img.shields.io/badge/lang-English-blue.svg)](README.md) [![cn](https://img.shields.io/badge/语言-中文-red.svg)](README_CN.md)

This is a bot that monitors Twitter and automatically buys time coins on the time.fun website.

> **Development Status**: [COMPLETE] Auto-buying functionality is complete and tested successfully. [IN PROGRESS] Twitter monitoring functionality is still under development.

## Features

- Monitors @timedotfun Twitter account for retweets
- Automatically identifies promoted usernames
- Automatically buys time coins for the promoted users on time.fun
- Connects to your existing Chrome session to avoid Cloudflare detection
- Supports two-step purchase confirmation process

## ?? Security Notice

**IMPORTANT:** This bot requires access to your Chrome browser and TimeFun account. Please review the following security considerations:

- The bot connects to your Chrome browser with remote debugging enabled, which could potentially expose your browser to other applications
- Your Chrome user data directory contains sensitive information including cookies and saved passwords
- The `.env.utf8` file contains sensitive API keys and credentials
- Never share your `.env.utf8` file, debug screenshots, or Chrome user data directory
- Review the code before running it to ensure it meets your security requirements

## Installation

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env.utf8` file with the necessary configuration (see Configuration section)

## Configuration

Configure the following in your `.env.utf8` file (note: do not add comments after values as this may cause parsing errors):

```
# Twitter API credentials
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret

# TimeFun account information
TIMEFUN_EMAIL=your_email
TIMEFUN_PASSWORD=your_password

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

- `TIMEFUN_EMAIL`: Your TimeFun account email (for reference only)
- `TIMEFUN_PASSWORD`: No longer used but kept for compatibility
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

## How Buying Works

The bot navigates directly to the user's market tab (e.g., https://time.fun/username?tab=market) where the Buy button is located. It will:

1. Try to find the Buy button using various selectors
2. Click the Buy button when found
3. Enter the configured amount of USDC
4. Click the final "Confirm & Buy" button to complete the purchase

The bot now supports the two-step purchase process:
- First click on the "Buy X mins for $Y" button
- Then click on the "Confirm & Buy X mins for $Y" button

## Troubleshooting

### Login Detection Issues

If the bot fails to detect that you're logged in even though you are, use the `--skip-login-check` flag:

```
python main.py --skip-login-check
```

or for testing:

```
python test_buy_en.py <username> --skip-login-check
```

### Button Detection Issues

If the bot cannot find the Buy button:
1. Check the debug screenshots saved in the project directory
2. Review the console output for button text information
3. Make sure you're logged into TimeFun in your Chrome session

## Testing

Before running the main program, you can run tests:

1. Test network connection: `python test_connection.py`
2. Test buying functionality: `python test_buy_en.py <username>`
3. Test Twitter monitoring: `python test_monitor.py`

## Usage

Run the main program:

```
python main.py
```

The program will monitor @timedotfun's Twitter account and automatically buy time coins for promoted users.

## File Descriptions

- `main.py` - Main program that integrates Twitter monitoring and TimeFun buying
- `twitter_monitor.py` - Twitter monitoring module
- `timefun_buyer_en.py` - TimeFun buying module
- `test_*.py` - Various test scripts
- `.env.utf8` - Environment variables configuration

## Development Status

Current version: 1.0.0

- [COMPLETE] Auto-buying functionality complete
  - [COMPLETE] Chrome integration with remote debugging
  - [COMPLETE] Automatic Chrome startup
  - [COMPLETE] Market tab navigation
  - [COMPLETE] Two-step purchase process
  - [COMPLETE] Detailed error logging and screenshots
- [IN PROGRESS] Twitter monitoring under development
  - [IN PROGRESS] Real-time monitoring of @timedotfun account
  - [IN PROGRESS] Automatic identification of promoted usernames
- [PLANNED] Planned features
  - [PLANNED] Improved error handling and recovery
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