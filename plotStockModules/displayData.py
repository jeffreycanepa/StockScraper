# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   displayData.py
-       This module creates a window using tkinter.
-       Matplotlib is then used to plot data within the 
-       tkinter window. Tkinter is also used to ask the 
-       user for a stock ticker and the number of days for
-       which to looking up data for. Though this module does
-       not use yfinance, it is used by module getCompanyData
-       and is therefore listed as a requirement.
-
-   Required Packages (required in imported Modules):
-       yfinance: 0.2.31
-       matplotlib: 3.8.0
-       seaborn: 0.13.0
-       pandas: 2.1.1
-       customtkinter: 5.2.1
-       tkinter: built-in
-       datetime: built-in
-
-   Required Modules:
-       numDays.py
-       getCompanyData.py
-
-   Methods:
-       plot_data()
-       set_winsize()
-       plot_window()
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Dec 2023
--------------------------------------------------------------
'''
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import seaborn as sns; sns.set()
import pandas as pd
from tkinter import *
from tkinter.simpledialog import askinteger, askstring
import plotStockModules.getCompanyData as getCompanyData
import plotStockModules.numDays as numDays

# plot_data()- Plot stock data using Matplotlib and add it to Tkinter window
# Requires:
#   company-   object containing the stock data
#   ticker-    The stock ticker
#   window-    The tkinter window to plot the data to
#  
# Returns:
#
def plot_data(window):
    company_name = getCompanyData.company_name
    company = getCompanyData.stockData
    dates = numDays.dates
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

# set_winsize()- Set the location/size of the window 
#
# Requires:
#   cwindow- The window object
#
# Returns:
#   string of the window dimensions to use.
#
def set_winsize(cwindow):
    winWidth = 800
    winHeight = 780
    x = (cwindow.winfo_screenwidth() / 2) - (winWidth / 2)
    winGeometry = f'{winWidth}x{winHeight}+{int(x)}+{80}'
    return winGeometry

# plot_window()- A tk window for displaying the data plot from plot_data().  Quiting dialog
#               quits the app.
#
# Required:
#   company_data- The object returned by yfinance that contains the stock data
#   ticker-       The stock ticker used to do the lookup
#
# Returns:
#
def plot_window():
    # Create the window
    plotWindow = Tk()
    plotWindow.title(getCompanyData.company_name +  ' Closing Prices')
    
    # size the window
    plotWindow.geometry(set_winsize(plotWindow))

    # Quit window/app if user closes dialog using the window's close widget
    def on_closing():
        plotWindow.destroy()

    # Quit window/app if user uses the Return key
    def on_return(event):
        plotWindow.destroy()
        getCompanyData.fetch_and_plot_data()

    plotWindow.protocol('WM_DELETE_WINDOW', on_closing)

    # lock the window size
    plotWindow.resizable(False, False)

    # Using Matplotlib display company stock data
    plot_data(plotWindow)

    # Add a button to ask for a new stock symbol
    bt_1 = Button(plotWindow, text='Enter New Ticker')
    bt_1.bind('<Return>', on_return)
    bt_1.bind('<Button-1>', on_return)
    bt_1.focus()
    bt_1.pack()

    plotWindow.mainloop() 