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
-       get_dates()
-       read_stock_file()
-       get_select_company_winsize()
-       get_selected_companies()
-       set_selected_companies()
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
-   Aug 2023
--------------------------------------------------------------
'''
# Import Stuff
import yfinance as yf
import csv
from tkinter import *
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import seaborn as sns;
import pandas as pd
from datetime import datetime, timedelta
import sys

#Global variables
dates = []
tickers = []
company_names = []
company_data = []
cbuts = []
selected_companies = []
# List of lists with seaborn line colors and line styles
linestyle = []
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
    # root = tk.Tk()
    # root.withdraw()
    numberofdays = simpledialog.askinteger('Enter Number of Days', 'How many day\'s data do you want?', 
                                      initialvalue=365, minvalue=2, maxvalue=10000)
    return numberofdays

# get_dates()- Get start/end dates for stock lookup.
# Requires: 
#   numdays- Number of days to lookup stock data for
# Returns:
#   a list containing start/end dates for yfinance lookup and for matplotlib labels
#
def get_dates(numdays):
    # Date must be in the format ("%Y-%m-%d") That is, year-month-day
    now = datetime.now()
    yfinance_start_date = (now - timedelta(days=numdays)).strftime('%Y-%m-%d')
    yfinance_end_date = now.strftime('%Y-%m-%d')
    start_date = (now - timedelta(days=numdays)).strftime('%b %d, %Y')
    end_date = now.strftime('%b %d, %Y')
    return [yfinance_start_date, yfinance_end_date, start_date, end_date] 

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
            linestyle.append([ccolor, cstyle])
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
    winHeight = 150 + (len(company_names) * 23)
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
    frame2 = Frame(cwindow, padx=5, pady=5)
    frame2.pack(padx=10)

     # Create Enter button
    bt1 = Button(cwindow, text='Enter', state='disabled', command=lambda:[set_selected_companies(), cwindow.destroy()])

    # array of the button values
    for x in range(len(company_names)):
        btvars.append(IntVar())

    for index, item in enumerate(company_names):
        cbuts.append(Checkbutton(frame, text=item, anchor='w', width=50, variable=btvars[index], onvalue=1, offvalue=0, command=is_checkbox_checked))
        cbuts[index].pack()
    Checkbutton(frame2, text='Select All', anchor='w', width=15, variable=cb, onvalue=1, offvalue=0, command=lambda:[select_deselect_all(),is_checkbox_checked()]).pack()
    Checkbutton(frame2, text='Display Trendline', anchor='w', width=15, variable=tline, onvalue=1, offvalue=0, command=showline).pack()
    
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

# get_company_data()- Using selected_companies(), get stock data and store results in list company
#
# Required:
#   selected_companies
#
# Returns:
#
def get_company_data():
    for item in (selected_companies):
        company_data.append(get_data(item))

# get_data()- Get stock data.
# Requires: 
#   symbol- a list of strings that are stock symbols (tickers) 
#   cname-  a list of strings with comany names
# Returns:
#   stockData- object containing stock data for past year for the provided symbol
#
def get_data(item):
    global dates
    print('Fetching data for', item[1], '...')
    stockObject = yf.Ticker(item[1])
    stockData = stockObject.history(start= dates[0],
                            end= dates[1],
                            auto_adjust= False)
    stockData.name = item[0]
    return stockData

# plot_data()- Plot stock data using Matplotlib and add it to Tkinter window
# Requires:
#   company-    a list of company objects containing stock data
#   linestyle-  a list of lists with strings that represent line color and style
#   window-     a tkinter window 
# Returns:
#
def plot_data(company, linestyle, window):
    # Create plot using matplotlib
    fig = plt.figure(figsize=(13, 7))
    sns.set_style('darkgrid')
    
    # convert the regression line start date to ordinal
    x1 = pd.to_datetime(dates[0]).toordinal()

    for cmp, lstyle in zip(company,linestyle):
        # convert the datetime index to ordinal values, which can be used to plot a regression line
        cmp.index = cmp.index.map(pd.Timestamp.toordinal)
        data=cmp.loc[x1:].reset_index()

        # Add Closing price for stock as a line and as a linear regression (trend line)
        ax1 = sns.lineplot(data=cmp,x=cmp.index,y="Close",color=lstyle[0],linestyle=lstyle[1], label=cmp.name)
        
        # If user checked to show trendline, then add trendline to the plot
        if trendline == 1:
            sns.regplot(data=data, x=cmp.index, y='Close', color=lstyle[0], scatter=False, ci=False)

        ax1.set_xlim(cmp.index[0], cmp.index[-1])

        # convert the axis back to datetime
        xticks = ax1.get_xticks()
        labels = [pd.Timestamp.fromordinal(int(label)).date() for label in xticks]
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(labels)

    sns.despine()
    plt.title('Closing Prices\n{0} - {1}'.format(dates[2], dates[3]), size='x-large', color='black')
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
    plot_data(company_data, linestyle, plotWindow)

    # Add a button to quit when done viewing the plot data
    bt_1 = Button(plotWindow, text='Quit', command=plotWindow.quit)
    bt_1.bind('<Return>', on_return)
    bt_1.focus()
    bt_1.pack()

    plotWindow.mainloop() 

# main()
def main():
    global dates

    # Get tickers and company names from csv file
    read_stock_file()

    # Get selection of companies from user
    get_selected_companies()

    # Get number of days to look up stock data for
    numdays = get_numdays()
    dates = get_dates(numdays)

    # Fetch the stock data from yfinance
    get_company_data()

    # Plot the stock data and display
    plot_window()

if __name__ == "__main__":
    main()