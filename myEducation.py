'''Script for testing out code before incorporating it into getStocksNew.py'''

from datetime import datetime, timezone
from time import gmtime
import time
from tkinter import messagebox
import openpyxl

def last_active_row():
    workbook = openpyxl.load_workbook('myStocks.xlsx')
    wp = workbook['AAPL']
    last_row = wp.max_row
    last_col = wp.max_column
    
    for i in range(last_row):
        for j in range(last_col):
            if wp.cell(last_row, last_col).value is None:
                last_row -= 1
                last_col -= 1 
            else:
                print(wp.cell(last_row,last_col).value) 
    print("The Last active row is: ", (last_row+1)) # +1 for index 0

def getLastStockEntry():
    workbook = openpyxl.load_workbook('myStocks.xlsx')
    wp = workbook.active
    last_row = wp.max_row
    todayDate = datetime.now().strftime('%Y-%m-%d')
    prevDate = wp.cell(last_row, 1).value
    if todayDate == prevDate:
        messagebox.showerror('Dates Match', 'This script was already run today.\nNo action will be taken.')
    else:
        messagebox.showinfo('Good to Go', 'Script is good to go')

def isMarketOpen():
    # Get current date
    now = datetime.now()
    utcnow = datetime.now(timezone.utc)
    print(utcnow.time())
    # print(utcnow.weekday())
    if (((utcnow.hour > 13) and (utcnow.minute > 30)) and (utcnow.hour < 20)):
        messagebox.showwarning('Warning', 'Markets are still open')
        return False
    else:
        return True
    

def main():
    # last_active_row()
    # print('In Main()')
    marketClosed = isMarketOpen()
    if marketClosed == True:
        getLastStockEntry()

if __name__ == '__main__':
    main()