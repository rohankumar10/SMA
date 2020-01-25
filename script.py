import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
import pandas_datareader as pdr
short_window = 40
long_window = 100
aapl = pdr.get_data_yahoo('AAPL',
start=datetime.datetime(2015, 10, 1),
end=datetime.datetime(2020, 10, 27))
signals = pd.DataFrame(index=aapl.index)
signals['signal'] = 0.0
signals['short'] = aapl['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
signals['long'] = aapl['Close'].rolling(window=long_window, min_periods=1, center=False).mean()
signals['signal'][short_window:] = np.where(signals['short'][short_window:]
                                            > signals['long'][short_window:], 1.0, 0.0)
signals['positions'] = signals['signal'].diff()
print(signals)
fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Price in $')
aapl['Close'].plot(ax=ax1, color='m', lw=2.)
signals[['short', 'long']].plot(ax=ax1, lw=2.)
ax1.plot(signals.loc[signals.positions == 1.0].index,
         signals.short[signals.positions == 1.0],
         '^', markersize=7, color='g')
ax1.plot(signals.loc[signals.positions == -1.0].index,
         signals.short[signals.positions == -1.0],
         'v', markersize=7, color='r')
plt.show()
