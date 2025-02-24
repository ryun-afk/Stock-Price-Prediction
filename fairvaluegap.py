import statistics

"""
Calculates Fair Value Gaps in historical price data

data (DataFrame): DataFrame with columns ['open','high','low','close']
lookback_period (int): Number of candles to look back for average
threshold (float): Multiplier to determine significant average
"""

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