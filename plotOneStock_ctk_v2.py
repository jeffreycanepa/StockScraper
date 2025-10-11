# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   plotOneStock_v2.py
-       This script looks up the closing price for a stock 
-       that the user supplies by calling yfinance. The user
-       enters a stock ticker, then supplies the number of days
-       to parse stock data for.  The script then uses matplotlib 
-       to plot the data within a tkinter window 
-
-   Required Packages (required in Modules):
-       yfinance: 0.2.31
-       customtkinter: 5.2.1
-       matplotlib: 3.8.0
-       pandas: 2.1.1
-       numpy: 1.26.4
-       tkinter: built-in
-       datetime: built-in
-
-   Required Modules:
-       getTicker_ctk.py
-       numDays_ctk.py
-       getCompanyData_ctk.py
-       displayData_ctk.py
-
-   Methods:
-       main()
-
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Oct 2023
--------------------------------------------------------------
'''
import plotStockModules.getCompanyData_ctk as getCompanyData

def main():
    getCompanyData.fetch_and_plot_data()

if __name__ == "__main__":
    main()
