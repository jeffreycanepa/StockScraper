# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   plotOneStock.py
-       This script looks up the Adjusted Closing Price 
-       for one stock and plots the data to a window that
-       displays the closing price and a trend line for the 
-       stock.
-
-   Requires:
-       yfinance
-       matplotlib
-       seaborn
-       pandas
-       datetime
-       tkinter
-
-   Methods:
-       get_numdays()
-       get_dates()
-       get_company()
-       get_company_name()
-       get_data()
-       plot_data()
-       plot_window()
-       main()
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Sep 2023
--------------------------------------------------------------
'''

import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import seaborn as sns; sns.set()
import pandas as pd
from datetime import datetime, timedelta
from tkinter import *
from tkinter.simpledialog import askinteger, askstring

#Global variables
dates = []
company_name = None

# get_numdays()- Get number of days to lookup stock data for
# Requires: 
#   
# Returns:
#   an integer with the number of days input by user
#
def get_numdays():
    numberofdays = askinteger('Enter Number of Days', 'How many day\'s data do you want?', 
                                      initialvalue=365, minvalue=2, maxvalue=10000)
    return numberofdays

# get_dates()- Get start/end dates for stock lookup.
# Requires: 
#   numdays- Number of days to lookup stock data for
# Returns:
#   a list containing start/end dates for yfinance lookup and for matplotlib labels
#
def get_dates(numdays):
    now = datetime.now()
    then = now - timedelta(numdays)
    # yfinance dates must be in the format ("%Y-%m-%d") That is, year-month-day
    yfinance_start_date = (now - timedelta(days=numdays)).strftime('%Y-%m-%d')
    yfinance_end_date = (now + timedelta(days=1)).strftime('%Y-%m-%d')
    # date strings I use in the UI are in format ("%b %d, %Y")
    start_date = (now - timedelta(days=numdays)).strftime('%b %d, %Y')
    end_date = now.strftime('%b %d, %Y')
    return [now, then, yfinance_start_date, yfinance_end_date, start_date, end_date] 

# get_company()- Get the stock ticker to look up
#
# Requires:
# 
# Returns:
#   string with the stock ticker to look up
#  

def get_company():
    myTicker = askstring('Enter Ticker', 'Enter the stock ticker:')
    return myTicker.upper()

# get_data()- Using yfinance, get stock data for provided stock ticker.
# Requires: 
#   item- the stock ticker to fetch data for 
#
# Returns:
#   stockData- object containing stock data for past year for the provided symbol
#
def get_stock_data(item):
    global dates
    global company_name
    # Pseudo status
    print('Fetching data for', item, '...')
    stockData = yf.download(tickers = item,
                         start= dates[2],
                         end= dates[3])
    cmp = yf.Ticker(item)
    try:
        # company_name = cmp.info['longName']

        # yfinance info seems to be flakey, so get company name by other means
        company_name = get_company_name(item)
    except:
        company_name = item
    return stockData

# get_company_name()- Get company name using it's stock ticker
# Requires: 
#   ticker- the stock ticker to fetch data for 
#
# Returns:
#   result- The name of the company
#
def get_company_name(ticker):
    import requests, re

    url = 'https://finance.yahoo.com/quote/WMT/'
    url = url.replace("WMT",ticker)

    req = requests.get(url)
    html = req.text

    name = re.search(r'\<title>([^\s]+)\ ([^\s]+)', html)
    result = str(name.group(0))
    result = result.replace("<title>", "")
    return result

# get_data()- Run all the methods needed to execute the script
# Requires: 
#
# Returns:
#
def get_data():
    global numdays
    global dates
    global ticker
    global company_data

    # Get the company ticker
    ticker = get_company()

    # Get number of days to look up stock data for
    numdays = get_numdays()

    # Get start/end dates based on numdays
    dates = get_dates(numdays)

    # Fetch the stock data from yfinance
    company_data = get_stock_data(ticker)

    # Create window to display data in, plot the data, then display the data
    plot_window(company_data, ticker)
    
# plot_data()- Plot stock data using Matplotlib and add it to Tkinter window
# Requires:
#   company-   object containing the stock data
#   ticker-    The stock ticker
#   window-    The tkinter window to plot the data to
#  
# Returns:
#
def plot_data(company, ticker, window):
    global company_name
    fig, ax = plt.subplots(figsize=(8,7))
    sns.set_style('darkgrid')
    # ax.set_title('Closing Prices', fontsize=7)

    # convert the regression line start date to ordinal
    x1 = pd.to_datetime(dates[0]).toordinal()

    # convert the datetime index to ordinal values, which can be used to plot a regression line
    company.index = company.index.map(pd.Timestamp.toordinal)
    data=company.loc[x1:].reset_index()

     # Add Closing price for stock as a line and as a linear regression (trend line)
    ax1 = sns.lineplot(data=company,x=company.index,y='Adj Close', color='blue', label=company_name)
    sns.regplot(data=company, x=company.index, y='Adj Close', color='black', scatter=False, ci=False)
   
    ax1.set_xlim(company.index[0], company.index[-1])

    # convert the axis back to datetime
    xticks = ax1.get_xticks()
    labels = [pd.Timestamp.fromordinal(int(label)).strftime('%b %d, \'%y') for label in xticks]
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(labels)
    ax.tick_params(axis='x', labelrotation=45)
    ax.tick_params(axis='both', labelsize=7)

    sns.despine()
    plt.title('{0} Closing Prices: {1} - {2}'.format(company_name, dates[4], dates[5]), size='large', color='black')
    plt.ylabel('Stock Price $ (USD)')
    plt.xlabel('')
    
    # Create canvas and add it to Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

# plot_window()- A tk window for displaying the data plot from plot_data().  Quiting dialog
#               quits the app.
#
# Required:
#   company_data- The object returned by yfinance that contains the stock data
#   ticker-       The stock ticker used to do the lookup
#
# Returns:
#
def plot_window(company_data, ticker):
    # Create the window
    plotWindow = Tk()
    width = 800
    height = 760
    x = (plotWindow.winfo_screenwidth() / 2) - (width / 2)
    y = (plotWindow.winfo_screenheight() / 2) - ((height / 2) + 60)
    plotWindow.title(company_name +  ' Closing Prices')
    plotWindow.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    # Quit window/app if user closes dialog using the window's close widget
    def on_closing():
        plotWindow.destroy()

    # Quit window/app if user uses the Return key
    def on_return(event):
        plotWindow.destroy()
        get_data()

    plotWindow.protocol('WM_DELETE_WINDOW', on_closing)

    # lock the window size
    plotWindow.resizable(False, False)

    # Using Matplotlib display company stock data
    plot_data(company_data, ticker, plotWindow)

    # Add a button to ask for a new stock symbol
    bt_1 = Button(plotWindow, text='Enter New Ticker', command=lambda:[plotWindow.destroy(), get_data()])
    bt_1.bind('<Return>', on_return)
    bt_1.focus()
    bt_1.pack()

    plotWindow.mainloop() 

# main()
#
def main():
    # Get Stock Data and plot it
    get_data()

if __name__ == "__main__":
    main()
