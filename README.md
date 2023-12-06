# StockScraper
These are some Python3 scripts that I am working on to practice coding in Python.
## stockData-scraper.py:
This script uses requests, BeautifulSoup and Scraperapi.com to extract stock data from https://www.investing.com. Output is to a csv file.

## getStocks.py-  
This script uses yFinance to get financial data then saves the data to a xlsx file using openpyxl.  Requires a .csv file with stock ticker/company name(stocktickers.csv).  Produces .xlsx file (myStocks.xlsx) with a tab for each company listed in the stocktickers.csv file.

## plotStocks.py- 
A set of scripts that use yfinance to get the last x days of stock data for provided stocks and uses matplotlib to plot the adjusted closing prices

### plotStocks_v1.py
This script uses tkinter to ask the user which of the stocks found in file stockktickers.csv to look up data for.  User has the option of adding a trend line to the plot.  Lookups can be from 2 to 10,000 days.
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

### plotStocks_v2.py
This script uses tkinter to ask the user which of the stocks found in file stockktickers.csv to look up data for. Lookups can be from 2 to 10,000 days.  User can toggle visibility of a stock plot by clicking on the colored line next to the company name in the plot index.
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

## plotOneStock.py- 
A set of scripts that use yfinance to get the adjusted closing price of a single stock for the last x days.  User is promted to enter a stock ticker then matplotlib is used to display the closing prices.

### plotOneStock_v1.py
This script uses tkinter to ask the user which stock ticker to look up data for.  It then asks how many days of data to look up.  
#### Requires: 
- yfinance
- matplotlib
- seaborn
- pandas
- tkinter
- datetime
- plotStockModules
- - displayData.py
- - getCompanyData.py
- - getTicker.py
- - numDays.py

### plotOneStock_ctk_v2.py
This script uses customtkinter to ask the user which stock ticker to look up data for.  It then asks how many days of data to look up.  
#### Requires: 
- yfinance
- matplotlib
- seaborn
- pandas
- tkinter
- customtkinter
- datetime
- plotStockModules
- - displayData_ctk.py
- - getCompanyData_ctk.py
- - getTicker_ctk.py
- - numDays_ctk.py

### plotOneStock_ctk_v3.py
This script uses customtkinter to ask the user which stock ticker to look up data for.  It then uses tkcalendar to allow
the user to select a start/end date.
#### Requires: 
- yfinance
- matplotlib
- seaborn
- pandas
- tkinter
- customtkinter
- tkcalendar
- datetime
- plotStockModules
- - displayData_ctk.py
- - getCompanyData_ctk.py
- - getTicker_ctk.py
- - numDays_ctk.py