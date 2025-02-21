#pip install pandas-datareader
#pip install matplotlib
#pip install yfinance
#pip install plotly

# yfinance documentation:
# https://pypi.org/project/yfinance/

import numpy as np
import pandas as pd
import pandas_datareader as data

import matplotlib.pyplot as plt
import plotly.graph_objects as go

import yfinance as yf
import datetime as dt

# retrieve data sets from yahoo finance API
stock = "AAPL"
start = dt.datetime(2020,1,1)
end = dt.datetime(2024,12,31)
df = yf.download(stock,start,end)

# returns first 5 data rows
#print('Head')
#print(df.head())

# returns number of data and data columns
# Date is a unique identifier
# Below are the column headers
# Close / High / Low / Open / Volume
#print('Shape')
#print(df.shape)

# returns first 5 and last 5 data rows
#print('Info')
#print(df.info)

# checks for missing data
#print(df.isnull())

# returns number of missing data in each column
#print(df.isnull().sum())

# returns table with standard information
# count, mean, std, min, Q1, Q2, Q3, max
# print(df.describe())

# resets index / order of data
df = df.reset_index()

# returns column names
#print(df.columns)
#output below:
# MultiIndex([(  'Date',     ''),
#            ( 'Close', 'AAPL'),
#            (  'High', 'AAPL'),
#            (   'Low', 'AAPL'),
#            (  'Open', 'AAPL'),
#            ('Volume', 'AAPL')],
#           names=['Price', 'Ticker'])

# exports to a csv file
csv_name = stock+" data.csv"
df.to_csv(csv_name)

# read csv files and allows data indexing for fig
data1 = pd.read_csv(csv_name)
fig = go.Figure(data = [go.Candlestick(x = data1['Date'],
                                       open = data1['Open'],
                                       high = data1['High'],
                                       low = data1['Low'],
                                       close = data1['Close'])])
fig.update_layout(xaxis_rangeslider_visible = False)
#fig.show()



#moving average
days_average100 = df.Close.rolling(100).mean()
days_average200 = df.Close.rolling(200).mean()

# multiple plots
plt.plot(df['Date'],df.Close,label = f'{stock} Close Price')
plt.plot(df['Date'],days_average100, label = f'{stock} moving average 100 price')
plt.plot(df['Date'],days_average200, label = f'{stock} moving average 200 price')

plt.xlabel('Date')
plt.ylabel('USD')
plt.legend()
plt.show()

# exponentially weightted moving
ema100 = df.Close.ewm(span=100,adjust = False).mean()
ema200 = df.Close.ewm(span=200,adjust = False).mean()
print(df.pct_change)
plt.plot(df['Date'],df.Close,label = f'{stock} Close Price')
plt.plot(df['Date'],ema100, label = f'{stock} moving average 100 price')
plt.plot(df['Date'],ema200, label = f'{stock} moving average 200 price')
plt.legend()
plt.show()