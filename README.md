# StockScraper
These are some Python3 scripts that I am working on to practice coding in Python.
## stockData-scraper.py:
This script uses requests, BeautifulSoup and Scraperapi.com to extract stock data from https://www.investing.com. Output is to a csv file.

## plotOneStock.py:
This script uses the yfinance extension to get stock data for a stock ticker provided by the user. The Adjusted Closing Price is plotted along with a trend line.

## getStocks.py-  
This script uses yFinance to get financial data then saves the data to a xlsx file using openpyxl.  Requires a .csv file with stock ticker/company name(stocktickers.csv).  Produces .xlsx file (myStocks.xlsx).

## plotStocks.py- 
Script that gets the last x days of stock data for provided stocks and uses matplotlib to plot the closing prices

#### Requires: 
- yfinance
- matplotlib
- seaborn
- csv
- datetime
- .csv file (stocktickers.csv) that contains stock tickers / company names.
    The csv file is looking for the following columns for each row (company).
- - Ticker: (The company ticker on NYSE or  Nasdaq)
- - Company Name: The Company name
- - Color: A seaborn compliant color to use in the data plot
- - Style: A seaborn compliant line style to use in the data plot