Stock Price Prediction Project: Machine Learning with Random Forest Classifiers and Fair Value Gap for Apple Stock Prices. 

import yfinance as yf
from matplotlib import pyplot as plt

# Retrieving open, high, low, close, and volume of Apple trades from yahoo finance API
data = yf.Ticker('AAPL')
data = data.history(period='max')

# Calculating fair value gap (FVG):
# FVG is calculated by subtracting the current market price from the theoretical price. 
# The theoretical price can be calculated by averaging the open and close prices from historical data. 
# By comparing the differences, we can add a data column for historical bullish or bearish days. 

import statistics
def fvg(data,lookback_period=10,body_multiplier=1.5):
    body_list = [0,0,0,0]
    fvg_list = [None,None,None,None]

    for  i in range(4,len(data)):
        first_high = data['High'].iloc[i-2]
        first_low = data['Low'].iloc[i-2]
        third_high = data['High'].iloc[i]
        third_low = data['Low'].iloc[i]

        # calculates candlestick body
        open = float(data.Open.iloc[i])
        close = float(data.Close.iloc[i])
        body = abs(open - close)
        body_list.append(body)

        # calculates average candlestick body size within lookback period
        avg_body = statistics.mean(body_list[max(0,i-1-lookback_period):i-1])
        
        # body size less than average body is an insignificant change
        if body_list[i-1] < avg_body * body_multiplier:
            fvg_list.append(None)

        # record prices following upward trend
        elif first_high < third_low:
            fvg_list.append('bullish')

        # record prices following downward trend
        elif first_low > third_high:
            fvg_list.append('bearish')
        
        # rest are None
        else:
            fvg_list.append(None)

    # body size for each day
    data['Body']= body_list

    # fair value gap for each day
    return fvg_list

# Implementing Random Forest Classifier (RFC):
# RFC is a machine learning algorithm used for classification. It combines multiple data sources and makes a prediction based on historical data and training. 

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
import pandas as pd
import numpy as np

def rfc(data):
    data['Tomorrow'] = data.Close.shift(-1)
    data['Target'] = data['Tomorrow'] > data['Close'].astype(int)

    model = RandomForestClassifier(n_estimators=100,
                                   min_samples_split=100,
                                   random_state=1)
    
    train = data.iloc[:-100]
    test = data.iloc[-100:]

    predictors = ['Open','High','Low','Close']
    predictions = backtest(data,model,predictors)

    # calculate averages within the dates
    TWO_DAYS_OF_TRADES = 2
    ONE_WEEK_OF_TRADES = 5
    THREE_MONTHS_OF_TRADES = 60
    ONE_YEAR_OF_TRADES = 250

    horizons = [TWO_DAYS_OF_TRADES,
                ONE_WEEK_OF_TRADES,
                THREE_MONTHS_OF_TRADES,
                ONE_YEAR_OF_TRADES]

    new_predictors = []
    for horizon in horizons:
        rolling_averages = data.rolling(horizon)

        ratio_column = f'Close_Ratio_{horizon}'
        data[ratio_column] = data['Close'] / rolling_averages['Close']

        trend_column = f'Trend_{horizon}'
        data[trend_column] = data.shift(1).rolling(horizon).sum['Target']

        new_predictors += [ratio_column,trend_column]

    print(data)


def predict(train,test,predictors,model):
    model.fit(train[predictors],train['Target'])

    predictions = model.predict(test[predictors])
    predictions = pd.Series(predictions,index=test.index, name='Predictions')
    combined = pd.concat([test['Target'],predictions], axis=1)

    return combined

def backtest(data,model,predictors,start=250,step=250):
    all_predictions = []

    for i in range(start, data.shape[0], step):
        train = data.iloc[0:i].copy()
        test = data.iloc[i:(i+step)].copy()

        predictions = predict(train,test,predictors,model)
        all_predictions.append(predictions)
    
    return pd.concat(all_predictions)

# Combining these two methods allows for higher confidence in the algorithm for when to sell or buy. 
# There are more trading strategies that could be implemented into this data pipeline for quick stock price analysis for weekly trades. 
