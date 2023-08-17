import yfinance as yf
import datetime
import csv

# My Stocks
myStocks = ['AAPL', 'ADBE', 'CSCO', 'NTAP', 'MSFT', 'AMZN', 'TSLA', 'VMW', 'DOCU', 'SPLK', 'XLU']

# Get current date
now = datetime.datetime.now().strftime('%Y-%m-%d')

# Create/open csv file for storing data
try:
    file = open('myStocks.csv', 'x')
    writer = csv.writer(file)
    writer.writerow(['Date', 'Ticker', 'Current Price', 'Previous Close', 'Change', '% Change'])
    writer.writerow([now, '', '', '','',''])
except FileExistsError as e:
    file = open('myStocks.csv', 'a')
    writer = csv.writer(file)
    writer.writerow([now, '', '', '','',''])

for stocks in myStocks:
    '''Example of getting just the Current Price and yesterday's closing price'''
    ticker = yf.Ticker(stocks).info
    curr_symbol = ticker['symbol']
    if curr_symbol == 'XLU':
        current_price = ticker['navPrice']
    else:
        current_price = ticker['currentPrice']
    previous_close_price = ticker['regularMarketPreviousClose']
    change = current_price - previous_close_price
    pctChange = ((current_price - previous_close_price) / previous_close_price) * 100
    # if curr_symbol == 'AAPL':
    #     writer.writerow([now, curr_symbol, current_price, previous_close_price])
    # else:
    writer.writerow(['', curr_symbol, current_price, previous_close_price, format(change, '.2f') , format(pctChange, '.2f')])

file.close()


'''Now try to get multiple tickers and print out'''
# # Set the start and end date
# start_date = '2023-08-01'
# end_date = '2023-08-16'

# # Add multiple space separated tickers here
# ticker = 'GOOGL MSFT TSLA'
# data = yf.download(ticker, start_date, end_date)
# print(data.tail)
