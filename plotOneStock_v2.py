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
import customtkinter

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
    def getTicker():
        return entry.get()

    customtkinter.set_appearance_mode('system')

    root = customtkinter.CTk()
    root.geometry('180x100')
    root.title('Enter Ticker')

    frame = customtkinter.CTkFrame(root)
    frame.grid(row=0,column=0)

    label = customtkinter.CTkLabel(frame, text='Enter A Stock Ticker')
    label.grid(row=0, column=0)

    entry = customtkinter.CTkEntry(frame, placeholder_text='AAPL')
    entry.grid(row=1, column=0, padx=20, pady=5)

    btn = customtkinter.CTkButton(frame, text='Enter',width=20, command=lambda:[getTicker(), root.quit()])
    btn.grid(row=2, column=0)
    root.mainloop()

# get_data()- Using yfinance, get stock data for provided stock ticker.
# Requires: 
#   item- the stock ticker to fetch data for 
#
# Returns:
#   stockData- object containing stock data for past year for the provided symbol
#
def get_data(item):
    global dates
    global company_name
    # Pseudo status
    print('Fetching data for', item, '...')
    stockData = yf.download(tickers = item,
                         start= dates[2],
                         end= dates[3])
    cmp = yf.Ticker(item)
    company_name = cmp.info['longName']
    return stockData

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
    fig, ax = plt.subplots(figsize=(13,7))
    sns.set_style('darkgrid')
    ax.set_title('Closing Prices', fontsize=20)

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
    ax.tick_params(axis='both', labelsize=9)

    sns.despine()
    plt.title('{0} Closing Prices\n{1} - {2}'.format(company_name, dates[4], dates[5]), size='x-large', color='black')
    plt.ylabel('Stock Price $ (USD)')
    
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

# main()
#
def main():
    global numdays
    global dates

    # Get the company ticker
    ticker = get_company()

    # Get number of days to look up stock data for
    numdays = get_numdays()

    # Get start/end dates based on numdays
    dates = get_dates(numdays)

    # Fetch the stock data from yfinance
    company_data = get_data(ticker)

    # Create window to display data in, plot the data, then display the data
    plot_window(company_data, ticker)
    
if __name__ == "__main__":
    main()
