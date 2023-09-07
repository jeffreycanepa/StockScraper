import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import yfinance
from datetime import datetime, date, timedelta
import tkinter as tk
from tkinter.simpledialog import askinteger


def get_numdays():
    # root = tk.Tk()
    # root.withdraw()
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
    # Date must be in the format ("%Y-%m-%d") That is, year-month-day
    now = datetime.now()
    then = now - timedelta(numdays)
    yfinance_start_date = (now - timedelta(days=numdays)).strftime('%Y-%m-%d')
    yfinance_end_date = now.strftime('%Y-%m-%d')
    start_date = (now - timedelta(days=numdays)).strftime('%b %d, %Y')
    end_date = now.strftime('%b %d, %Y')
    return [now, then, yfinance_start_date, yfinance_end_date, start_date, end_date] 

def main():
    # Get number of days to look up stock data for
    numdays = get_numdays()

    dates = get_dates(numdays)


    stockTickers = ['AAPL', 'ADBE','CSCO', 'NTAP', 'MSFT']
    cn = ["Apple", "Adobe", "Cisco", "NetApp", 'Microsoft']
    stockData = []

    for company in stockTickers:
        cmp = yfinance.download(company, start=dates[2], end=dates[3])
        newcmp = cmp.reset_index()
        stockData.append(newcmp)

    # now = datetime.now()
    then = dates[0] - (timedelta(days=len(stockData[0])))
    days = mdates.drange(then,dates[0],timedelta(days=1))

    mylines = []
    fig, ax = plt.subplots(figsize=(12,7))
    ax.set_title('My Stocks for past year')

    x = 0
    while x <= len(stockData)-1:
        line, = ax.plot(days, stockData[x]['Adj Close'], label=cn[x])
        mylines.append(line,)
        x += 1

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=10))
    ax.tick_params(axis='x', labelrotation=45)

    leg = ax.legend(loc = 'upper left', fancybox=True, shadow=True)
    lined = {}  # Will map legend lines to original lines.
    for legline, origline in zip(leg.get_lines(), mylines):
        legline.set_picker(True)  # Enable picking on the legend line.
        legline.set_picker(5)
        lined[legline] = origline


    def on_pick(event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        legline = event.artist
        origline = lined[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        # Change the alpha on the line in the legend, so we can see what lines
        # have been toggled.
        legline.set_alpha(1.0 if visible else 0.2)
        fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', on_pick)
    plt.show()


if __name__ == "__main__":
    main()

# --------------------------------------------------------------------------
# This is my Maginot line
# --------------------------------------------------------------------------