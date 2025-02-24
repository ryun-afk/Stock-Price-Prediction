from matplotlib import pyplot as plt

from stock import Stock
from fairvaluegap import fvg
from randomforestclassifier import *

print('start')

# initialize data
AAPL = Stock(ticker='AAPL')
KHC = Stock(ticker='KHC')


AAPL.data['FVG'] = fvg(AAPL.data)
rfc(AAPL.data)


# matplotlib visual
#AAPL.plot_data()
#KHC.plot_data()
#plt.show()

# terminal print
#AAPL.print_data()


print('end')