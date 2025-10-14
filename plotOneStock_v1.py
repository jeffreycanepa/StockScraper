# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   plotOneStock.py
-       This script looks up the closing price for a stock 
-       that the user supplies by calling yfinance. The user
-       enters a stock ticker, then supplies the number of days
-       to look stock data for.  The script then uses matplotlib 
-       to plot the data within a tkinter window. 
-
-   Required Packages (required in imported Modules):
-       yfinance: 0.2.31
-       matplotlib: 3.8.0
-       pandas: 2.1.1
-       numpy: 1.26.4
-       tkinter: built-in
-       datetime: built-in
-
-   Required Modules:
-       getCompanyData.py
-
-   Methods:
-       main()
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Sep 2023
--------------------------------------------------------------
'''
import plotStockModules.getCompanyData as getCompanyData

# main()
def main():
    # Get Stock Data and plot it
    getCompanyData.fetch_and_plot_data()

if __name__ == "__main__":
    main()
