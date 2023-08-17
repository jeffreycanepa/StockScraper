# /opt/homebrew/bin/python3

import yfinance as yf
import datetime
import csv

# Calculate the difference between today's price and yesterday's price
def getChange(curPrice, oldPrice):
    return curPrice - oldPrice

# Calulate the pecent change from today's price and yesterday's price
def getPercentChange(curPrice, oldPrice):
    return ((curPrice - oldPrice) / oldPrice) * 100

# Using myStocks, get stock data on each stock and write it out to file
def checkStocks(writer):
    '''To Do: 
    1) Read in stocks from a file. 
    2) Add UI to add/remove stocks 
    '''
    # My Stocks
    myStocks = ['AAPL', 'ADBE', 'CSCO', 'NTAP', 'MSFT', 'AMZN', 'TSLA', 'VMW', 'DOCU', 'SPLK', 'XLU']

    for stocks in myStocks:
        ticker = yf.Ticker(stocks).info
        curr_symbol = ticker['symbol']
        # For reasons unknown to me, XLU does not have currentPrice as part of Yahoo Finance ticker info.
        # Use navPrice instead
        if curr_symbol == 'XLU':
            current_price = ticker['navPrice']
        else:
            current_price = ticker['currentPrice']
        previous_close_price = ticker['regularMarketPreviousClose']
        change = getChange(current_price, previous_close_price)
        pctChange = getPercentChange(current_price, previous_close_price)
    
        # Write out the data
        writer.writerow(['', curr_symbol, current_price, previous_close_price, format(change, '.2f') , format(pctChange, '.2f')])


def main():
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
    
    checkStocks(writer)
    file.close()


if __name__ == "__main__":
    main()
