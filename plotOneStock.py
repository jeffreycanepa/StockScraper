# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   plotStocks.py
-       This script looks up the provided stocks then uses
-       matplotlib to plot the closing price for the past 
-       365 days and displays the plot in a tkinter window
-
-   Requires:
-       yfinance
-       csv
-       matplotlib
-       seaborn
-       datetime
-       tkinter
-       sys
-
-   Methods:
-       get_numdays()
-       get_dates()
-       read_stock_file()
-       get_select_company_winsize()
-       get_selected_companies()
-       set_selected_companies()
-       get_company_data()
-       get_data()
-       plot_data()
-       plot_window()
-       main()
-
-   Data for stock ticker, company name, line color and line style
-       are read in from .csv file stocktickers.csv.  The file should
-       consist of a row of data for every stock you wish to lookup.
-       Required columns are: 
-           A: Stock ticker 
-           B: Company Name
-           C: seaborn line color
-           D: seaborn line style
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Sep 2023
--------------------------------------------------------------
'''

import yfinance as yf
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import seaborn as sns; sns.set()
import pandas as pd
from datetime import datetime, timedelta
from tkinter import *
from tkinter.simpledialog import askinteger, askstring
import sys

#Global variables
dates = []
tickers = []
company_names = []
company_data = []
cbuts = []
selected_companies = []
# List of lists with seaborn line colors and line styles
linestyles = []
btvars = []
numdays = None
trendline = None

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

def get_company():
    return askstring('Enter Ticker', 'Enter the stock ticker:')

# get_data()- Using yfinance, get stock data for provided stock ticker.
# Requires: 
#   item- the stock ticker to fetch data for 
#
# Returns:
#   stockData- object containing stock data for past year for the provided symbol
#
def get_data(item):
    global dates
    # Pseudo status
    print('Fetching data for', item, '...')
    stockData = yf.download(tickers = item,
                         start= dates[2],
                         end= dates[3])
    # stockData.name = item[0]
    return stockData

# plot_data()- Plot stock data using Matplotlib and add it to Tkinter window
# Requires:
#   company-  a list of company objects containing stock data
#   linestyles-   a list of lists with strings that represent line color and style
#   window-   a tkinter window 
# Returns:
#
def plot_data(company, ticker, window):
    mylines = []
    fig, ax = plt.subplots(figsize=(13,7))
    sns.set_style('darkgrid')
    ax.set_title('Closing Prices', fontsize=20)

    # convert the regression line start date to ordinal
    x1 = pd.to_datetime(dates[0]).toordinal()

    # convert the datetime index to ordinal values, which can be used to plot a regression line
    company.index = company.index.map(pd.Timestamp.toordinal)
    data=company.loc[x1:].reset_index()

     # Add Closing price for stock as a line and as a linear regression (trend line)
    ax1 = sns.lineplot(data=company,x=company.index,y='Adj Close', color='blue', label=ticker)
    sns.regplot(data=company, x=company.index, y='Adj Close', color='black', scatter=False, ci=False)
   
    ax1.set_xlim(company.index[0], company.index[-1])

    # convert the axis back to datetime
    xticks = ax1.get_xticks()
    labels = [pd.Timestamp.fromordinal(int(label)).date() for label in xticks]
    ax1.set_xticks(xticks)
    ax1.set_xticklabels(labels)

    sns.despine()
    plt.title('Closing Prices\n{0} - {1}'.format(dates[2], dates[3]), size='x-large', color='black')
    plt.ylabel('Stock Price $ (USD)')
    # line, = ax.plot(company.index.values, company['Adj Close'], label=ticker)
    # mylines.append(line,)

    # # Format the x and y tickers and labels
    # ax.set(ylabel='Stock Price (USD)')
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    # ax.yaxis.set_major_formatter('${x:1.0f}')
    # ax.tick_params(axis='x', labelrotation=45)
    # ax.tick_params(axis='both', labelsize=9)

    # # Adjust the number of tickers depending on number of days worth of
    # # stock data there is to plot
    # numDates = len(company['Adj Close'])
    # if numDates <= 30:
    #     ax.xaxis.set_minor_locator(mdates.DayLocator())
    # elif numDates > 30 and numDates <= 120:
    #     ax.xaxis.set_minor_locator(mdates.DayLocator(interval=2))
    # elif numDates > 120 and numDates <= 730:
    #     ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
    # else:
    #     ax.xaxis.set_major_locator(mdates.YearLocator())

    # # Map legend lines to plot lines
    # leg = ax.legend(loc = 'upper center', fancybox=True, framealpha=0.5, ncols=3, title='Click on marker to hide/show plot line')
    # lined = {}
    # for legline, origline in zip(leg.get_lines(), mylines):
    #     legline.set_picker(True)  # Enable picking on the legend line.
    #     legline.set_picker(5)
    #     lined[legline] = origline

    # # On the pick event, find the original line corresponding to the legend
    # # proxy line, and toggle its visibility.
    # def on_pick(event):
    #     legline = event.artist
    #     origline = lined[legline]
    #     visible = not origline.get_visible()
    #     origline.set_visible(visible)
    #     # Change the alpha on the line in the legend, so we can see what lines
    #     # have been toggled.
    #     legline.set_alpha(1.0 if visible else 0.2)
    #     fig.canvas.draw()

    # fig.canvas.mpl_connect('pick_event', on_pick)
    
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
#
# Returns:
#
def plot_window(company_data, ticker):
    # Create the window
    plotWindow = Tk()
    plotWindow.title('Past ' + str(numdays) + ' Days')
    plotWindow.geometry('1000x770+200+40')

    # Quit window/app if user closes dialog using the window's close widget
    def on_closing():
        plotWindow.destroy()

    plotWindow.protocol('WM_DELETE_WINDOW', on_closing)

    # Using Matplotlib display company stock data
    plot_data(company_data, ticker, plotWindow)

    # Add a button to quit when done viewing the plot data
    bt_1 = Button(plotWindow, text='Quit', command=plotWindow.quit).pack()

    plotWindow.mainloop() 

def main():
    global numdays
    global dates
    # Get number of days to look up stock data for
    numdays = get_numdays()

    # Get start/end dates based on numdays
    dates = get_dates(numdays)

    # Get the company ticker
    ticker = get_company()

    # Fetch the stock data from yfinance
    company_data = get_data(ticker)

    # Create window to display data in, plot the data, then display the data
    plot_window(company_data, ticker)
    
if __name__ == "__main__":
    main()