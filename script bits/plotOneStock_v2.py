# Scratch script for practicing code before adding to larger script
import plotStockModules.getTicker_ctk as getTicker
import plotStockModules.numDays_ctk as numDays
import plotStockModules.getCompanyData as getCompanyData
import plotStockModules.displayData_ctk as displayData

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
