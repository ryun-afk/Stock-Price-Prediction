import numpy as np
import statistics
import yfinance as yf
import datetime as dt
import pandas as pd
import os.path

class Stock:
    tickers = ""
    csv_name = ""
    data = [[]]

    def __init__(self,ticker):
        self.ticker = ticker
        self.csv_name = ticker + " data.csv"
        self.df = self.read_data()
        

    def read_data(self):
        if not os.path.isfile(self.csv_name):
            self.download_data()

        return pd.read_csv(self.csv_name)

    def download_data(self):
        """
        Downloads stock price data and saves as csv
        """
        start = dt.datetime(2020,1,1)
        end = dt.datetime(2024,12,31)
        data = yf.download(self.ticker,start,end)
        data.reset_index(drop=True,inplace=True)
        data.to_csv(self.csv_name)
        

    def calculate_fvg(self,lookback_period=10,body_multiplier=1.5):
        """
        Calculates Fair Value Gaps in historical price data

        data (DataFrame): DataFrame with columns ['open','high','low','close']
        lookback_period (int): Number of candles to look back for average
        threshold (float): Multiplier to determine significant average
        """

        body_list = [0,0,0,0]
        fvg_list = [None,None,None,None]
        for  i in range(4,len(self.df)):
            first_high = self.df.High[i-2]
            first_low = self.df.Low[i-2]
            third_high = self.df.High[i]
            third_low = self.df.Low[i]

            # calculates candlestick body
            open = float(self.df.Open[i])
            close = float(self.df.Close[i])
            body = abs(open - close)
            body_list.append(body)

            # calculates average candlestick body within lookback period
            avg_body = statistics.mean(body_list[max(0,i-1-lookback_period):i-1])
            
            # checks candlestick body size
            # body size less than average body are insignificant changes
            if body_list[i-1] < avg_body * body_multiplier:
                fvg_list.append(None)

            # record prices following upward trend
            elif first_high < third_low:
                fvg_list.append(('bullish',first_high,third_low))

            # record prices following downward trend
            elif first_low > third_high:
                fvg_list.append(('bearish',first_low,third_high))
            
            # rest are None
            else:
                fvg_list.append(None)

        # body size for each day
        self.df['Body']= body_list

        # fair value gap for each day
        self.df['FVG'] = fvg_list