import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from stock import Stock

ticker = "AAPL"

stock = Stock(ticker=ticker)
stock.calculate_fvg()
print(stock.df.head(20))