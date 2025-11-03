# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   displayData_ctk.py
-       This module creates a window using customtkinter.
-       Matplotlib is then used to plot data within the 
-       customtkinter window.  Customtkinter is also used to
-       ask the user for a stock ticker and to select a start
-       and end date for looking up data for the provided stock 
-       ticker.
-
-   Required Packages:
-       matplotlib: 3.8.0
-       pandas: 2.1.1
-       numpy: 1.26.4
-       customtkinter: 5.2.1
-       tkinter: built-in
-       datetime: built-in
-
-   Required Modules:
-       numDays_ctk.py
-       getCompanyData_ctk.py
-       isMacbookPro.py
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
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import pandas as pd
import numpy as np 
import customtkinter
import plotStockModules.getCompanyData_ctk as getCompanyData
import plotStockModules.numDays_ctk as numDays
import plotStockModules.isMacbookPro as isMacbookPro

# plot_data()- Plot stock data using Matplotlib and add it to Tkinter window
# Requires:
#   company-   object containing the stock data
#   ticker-    The stock ticker
#   window-    The tkinter window to plot the data to
#  
# Returns:
#
def plot_data(window):
    # Adjust the DPI for MacBook Pro displays
    if isMacbookPro.is_macbook_pro():
        mpl.rcParams['figure.dpi'] = 50 # Adjust this value (e.g., 150, 300) for desired size/sharpness
    
    company_name = getCompanyData.company_name
    company = getCompanyData.stockData
    dates = numDays.dates
    fig, ax = plt.subplots(figsize=(8,7))

    # Set mydates to the index of the company data
    mydates = company.index

    # convert the datetime index to ordinal values, which can be used to plot a regression line
    company.index = company.index.map(pd.Timestamp.toordinal)

    # Add Closing price for stock as a line
    ax.plot(mydates, company['Close'], color='blue', label=company_name)

    # Set dates values to numeric values for use in regression line
    mydates = mdates.date2num(mydates)

    # Display regression line
    coefficients_close = np.polyfit(mydates, company['Close'], 1)
    p_close = np.poly1d(coefficients_close)
    ax.plot(mydates, p_close(mydates), color='black', linestyle='dotted', label='Trend Line')

    # Configure title, tick parameters, plot labels, ect.
    ax.set_title('Closing Prices: {0} - {1}'.format(dates[4], dates[5]), size='large', color='black')
    ax.set_facecolor(color='0.95')  # Light Gray background for plot area
    ax.set(ylabel='Stock Price ($ USD)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d \'%y'))
    ax.yaxis.set_major_formatter('${x:1.0f}.00') # Format y-axis labels as $XX.00
    ax.yaxis.set_major_locator(MaxNLocator(nbins=15))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=20))
    ax.tick_params(axis='x', rotation=45)
    ax.tick_params(axis='both', labelsize=7)
    ax.grid(True, linestyle='--', linewidth=0.5)
    ax.legend()
    
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
    plotWindow = customtkinter.CTk()
    # plotWindow.title('Past ' + str(numDays.days) + ' Days')
    plotWindow.title(getCompanyData.company_name + ' Closing Price')
    
    # size the window
    plotWindow.geometry(set_winsize(plotWindow))

    # Quit window/app if user closes dialog using the window's close widget
    def on_closing():
        plotWindow.destroy()
    plotWindow.protocol('WM_DELETE_WINDOW', on_closing)

    # Quit window/app if user uses Return key
    def on_return(event):
        plotWindow.destroy()
        getCompanyData.get_data_using_calendar()

    # Using Matplotlib display company stock data
    plot_data(plotWindow)

    # Add a button to quit when done viewing the plot data
    bt_1 = customtkinter.CTkButton(plotWindow, text='Enter New Ticker', width=20, height=12)
    bt_1.bind('<Return>', on_return)
    bt_1.bind('<Button-1>', on_return)
    bt_1.focus()
    bt_1.pack(pady=10)

    plotWindow.mainloop() 