#pip install pandas-datareader
#pip install matplotlib
#pip install yfinance

import numpy as np
import pandas as pd
import pandas_datareader as data
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt

# retrieve data sets from yahoo finance API
stock = "AAPL"
start = dt.datetime(2020,1,1)
end = dt.datetime(2024,12,31)
df = yf.download(stock,start,end)

# returns first 5 data rows
print('Head')
print(df.head())

# returns number of data and data columns
# Date is a unique identifier
# Below are the column headers
# Close / High / Low / Open / Volume
print('Shape')
print(df.shape)

# returns first 5 and last 5 data rows
print('Info')
print(df.info)

# checks for missing data
print(df.isnull())

# returns number of missing data in each column
print(df.isnull().sum())

print(df.describe())