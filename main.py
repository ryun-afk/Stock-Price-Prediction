





# yfinance documentation:
# https://pypi.org/project/yfinance/

import numpy as np
import pandas as pd
import datetime as dt

#pip install pandas-datareader
import pandas_datareader as data

#pip install matplotlib
import matplotlib.pyplot as plt

#pip install plotly
import plotly.graph_objects as go

#pip install yfinance
import yfinance as yf


#pip install scikit-learn
from sklearn.preprocessing import MinMaxScaler
from keras.layes import Dense, Dropout, LSTM
from keras.models import Sequential

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


'''
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
'''


# Training and Testing LSTM
partition = .7
data_training = pd.DataFrame(df.Close[0:int(len(df)*partition)])
data_testing = pd.DataFrame(df.Close[int(len(df)*partition):int(len(df))])

print(data_training.shape)
print(data_testing.shape)

scaler = MinMaxScaler(feature_range=(0,1))
data_training_arr = scaler.fit_transform(data_training)

x_train = []
y_train = []

for i in range(100,data_training_arr.shape[0]):
    x_train.append(data_training_arr[i-100:i])
    y_train.append(data_training_arr[i,0])

x_train,y_train = np.array(x_train), np.array(y_train)

# Model Building
