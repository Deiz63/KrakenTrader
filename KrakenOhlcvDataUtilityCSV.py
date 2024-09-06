# NOTE: DEFAULT UTILITY TO SIMPLIFY COLLECTING KRAKEN TOKEN DATA 
# NOTE: SIMPLIFIED MODULE TO ASSIST WITH BACKTESTING & ORDER TRACKING
# NOTE: DATA CONVERTED TO DF & CSV FILE FOR OUTPUT.
from KrakenCancelOrdersForToken import  token, token_pair
import pandas as pd
import requests
import numpy as np
import math



def get_low_data(token_pair):
    # Fetch data from Kraken API
    coin_symbol = token_pair # Ensure the correct pair key, check Kraken API documentation for exact symbol
    params = {'interval': 5}

    resp = requests.get(f'https://api.kraken.com/0/public/OHLC?pair={coin_symbol}', params=params)

    # Check if the request was successful
    if resp.status_code == 200:
        data = resp.json()
        
        # Extract the OHLC data for the pair
        ohlc_data = data['result'][coin_symbol]  # Ensure you use the correct pair key here
        
        # Define the column names based on Kraken's OHLC data structure
        columns = ['time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
        
        # Create a DataFrame
        df = pd.DataFrame(ohlc_data, columns=columns)
        df = df.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'})
        
        # Convert the timestamp to a readable format
        df['time'] = pd.to_datetime(df['time'], unit='s')
        
        # Convert relevant columns to numeric types
        df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].apply(pd.to_numeric, errors='coerce')
        
        # Drop any rows with NaN values
        df.dropna(inplace=True)
        
        # Sort values by time
        df.sort_values(by=['time'], ascending=True, inplace=True)
        
        
    else:
        print(f"Error fetching data: {resp.status_code}")
        
    # Calculate Current Price vs. Previous Price     
    df['Close_Previous'] = df['Close'].shift(1)
    df['Change_Last'] = df['Close'] - df["Close_Previous"]
    df['Change_%_of_Total'] = df['Change_Last'] / df['Close']

    df["High_50"] = (df['High'].rolling(window=50)).max() # High Price for last 50 Periods
    df["Current_vs_High_50"] = df["High_50"] - df["Close"] # High_50 minus Current Price 

    df["Low_10"] = (df['Low'].rolling(window=10)).min() # Low Price for last 10 Periods
    df["Low_50"] = (df['Low'].rolling(window=50)).min() # Low Price for last 50 Periods
    df["Low_200"] = (df['Low'].rolling(window=200)).min() # Low Price for last 200 Periods

    # Calculate the SMA's of the 'count' & 'Volume' column
    df["SMA_Trade_count"] = df['count'].rolling(window=50).mean() # Trade count SMA
    df["trade_score"] = df["count"] / df["SMA_Trade_count"] # Shows Todays % trade count vs SMA

    df['SMA_Volume'] = df['Volume'].rolling(window=50).mean() # Rolling SMA of volume @ 50 period Window
    df['vol_score'] = (df['Volume'] / df['SMA_Volume']) # Todays volume against SMA_Volume

    df['Spread'] = df['High'] - df['Low'] # Current High vs Low = Spread 
    df['Spread_%_Total'] = (df['Spread'] / df['Close']) * 100

    df.style.hide(axis="index") # neither of these seem to work
    df.style.format(precision=2) # Should be placing only 2 decimals in output


    #print(df)

    # Save the DataFrame to a CSV file
    #csv_file_path = f'kraken_OHLCV_{coin_symbol}.csv'
    #df.to_csv(csv_file_path, index=False)
    #print(f'DataFrame saved to {csv_file_path}')

    # Access the 'Low_10' value from the last row using .iloc
    low_10_latest = df.iloc[-1]['Low_10']
    #print(low_10_latest)
    return low_10_latest
    # Access the 'Low_10' value from the last row using .tail(1)
    #low_10_latest = df['Low_10'].tail(1).values[0]