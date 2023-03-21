import pandas as pd
import numpy as np
import talib

# Load the data
data = pd.read_csv("path/to/your/data.csv")

# Calculate the RSI
rsi_period = 14
data["RSI"] = talib.RSI(data["Close"], timeperiod=rsi_period)

# Calculate the MACD
macd_fast_period = 12
macd_slow_period = 26
macd_signal_period = 9
macd, signal, hist = talib.MACD(data["Close"], fastperiod=macd_fast_period, slowperiod=macd_slow_period, signalperiod=macd_signal_period)
data["MACD"] = macd
data["Signal"] = signal

# Generate trading signals
data["Position"] = np.where(data["MACD"] > data["Signal"], 1, 0)
data["Position"] = np.where(data["MACD"] < data["Signal"], -1, data["Position"])
data["Position"] = data["Position"].shift(1)

# Calculate the returns
data["Returns"] = np.log(data["Close"]/data["Close"].shift(1))

# Calculate the strategy returns
data["StrategyReturns"] = data["Position"] * data["Returns"]

# Calculate the cumulative returns
data["CumulativeReturns"] = np.exp(data["StrategyReturns"].cumsum()) - 1

# Print the results
print("RSI Period:", rsi_period)
print("MACD Fast Period:", macd_fast_period)
print("MACD Slow Period:", macd_slow_period)
print("MACD Signal Period:", macd_signal_period)
print(data.tail())
