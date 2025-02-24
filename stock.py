import numpy as np
import statistics
import yfinance as yf
import datetime as dt
import pandas as pd
import os.path

class Stock:
    ticker = ""
    csv_name = ""
    data = [[]]

    def __init__(self,ticker):
        self.ticker = ticker
        self.csv_name = ticker + " data.csv"
        self.data = self.read_data()
        

    def read_data(self):
        if not os.path.isfile(self.csv_name):
            self.download_data()
        return pd.read_csv(self.csv_name)

    def download_data(self):
        self.data = yf.Ticker(self.ticker)
        self.data = self.data.history(period = 'max')
        self.save_data()
        
    def save_data(self):
        self.data.to_csv(self.csv_name)

    def calculate_fvg(self,lookback_period=10,body_multiplier=1.5):
        """
        Calculates Fair Value Gaps in historical price data

        data (DataFrame): DataFrame with columns ['open','high','low','close']
        lookback_period (int): Number of candles to look back for average
        threshold (float): Multiplier to determine significant average
        """

        body_list = [0,0,0,0]
        fvg_list = [None,None,None,None]
        for  i in range(4,len(self.data)):
            first_high = self.data.High[i-2]
            first_low = self.data.Low[i-2]
            third_high = self.data.High[i]
            third_low = self.data.Low[i]

            # calculates candlestick body
            open = float(self.data.Open[i])
            close = float(self.data.Close[i])
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
        self.data['Body']= body_list

        # fair value gap for each day
        self.data['FVG'] = fvg_list