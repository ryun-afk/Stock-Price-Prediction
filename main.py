import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from stock import Stock

tickers = "AAPL"

stock = Stock(tickers=tickers)


print(stock.df.head())