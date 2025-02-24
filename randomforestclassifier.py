#pip install scikit-learn
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

    # calculate averages within
    # 2 days
    # 1 week
    # 3 months
    # 1 year
    horizons = [2,5,60,250]

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
