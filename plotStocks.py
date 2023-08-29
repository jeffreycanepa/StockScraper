'''
--------------------------------------------------------------
-   plotStocks.py
-       This script looks up the provided stocks then uses
-       matplotlib to plot the closing price for the past 
-       365 days
-
-   Requires:
-       yfinance
-       matplotlib
-       seaborn
-       datetime
-
-   Methods:
-       get_dates()
-       read_stock_file()
-       get_data()
-       plot_data()
-
--------------------------------------------------------------
'''
# Import Stuff
import yfinance as yf
import csv
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
from datetime import datetime, timedelta

#Global variables
dates = []
ticker = []
company = []
company_names = []
colors = ['blue', 'red', 'black', 'yellow', 'orange', 'green', 'navy',
          'hotpink', 'lightsteelblue', 'mediumspringgreen', 'grey',
          'sandybrown']

# get_dates()- Get start/end dates for stock lookup.
# Requires: 
#
# Returns:
#   a list containing start/end dates
def get_dates():
    # Date must be in the format ("%Y-%m-%d") That is, year-month-day
    now = datetime.now()
    start_date = (now - timedelta(days=365)).strftime('%Y-%m-%d')
    end_date = now.strftime('%Y-%m-%d')
    return [start_date, end_date] 

# read_stock_file()- Get stock ticker and company name data from file stocktickers.csv
# Requires:
#   External .csv file with stock ticker and company name data
#
# Returns:
#
def read_stock_file():
    global ticker
    global company_names
    try:
        with open('stocktickers.csv', 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            companys = list(csv_reader)
        for cticker, cname in companys:
            ticker.append(cticker)
            company_names.append(cname) 
    except FileNotFoundError as e:
        print(e)
    except:
        print('Something went wrong with accessing file stocktickers.csv')

# get_data()- Get stock data.
# Requires: 
#   symbol- a list of strings that are stock symbols (tickers) 
#   cname- a list of strings with comany names
# Returns:
#   stockData- object containing stock data for past year for the provided symbol
def get_data(symbol, cname):
    stockData = yf.download(tickers = symbol,
                         start= dates[0],
                         end= dates[1])
    stockData.name = cname
    return stockData

# plot_data()- Plot stock data using Matplotlib.  
# Requires:
#   company-  a list of company objects containing stock data
#   colors-   a list of strings that are colors used by Matplotlib
# Returns:
#
def plot_data(company, colors):
    plt.figure(figsize=(16, 9))
    sns.set_style('ticks')
    for cmp, clr in zip(company,colors):
        sns.lineplot(data=cmp,x="Date",y="Close",color=clr,linewidth=2.5, label=cmp.name)
    sns.despine()
    plt.title('Closing Prices\n{0} - {1}'.format(dates[0], dates[1]), size='x-large', color='black')
    plt.ylabel('Stock Price $')
    plt.show()

# main()
def main():
    global dates
    global ticker
    global company_names
    dates = get_dates()

    # Get tickers and company names from csv file
    read_stock_file()

    # Populate list company[] with stock data for the provided ticker
    for cmp, name in zip(ticker, company_names):
        company.append(get_data(cmp, name))

    # Using Matplotlib display company stock data
    plot_data(company, colors)

if __name__ == "__main__":
    main()