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
-       tkinter
-       matplotlib
-       seaborn
-       pandas
-       datetime
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

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd
import seaborn as sns; sns.set()
import yfinance as yf
from datetime import datetime, date, timedelta
from tkinter import *
from tkinter.simpledialog import askinteger
from tkinter import messagebox
import csv
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

# read_stock_file()- Get stock tickers and company name data from file stocktickers.csv
# Requires:
#   External .csv file with stock tickers and company name data
#
# Returns:
#
def read_stock_file():
    global tickers
    global company_names
    global linestyle
    try:
        with open('stocktickers.csv', 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            companies = list(csv_reader)
        for cticker, cname, ccolor, cstyle in companies:
            tickers.append(cticker)
            company_names.append(cname) 
            linestyles.append([ccolor, cstyle])
    except FileNotFoundError as e:
        print(e)
    except:
        print('Something went wrong with accessing file stocktickers.csv')

# get_select_company_winsize()- Set the height of the Select Companies dialog based on 
#                               number of companies listed in company_names
#
# Requires:
#   company_names- a list of the strings that are Company Names
#
# Returns:
#   string of the window dimensions to use for dialog Select Companies
#
def get_select_company_winsize():
    winHeight = 120 + (len(company_names) * 23)
    winGeometry = '200x{}+200+40'
    return winGeometry.format(winHeight)

# get_selected_companies()- Ask user to select the stocks to lookup data for
#
# Requires:
#   company_names- a list of strings that are Company names
#   window- The root window
#
#   Returns:
#
def get_selected_companies():
    winsize = get_select_company_winsize()
    cwindow = Tk()
    cwindow.title('Select Companies')
    cwindow.geometry(winsize)
    # cwindow.eval(f'tk::PlaceWindow {cwindow._w} center')
    tline = IntVar()
    cb = IntVar()

    # Create a LabelFrame
    frame =LabelFrame(cwindow, text="Select the Companies", padx=5, pady=5) #, padx=10, pady=5
    frame.pack(padx=10, pady=10) #pady=20, padx=10

     # Create a frame for checkboxes
    frame2 = Frame(cwindow, padx=8) #, pady=5
    frame2.pack(padx=10)

    # Add method to select/deselect all checkboxes
    def select_deselect_all():
        if cb.get() == 1:
            for i in cbuts:
                i.select()
        else:
            for i in cbuts:
                i.deselect()

    def showline():
        global trendline
        if tline.get() == 1:
            trendline = 1

    # array of the button values
    for x in range(len(company_names)):
        btvars.append(IntVar())

    for index, item in enumerate(company_names):
        cbuts.append(Checkbutton(frame, text=item, anchor='w', width=50, variable=btvars[index], onvalue=1, offvalue=0, command=tline))
        cbuts[index].pack()
    Checkbutton(frame2, text='Select All', anchor='w', width=50, variable=cb, onvalue=1, offvalue=0, command=select_deselect_all).pack()
    # Checkbutton(frame2, text='Display Trendline', anchor='w', width=15, variable=tline, onvalue=1, offvalue=0, command=showline).pack()
    Button(cwindow, text='Enter', command=lambda:[set_selected_companies(), cwindow.destroy()]).pack()

    # Quit window/app if user closes dialog using the window's close widget.  Using sys.exit.
    def on_closing():
        sys.exit()

    cwindow.protocol('WM_DELETE_WINDOW', on_closing)


    cwindow.mainloop()

# set_selected_companies()- Create a list of objects (selected_companies) with company name and
#                           company stock ticker based on returned from get_selected_companies
# Required:
#   company_names
#   btvars
#   selected_companies
#   tickers
#
# Returned:
#  
def set_selected_companies():
    for index, item in enumerate(company_names):
        if btvars[index].get() == 1:
            selected_companies.append([item,tickers[index]])

# get_company_data()- Using selected_companies(), get stock data and store results in list company_data
#
# Required:
#   selected_companies
#
# Returns:
#
def get_company_data():
    for item in (selected_companies):
        company_data.append(get_data(item))

# get_data()- Using yfinance, get stock data for provided stock ticker.
# Requires: 
#   item- the stock ticker to fetch data for 
#
# Returns:
#   stockData- object containing stock data for past year for the provided symbol
#
def get_data(item):
    global dates
    stockData = yf.download(tickers = item[1],
                         start= dates[2],
                         end= dates[3])
    stockData.name = item[0]
    return stockData

# plot_data()- Plot stock data using Matplotlib and add it to Tkinter window
# Requires:
#   company-  a list of company objects containing stock data
#   linestyles-   a list of lists with strings that represent line color and style
#   window-   a tkinter window 
# Returns:
#
def plot_data(company, linestyles, window):
    mylines = []
    fig, ax = plt.subplots(figsize=(13,7))
    sns.set_style('darkgrid')
    ax.set_title('Closing Prices', fontsize=20)

    # Get plot lines for all selected stocks
    x = 0
    while x <= len(company)-1:
        line, = ax.plot(company[x].index.values, company[x]['Adj Close'], label=company_names[x], color=linestyles[x][0], linestyle=linestyles[x][1])
        mylines.append(line,)
        x += 1

    # Format the x and y tickers and labels
    ax.set(ylabel='Stock Price (USD)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    ax.yaxis.set_major_formatter('${x:1.0f}')
    ax.tick_params(axis='x', labelrotation=45)
    ax.tick_params(axis='both', labelsize=9)

    # Adjust the number of tickers depending on number of days worth of
    # stock data there is to plot
    numDates = len(company[0]['Adj Close'])
    if numDates <= 30:
        ax.xaxis.set_minor_locator(mdates.DayLocator())
    elif numDates > 30 and numDates < 120:
        ax.xaxis.set_minor_locator(mdates.DayLocator(interval=2))
    else:
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=4))

    # Map legend lines to plot lines
    leg = ax.legend(loc = 'upper center', fancybox=True, framealpha=0.5, ncols=3, title='Click on marker to hide/show plot line')
    lined = {}
    for legline, origline in zip(leg.get_lines(), mylines):
        legline.set_picker(True)  # Enable picking on the legend line.
        legline.set_picker(5)
        lined[legline] = origline

    # On the pick event, find the original line corresponding to the legend
    # proxy line, and toggle its visibility.
    def on_pick(event):
        legline = event.artist
        origline = lined[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legline.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', on_pick)
    
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
def plot_window():
    # Create the window
    plotWindow = Tk()
    plotWindow.title('Past ' + str(numdays) + ' Days')
    plotWindow.geometry('1000x770+200+10')

    # Quit window/app if user closes dialog using the window's close widget
    def on_closing():
        plotWindow.destroy()

    plotWindow.protocol('WM_DELETE_WINDOW', on_closing)

    # Using Matplotlib display company stock data
    plot_data(company_data, linestyles, plotWindow)

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

    # Get tickers and company names from csv file
    read_stock_file()

    # Get selection of companies from user
    get_selected_companies()

    # Fetch the stock data from yfinance
    get_company_data()

    # Create window to display data in, plot the data, then display the data
    plot_window()
    
if __name__ == "__main__":
    main()
