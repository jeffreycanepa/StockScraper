# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   plotStocks_v2.py
-       This script asks for user to select stocks from a list
-       provided by .csv file.  It then looks up stock data
-       using yfinance for the selected stocks. 
-       Matplotlib is then used to plot the closing price for the
-       past x number of days and displays the plot in a tkinter
-       window.
-
-       The user can click on the legend items to hide/show the
-       corresponding stock data.
-
-   Requires:
-       yfinance
-       csv
-       matplotlib
-       pandas
-       numpy
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
-   are read in from .csv file 'stocktickers.csv'.  The file should
-   consist of a row of data for every stock you wish to lookup.
-   Required columns are: 
-       A: Stock ticker 
-       B: Company Name
-       C: seaborn line color
-       D: seaborn line style
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Sep 2023
--------------------------------------------------------------
'''

from matplotlib.ticker import MaxNLocator
import yfinance as yf
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tkinter import *
from tkinter.simpledialog import askinteger
import sys
from textwrap import fill

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
        print('You need to create a csv file named \"stocktickers.csv\" and add\n',
               'company ticker, company name, line color and line style.\n',
               'Example: \"AAPL,Apple,blue,solid\"')
        sys.exit()
    except:
        print('Something went wrong with accessing file stocktickers.csv')
        sys.exit()

# get_select_company_winsize()- Set the height of the Select Companies dialog based on 
#                               number of companies listed in company_names
#
# Requires:
#   company_names- a list of the strings that are Company Names
#
# Returns:
#   string of the window dimensions to use for dialog Select Companies
#
def get_select_company_winsize(cwindow):
    winWidth = 200
    winHeight = 120 + (len(company_names) * 23)
    x = (cwindow.winfo_screenwidth() / 2) - (winWidth / 2)
    y = (cwindow.winfo_screenheight() / 2) - ((winHeight / 2) + 60)
    winGeometry = f'{winWidth}x{winHeight}+{int(x)}+{int(y)}'
    return winGeometry

# get_selected_companies()- Ask user to select the stocks to lookup data for
#
# Requires:
#   company_names- a list of strings that are Company names
#   window- The root window
#
#   Returns:
#
def get_selected_companies():
    cwindow = Tk()
    winsize = get_select_company_winsize(cwindow)
    cwindow.title('Select Companies')
    cwindow.geometry(winsize)
    tline = IntVar()
    cb = IntVar()

    # Set selected companies and quit the window 
    def on_return(event):
        set_selected_companies()
        cwindow.destroy()

    # Method to validate is any checkbuttons are checked. If they are, then enable the enter button.
    def is_checkbox_checked():
        my_flag=False
        # ischecked = False
        for index, item in enumerate(company_names):
            if btvars[index].get() == 1:
                my_flag = True               
        if my_flag == True:
            bt1.config(state='normal')
        else:
            bt1.config(state='disabled')

    # Method to select/deselect all checkboxes
    def select_deselect_all():
        if cb.get() == 1:
            for i in cbuts:
                i.select()
        else:
            for i in cbuts:
                i.deselect()

    # Method to set trendline to 1 if the checkbutton in the Select Stocks dialog is checked
    def showline():
        global trendline
        if tline.get() == 1:
            trendline = 1
    
    # Create a LabelFrame
    frame =LabelFrame(cwindow, text="Select the Companies", padx=5, pady=5) #, padx=10, pady=5
    frame.pack(padx=10, pady=10) #pady=20, padx=10

     # Create a frame for checkboxes
    frame2 = Frame(cwindow, padx=8) #, pady=5
    frame2.pack(padx=10)

     # Create Enter button
    bt1 = Button(cwindow, text='Enter', state='disabled', command=lambda:[set_selected_companies(), cwindow.destroy()])
    
    # array of the button values
    for bt in range(len(company_names)):
        btvars.append(IntVar())

    for index, item in enumerate(company_names):
        cbuts.append(Checkbutton(frame, text=item, anchor='w', width=50, variable=btvars[index], onvalue=1, offvalue=0, command=is_checkbox_checked))
        cbuts[index].pack()
    Checkbutton(frame2, text='Select All', anchor='w', width=50, variable=cb, onvalue=1, offvalue=0, command=lambda:[select_deselect_all(),is_checkbox_checked()]).pack()

    # Bind Return key to Button
    bt1.bind('<Return>', on_return)
    bt1.pack()

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
    # Pseudo status
    print('Fetching data for', item[0], '...')
    stockObject = yf.Ticker(item[1])
    stockData = stockObject.history(start= dates[2],
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
    ax.set_title('Closing Prices\n{0} - {1}'.format(dates[4], dates[5]), size='x-large', color='black')
    ax.set_facecolor(color='0.95')  # Light Gray background for plot area

    # Get plot lines for all selected stocks
    x = 0
    while x <= len(company)-1:
        mydates = company[x].index
        company[x].index.map(pd.Timestamp.toordinal)
        line, = ax.plot(company[x].index, company[x]['Close'], label=selected_companies[x][0], color=linestyles[x][0], linestyle=linestyles[x][1])
        
        mydates = mdates.date2num(mydates)

        # Add trendline
        coefficients = np.polyfit(mydates, company[x]['Close'], 1)
        p_close = np.poly1d(coefficients)
        line2, = ax.plot(mydates, p_close(mydates), linestyle='--', label=selected_companies[x][1], color=linestyles[x][0])

        mylines.append(line,)
        mylines.append(line2,)
        x += 1

    # Format the x and y tickers and labels
    ax.set(ylabel='Stock Price (USD)')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d \'%y'))
    ax.yaxis.set_major_formatter('${x:1.0f}.00')
    ax.yaxis.set_major_locator(MaxNLocator(nbins=15))
    ax.xaxis.set_major_locator(MaxNLocator(nbins=20))
    ax.tick_params(axis='x', labelrotation=45)
    ax.tick_params(axis='both', labelsize=9)
    ax.grid(True, linestyle='--', linewidth=0.5)

    # Shrink current axis by 10% so legend fits in window
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])  

    # Place legend and set the title with wrapped text
    leg = ax.legend(fancybox=True, framealpha=0.5, ncols=1, bbox_to_anchor=(1.01, 1.01), fontsize=9, title_fontsize=10, handlelength=1.5)
    leg.set_title(fill('Click on item to hide/show line', width=20))
    
    # Map legend lines to original lines, enable picking on the legend line
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

    # Set Window size and center on screen
    width = 1000
    height = 770
    x = (plotWindow.winfo_screenwidth() / 2) - (width / 2)
    y = (plotWindow.winfo_screenheight() / 2) - ((height / 2) + 60)
    plotWindow.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    # Quit window/app if user closes dialog using the window's close widget
    def on_closing():
        plotWindow.destroy()

    plotWindow.protocol('WM_DELETE_WINDOW', on_closing)

    def on_return(event):
        plotWindow.destroy()

    # Using Matplotlib display company stock data
    plot_data(company_data, linestyles, plotWindow)

    # Add a button to quit when done viewing the plot data
    bt_1 = Button(plotWindow, text='Quit', command=plotWindow.quit)
    bt_1.bind('<Return>', on_return)
    bt_1.focus()
    bt_1.pack()

    plotWindow.mainloop() 

def main():
    global numdays
    global dates
    
    # Get tickers and company names from csv file
    read_stock_file()

    # Get selection of companies from user
    get_selected_companies()

    # Get number of days to look up stock data for
    numdays = get_numdays()

    # Get start/end dates based on numdays
    dates = get_dates(numdays)

    # Fetch the stock data from yfinance
    get_company_data()

    # Create window to display data in, plot the data, then display the data
    plot_window()
    
if __name__ == "__main__":
    main()
