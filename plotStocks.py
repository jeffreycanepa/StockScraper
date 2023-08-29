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
-       datetime
-
-   Methods:
-       get_dates()
-       read_stock_file()
-       get_data()
-       plot_data()
-       main()
-
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
#
def get_data(symbol, cname):
    stockData = yf.download(tickers = symbol,
                         start= dates[0],
                         end= dates[1])
    stockData.name = cname
    return stockData

# plot_data()- Plot stock data using Matplotlib and add it to Tkinter window
# Requires:
#   company-  a list of company objects containing stock data
#   colors-   a list of strings that are colors used by Matplotlib
#   window-   a tkinter window 
# Returns:
#
def plot_data(company, colors, window):
    # Create plot using matplotlib
    fig = plt.figure(figsize=(13, 7))
    sns.set_style('ticks')
    for cmp, clr in zip(company,colors):
        sns.lineplot(data=cmp,x="Date",y="Close",color=clr,linewidth=2.5, label=cmp.name)
    sns.despine()
    plt.title('Closing Prices\n{0} - {1}'.format(dates[2], dates[3]), size='x-large', color='black')
    plt.ylabel('Stock Price $')
    
    # Create canvas and add it to Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()
  
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

# main()
def main():
    global dates
    global ticker
    global company_names

    # Get tickers and company names from csv file
    read_stock_file()

    # Create the window
    window = Tk()
    window.title('Plot Stocks')
    window.geometry('1000x730')

    # Get number of days to look up stock data for
    numdays = simpledialog.askinteger('Enter Number of Days', 'How many day\'s data do you want?', minvalue=2, maxvalue=10000, parent=window)
    dates = get_dates(numdays)

    window.title(str(numdays) + ' days')

    # Populate list company[] with stock data for the provided ticker
    for cmp, name in zip(ticker, company_names):
        company.append(get_data(cmp, name))
    


    # Using Matplotlib display company stock data
    plot_data(company, colors, window)

    window.mainloop()

if __name__ == "__main__":
    main()