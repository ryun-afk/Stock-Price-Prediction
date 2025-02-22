


def detect_fvg(data,lookback_period=10,threshold=1.5):
    """
    Detects Fair Value Gaps in historical price data

    data (DataFrame): DataFrame with columns ['open','high','low','close']
    lookback_period (int): Number of candles to look back for average
    threshold (float): Multiplier to determine significant average
    """

    fvg_list = [None,None]

    for  i in range(2,len(data)):
        first_high = data.High.iloc[i-2]
        first_low = data.Low.iloc[i-2]