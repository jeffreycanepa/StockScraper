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
-       yfinance: 0.2.31
-       tkinter: 
-       customtkinter: 5.2.1
-       matplotlib: 3.8.0
-       seaborn: 0.13.0
-       pandas: 2.1.1
-       datetime:
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
    getCompanyData.fetch_and_plot_data()

if __name__ == "__main__":
    main()
