# Scratch script for practicing code before adding to larger script
from datetime import datetime, timedelta
import getTicker
import numDays
import getCompanyData
import displayData

dates = None
numdays = None
company_name = None
stockData = None


def main():
    global numdays
    global dates
    # Get the Ticker symbol
    getTicker.getTicker()
    # Get number of days to look u
    numDays.getNumDays()  
    # Get start/end dates based on numer of days
    numDays.getDates()
    # Grab the data from yfinance
    getCompanyData.get_data()
    # Create window to display data in, plot the data, then display the data
    displayData.plot_window()

if __name__ == "__main__":
    main()
