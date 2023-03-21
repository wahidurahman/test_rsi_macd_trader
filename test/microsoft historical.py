import pandas_datareader as pdr

# Load the data
start_date = "2015-01-01"
end_date = "2022-03-21"
msft = pdr.get_data_yahoo("MSFT", start=start_date, end=end_date)

# Rename columns
msft = msft.rename(columns={"Adj Close": "Close"})

# Calculate the RSI
rsi_period = 14
msft["RSI"] = talib.RSI(msft["Close"], timeperiod=rsi_period)

# Calculate the MACD
macd_fast_period = 12
macd_slow_period = 26
macd_signal_period = 9
macd, signal, hist = talib.MACD(msft["Close"], fastperiod=macd_fast_period, slowperiod=macd_slow_period, signalperiod=macd_signal_period)
msft["MACD"] = macd
msft["Signal"] = signal

# Generate trading signals
msft["Position"] = np.where(msft["MACD"] > msft["Signal"], 1, 0)
msft["Position"] = np.where(msft["MACD"] < msft["Signal"], -1, msft["Position"])
msft["Position"] = msft["Position"].shift(1)

# Calculate the returns
msft["Returns"] = np.log(msft["Close"]/msft["Close"].shift(1))

# Calculate the strategy returns
msft["StrategyReturns"] = msft["Position"] * msft["Returns"]

# Calculate the cumulative returns
msft["CumulativeReturns"] = np.exp(msft["StrategyReturns"].cumsum()) - 1

# Print the results
print("RSI Period:", rsi_period)
print("MACD Fast Period:", macd_fast_period)
print("MACD Slow Period:", macd_slow_period)
print("MACD Signal Period:", macd
