# Scratch script for practicing code before adding to larger script
import plotStockModules.getTicker_ctk as getTicker
import plotStockModules.numDays_ctk as numDays_ctk
import plotStockModules.getCompanyData_ctk as getCompanyData_ctk
import plotStockModules.displayData_ctk as displayData_ctk

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
    numDays_ctk.getNumDays()  
    # Get start/end dates based on numer of days
    numDays_ctk.getDates()
    # Grab the data from yfinance
    getCompanyData_ctk.get_data()
    # Create window to display data in, plot the data, then display the data
    displayData_ctk.plot_window()

if __name__ == "__main__":
    main()
