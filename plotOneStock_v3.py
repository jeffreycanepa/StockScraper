# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   plotOneStock_v2.py
-       This script looks up the closing price for a stock 
-       that the user supplies by calling yfinance. The user
-       enters a stock ticker, then is asked to choose a start
-       date and an end date.  The script then uses matplotlib 
-       to plot the data within a customtkinter window 
-
-   Required Packages:
-       yfinance: 0.2.31
-       tkinter: 
-       customtkinter: 5.2.1
-       matplotlib: 3.8.0
-       seaborn: 0.13.0
-       pandas: 2.1.1
-       datetime:
-       tkcalendar: 1.6.1
-
-   Required Modules:
-       getTicker_ctk.py
-       numDays_ctk.py
-       getCompanyData.py
-       displayData_ctk.py
-
-   Methods:
-       get_ticker()
-       get_lookup_dates()
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
import plotStockModules.numDays_ctk_v3 as numDays
import plotStockModules.getCompanyData_v3 as getCompanyData
import plotStockModules.displayData_ctk_v3 as displayData

dates = None
numdays = None
company_name = None
stockData = None


def main():
    global numdays
    global dates
    # Get the Ticker symbol
    getTicker.getTicker()

    # Get a start date and an end date for the stock lookup
    numDays.get_lookup_dates()

    # Grab the data from yfinance
    getCompanyData.get_data()
    
    # Create window to display data in, plot the data, then display the data
    displayData.plot_window()

if __name__ == "__main__":
    main()
