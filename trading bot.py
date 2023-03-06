import yfinance as yf
import matplotlib.pyplot as plt

# Define the stock symbol and the timeframe for the data
symbol = 'AAPL'
start_date = '2019-03-06'
end_date = '2021-03-06'

# Get the historical stock data for the specified timeframe
data = yf.download(symbol, start=start_date, end=end_date)

# Define the breakout algorithm
def breakout(data):
    high = data['High'].rolling(window=20).max()
    low = data['Low'].rolling(window=20).min()
    close = data['Close']
    buy_signal = close > high.shift(1)
    sell_signal = close < low.shift(1)
    return buy_signal, sell_signal

# Use the breakout algorithm to generate buy and sell signals
buy_signal, sell_signal = breakout(data)

# Create a variable to keep track of our position
position = None

# Create a list to store the prices of the stock
prices = []

# Loop through the data and execute trades based on the signals
for i in range(len(data)):
    if buy_signal[i]:
        if position is None:
            # Buy the stock if we don't currently have a position
            print(f"Buying {symbol} at {data['Close'][i]}")
            position = 'long'
            prices.append(data['Close'][i])
        elif position == 'short':
            # Buy back our short position and then buy the stock
            print(f"Buying back short position and then buying {symbol} at {data['Close'][i]}")
            position = 'long'
            prices.append(data['Close'][i])
    elif sell_signal[i]:
        if position is None:
            # Short the stock if we don't currently have a position
            print(f"Shorting {symbol} at {data['Close'][i]}")
            position = 'short'
            prices.append(-data['Close'][i])
        elif position == 'long':
            # Sell our long position and then short the stock
            print(f"Selling long position and then shorting {symbol} at {data['Close'][i]}")
            position = 'short'
            prices.append(-data['Close'][i])
    else:
        # Do nothing if we don't have a signal
        prices.append(None)
        pass

# Plot the price of the stock and the trades we executed
fig, ax = plt.subplots()
ax.plot(data['Close'])
for i in range(len(prices)):
    if prices[i] is not None:
        if prices[i] > 0:
            ax.scatter(data.index[i], prices[i], marker='^', color='g')
        else:
            ax.scatter(data.index[i], -prices[i], marker='v', color='r')
plt.show()
