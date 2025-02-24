import matplotlib as plt
from stock import Stock

aapl = Stock(ticker="AAPL")
aapl.calculate_fvg()
aapl.save_data()

print(aapl.data)