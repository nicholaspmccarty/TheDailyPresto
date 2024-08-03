import tweepy
import time
import yfinance as yf
import schedule
import datetime
import os

# Function to read credentials from data.txt
def read_credentials():
    creds = {}
    with open('data.txt', 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            creds[key] = value
    return creds

# Load credentials
credentials = read_credentials()
api_key = credentials['api_key']
api_key_secret = credentials['api_key_secret']
access_token = credentials['access_token']
access_token_secret = credentials['access_token_secret']
bearer_token = credentials['bearer_token']

# Authenticate to Twitter using OAuth2
client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_key_secret, access_token=access_token, access_token_secret=access_token_secret)

# Function to get and print the current Presto stock price
def get_presto_stock_price():
    stock = yf.Ticker("PRST")
    stock_price = stock.history(period="1d")["Close"].iloc[-1]
    print(f"The current price of Presto stock (PRST) is ${stock_price:.2f}")
    try:
        client.create_tweet(text=f"The current price of Presto stock (PRST) is ${stock_price:.2f}")
    except Exception as e:
        print(f"Error during tweeting stock price: {e}")

# Log system info and Unix time on login
def log_system_info():
    unix_time = int(time.time())
    system_info = os.uname()  # For Unix-based systems
    print(f"Logged in successfully on PC: {system_info}")
    print(f"Unix time: {unix_time}")

# Schedule the stock price tweet every 24 hours
schedule.every(24).hours.do(get_presto_stock_price)

# Verify the credentials and log system info
try:
    response = client.get_me()
    if response.data:
        print("Authentication OK")
        log_system_info()
except Exception as e:
    print("Error during authentication", e)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
