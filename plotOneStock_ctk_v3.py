# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   plotOneStock_v3.py
-       This script looks up the closing price for a stock 
-       that the user supplies by calling yfinance. The user
-       enters a stock ticker, then is asked to choose a start
-       date and an end date.  The script then uses matplotlib 
-       to plot the data within a customtkinter window 
-
-   Required Packages (Required by imported Modules):
-       yfinance: 0.2.31
-       matplotlib: 3.8.0
-       seaborn: 0.13.0
-       pandas: 2.1.1
-       customtkinter: 5.2.1
-       tkinter: built-in
-       datetime: built-in
-       tkcalendar: 1.6.1
-
-   Required Modules:
-       getTicker_ctk.py
-       numDays_ctk.py
-       getCompanyData.py
-       displayData_ctk.py
-
-   Methods:
-       main()
-
-   New in Version 3:
-       Replaced numDays.getNumDays() and numDays.getDates() with numDays.get_lookup_dates()
-       This new method uses tkcalendar to allow the user pick a start/end date using the
-       tkcalendar widget within a customtkinter window.
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Nov 2023
--------------------------------------------------------------
'''
import plotStockModules.getCompanyData_ctk as getCompanyData

def main():
    getCompanyData.get_data_using_calendar()

if __name__ == "__main__":
    main()
