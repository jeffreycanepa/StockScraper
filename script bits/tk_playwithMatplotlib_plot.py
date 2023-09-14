# tk_checkboxes.py
# This is a script I am using to work on playing with matplotlib
# plot data.  Try to make is so items in plot can be show/hidden
# with a mouse click.
#
# Jeff Canepa
# 03-09-23

#!/usr/bin/env python
import yfinance as yf
import csv
from tkinter import *
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import seaborn as sns; sns.set()
import pandas as pd
from datetime import datetime, timedelta

dates = []
tickers = []
companies = [] 
company_names = []
company_data = []
cbuts = []
selected_companies = []
# List of lists with seaborn line colors and line styles
linestyle = []
btvars = []
numdays = None
trendline = None

def get_dates(numdays):
    # Date must be in the format ("%Y-%m-%d") That is, year-month-day
    now = datetime.now()
    yfinance_start_date = (now - timedelta(days=numdays)).strftime('%Y-%m-%d')
    yfinance_end_date = now.strftime('%Y-%m-%d')
    start_date = (now - timedelta(days=numdays)).strftime('%b %d, %Y')
    end_date = now.strftime('%b %d, %Y')
    return [yfinance_start_date, yfinance_end_date, start_date, end_date] 

def read_stock_file():
    global tickers
    global company_names
    global linestyle
    try:
        with open('../stocktickers.csv', 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            companies = list(csv_reader)
        for cticker, cname, ccolor, cstyle in companies:
            tickers.append(cticker)
            company_names.append(cname) 
            linestyle.append([ccolor, cstyle])
    except FileNotFoundError as e:
        print(e)
    except:
        print('Something went wrong with accessing file stocktickers.csv')

def get_selected_companies():
    window = Tk()
    window.title('Select Companies')
    window.geometry('200x440')
    tline = IntVar()
    cb = IntVar()

    # Create a LabelFrame
    frame =LabelFrame(window, text="Select the Companies", padx=5, pady=5) #, padx=10, pady=5
    frame.pack(padx=10, pady=10) #pady=20, padx=10

    # Create a frame for checkboxes
    frame2 = Frame(window, padx=5, pady=5)
    frame2.pack(padx=10)

    # Add method to select all checkboxes
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
    Checkbutton(frame2, text='Display Trendline', anchor='w', width=50, variable=tline, onvalue=1, offvalue=0, command=showline).pack()
    Button(window, text='Enter', command=lambda:[set_selected_companies(), window.destroy()]).pack()
                
    window.mainloop()

def set_selected_companies():
    for index, item in enumerate(company_names):
        if btvars[index].get() == 1:
            selected_companies.append([item,tickers[index]])

def get_company_data():
    for item in (selected_companies):
        company_data.append(get_data(item))

def get_data(item):
    global dates
    stockData = yf.download(tickers = item[1],
                         start= dates[0],
                         end= dates[1])
    stockData.name = item[0]
    return stockData

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
#   company_data
#   linestyle
#
# Returns:
#
def plot_window():
    # Create the window
    plotWindow = Tk()
    plotWindow.title('Past ' + str(numdays) + ' Days')
    plotWindow.geometry('1000x770')

    # Using Matplotlib display company stock data
    plot_data(company_data, linestyle, plotWindow)

    # Add a button to quit when done viewing the plot data
    bt_1 = Button(plotWindow, text='Quit', command=plotWindow.quit).pack()

    plotWindow.mainloop() 
    # exit(0)

def main():
    global dates
    global numdays
     # Get number of days to look up stock data for
    numdays = simpledialog.askinteger('Enter Number of Days', 'How many day\'s data do you want?', 
                                      initialvalue=365, minvalue=2, maxvalue=10000)
    dates = get_dates(numdays)
    read_stock_file()
    get_selected_companies()
    get_company_data()
    plot_window()


if __name__ == "__main__":
    main()
    