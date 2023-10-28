# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   plotOneStock_v2.py
-       This script looks up the closing price for a stock 
-       that the user supplies by calling yfinance. The user
-       enters a stock ticker, then supplies the number of days
-       to look stock data for.  The script then uses matplotlib 
-       to plot the data within a tkinter window 
-
-   Required Packages:
-       yfinance
-       csv
-       tkinter
-       customtkinter
-       matplotlib
-       seaborn
-       pandas
-       datetime
-
-   Required Modules:
-       getTicker_ctk.py
-       numDays_ctk.py
-       getCompanyData.py
-       displayData_ctk.py
-
-   Methods:
-       get_ticker()
-       get_numdays()
-       get_dates()
-       get_data()
-       plot_window()
-       main()
-
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Oct 2023
--------------------------------------------------------------
'''
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
