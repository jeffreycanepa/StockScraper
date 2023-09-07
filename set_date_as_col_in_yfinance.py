import yfinance as yf 
tickers = ["AAPL"] 
df = yf.download(tickers,  start = "2021-02-01" , end = "2021-02-04") 
newdf = df.reset_index() 
## Get the column names
# for col in newdf.columns:
#     print(col)

# Set list to values in Column 'Date'
myDates = newdf.loc[:,'Date']
print(myDates)