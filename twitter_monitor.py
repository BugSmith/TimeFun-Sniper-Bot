# -*- coding: utf-8 -*-
import os
import re
import time
import tweepy
from dotenv import load_dotenv

class TwitterMonitor:
    def __init__(self):
        load_dotenv(dotenv_path=".env.utf8")
        
        # Get Twitter API credentials
        api_key = os.getenv('TWITTER_API_KEY')
        api_secret = os.getenv('TWITTER_API_SECRET')
        access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        # Initialize Twitter API
        auth = tweepy.OAuth1UserHandler(
            api_key, api_secret, access_token, access_token_secret
        )
        self.api = tweepy.API(auth)
        
        # Set Twitter account to monitor
        self.target_account = "timedotfun"
        
        # Store processed tweet IDs
        self.processed_tweets = set()
        
    def get_latest_retweets(self):
        """Get latest retweets from @timedotfun"""
        try:
            # Get user timeline
            tweets = self.api.user_timeline(
                screen_name=self.target_account,
                count=10,  # Get the latest 10 tweets
                include_rts=True,
                tweet_mode="extended"
            )
            
            # Filter retweets
            retweets = [tweet for tweet in tweets if hasattr(tweet, 'retweeted_status')]
            
            return retweets
        except Exception as e:
            print(f"Error getting tweets: {e}")
            return []
    
    def extract_username(self, tweet):
        """Extract promoted username from tweet"""
        # Method 1: Extract author username from original retweeted tweet
        if hasattr(tweet, 'retweeted_status'):
            return tweet.retweeted_status.user.screen_name
        
        # Method 2: Extract username from tweet text
        # Example: "time.fun has retweeted Zagabond @Zagabond Just set up my profile on @timedotfun"
        full_text = tweet.full_text
        
        # Try to match patterns: "has retweeted Username" or "@Username"
        patterns = [
            r"已转帖\s+(\w+)",  # Match "已转帖 Username"
            r"@(\w+)",          # Match "@Username"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, full_text)
            if matches:
                # Exclude known usernames like timedotfun
                for match in matches:
                    if match.lower() != "timedotfun":
                        return match
        
        return None
    
    def check_new_promotions(self):
        """Check for new promotions, return list of newly discovered usernames"""
        new_usernames = []
        
        retweets = self.get_latest_retweets()
        for tweet in retweets:
            # Skip if this tweet has already been processed
            if tweet.id in self.processed_tweets:
                continue
            
            # Extract username
            username = self.extract_username(tweet)
            if username:
                new_usernames.append(username)
                print(f"Found new promoted user: {username}")
            
            # Mark as processed
            self.processed_tweets.add(tweet.id)
        
        return new_usernames
    
    def monitor(self, callback):
        """Continuously monitor Twitter, call callback function when new promotions are found"""
        try:
            check_interval = int(os.getenv('CHECK_INTERVAL', '60').strip())
        except ValueError as e:
            print(f"Error parsing CHECK_INTERVAL: {e}")
            print("Using default value of 60 seconds")
            check_interval = 60
        
        print(f"Starting to monitor @{self.target_account} retweets...")
        
        while True:
            try:
                new_usernames = self.check_new_promotions()
                
                # Call callback function for each newly discovered username
                for username in new_usernames:
                    callback(username)
                
                # Wait for specified interval
                time.sleep(check_interval)
            except Exception as e:
                print(f"Error during monitoring: {e}")
                # Wait a while before continuing after error
                time.sleep(check_interval) 