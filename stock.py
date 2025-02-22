import yfinance as yf
import datetime as dt
import pandas as pd
import os.path

class Stock:
    tickers = ""
    csv_name = ""
    data = [[]]

    def __init__(self,tickers):
        self.tickers = tickers
        self.csv_name = tickers + " data.csv"
        self.df = self.read_data()
        

    def read_data(self):
        if not os.path.isfile(self.csv_name):
            self.download_data(self)

        return pd.read_csv(self.csv_name)

    def download_data(self):
        # Collect data from 2020 to 2024
        start = dt.datetime(2020,1,1)
        end = dt.datetime(2024,12,31)
        self.df = yf.download(self.tickers,start,end)
        self.filter_data
        self.df.to_csv(self.csv_name)

    def filter_data(self):
        self.df.reset_index(drop=True,inplace=True)