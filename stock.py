import yfinance as yf
import datetime as dt
import pandas as pd
from matplotlib import pyplot as plt

class Stock:
    ticker = ''
    csv_name = ''
    data = [[]]

    def __init__(self,ticker):
        self.ticker = ticker
        self.csv_name = ticker + ' data.csv'
        self.extract_data()
        self.transform_data()
        self.load_data()
        

    def extract_data(self):
        self.data = yf.Ticker(self.ticker)
        self.data = self.data.history(period = 'max')

    def transform_data(self):
        del self.data['Dividends']
        del self.data['Stock Splits']
        self.data = self.data.loc['2022-01-01':].copy() 

    def load_data(self):
        self.data.to_csv(self.csv_name)

    def plot_data(self):
        self.data.plot.line(y='Close',use_index=True,label=self.ticker)
        plt.xlabel('Date')
        plt.ylabel('Price (USD)')

    def print_data(self):
        del self.data['Open']
        del self.data['High']
        del self.data['Low']
        del self.data['Close']
        del self.data['Volume']
        del self.data['Body']
        print(self.data)
    