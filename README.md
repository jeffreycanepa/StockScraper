These are a couple of Python3 scripts that I am working on to practice coding in Python.
    stockData-scraper.py: This script uses requests, BeautifulSoup and Scraperapi.com to extract
        stock data from https://www.investing.com.
        Output is to a csv file.

    yFinanceStockData.py: This script uses the yfinance extension to get stock data.
        Output is to a csv file.

    getStocks.py-  This script uses yFinance to get financial data then saves the data
        to a xlsx file using openpyxl.  Requires a .csv file with stock ticker/company name (stocktickers.csv).  Produces .xlsx file (myStocks.xlsx).

    plotStocks.py- Script that gets the last 365 days of stock data for provided stocks
        and uses matplotlib to plot the closing prices
        Requires: 
            yfinance
            matplotlib
            seaborn
            csv
            datetime.
            .csv file (stocktickers.csv) that contains stock tickers / company names.
