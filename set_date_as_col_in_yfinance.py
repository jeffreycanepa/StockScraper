import yfinance as yf 
tickers = ["AAPL"] 
df = yf.download(tickers,  start = "2021-02-01" , end = "2021-02-04") 
newdf = df.reset_index() 
print(newdf)
