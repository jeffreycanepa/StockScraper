import yfinance as yf 
tickers = ["AAPL"] 
df = yf.download(tickers,  start = "2023-09-01" , end = "2023-09-12") 
newdf = df.reset_index() 
## Get the column names
# for col in newdf.columns:
#     print(col)

# Set list to values in Column 'Date'
myDates = newdf.loc[:,'Date']
x = len(myDates) -1
print(myDates)
print(myDates[0])
print(myDates[len(myDates)-1])