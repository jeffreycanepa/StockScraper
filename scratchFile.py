# Scratch script for practicing code before adding to larger script
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from tkinter import simpledialog


def get_numdays():
    return simpledialog.askinteger('Enter Number of Days', 'How many day\'s data do you want?', 
                                      initialvalue=365, minvalue=2, maxvalue=10000)

def get_dates(numdays):
    # Date must be in the format ("%Y-%m-%d") That is, year-month-day
    now = datetime.now()
    then = now - timedelta(numdays)
    yfinance_start_date = (now - timedelta(days=numdays)).strftime('%Y-%m-%d')
    yfinance_end_date = now.strftime('%Y-%m-%d')
    start_date = (now - timedelta(days=numdays)).strftime('%b %d, %Y')
    end_date = now.strftime('%b %d, %Y')
    return [yfinance_start_date, yfinance_end_date, start_date, end_date, now, then] 

# Get number of days to look up stock data for
numdays = get_numdays()
dates = get_dates(numdays)

# print(dates)

# now = datetime.now()
# then = now - timedelta(days=365)
days = mdates.drange(dates[5], dates[4],timedelta(days=1))
print(days)
