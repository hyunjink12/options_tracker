import yfinance as yf
t = yf.Ticker("SPY") # replace with desired ticker symbol
expiries = t.options
print(expiries [:10], len(expiries))
# prints expiries & total count available for ticker
# set at 10 for viewing purposes, can be adjusted as needed
