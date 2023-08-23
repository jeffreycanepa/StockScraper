# /opt/homebrew/bin/python3
'''
getStocks: This is my first attempt at a useful Python script.  This
script uses yFinance to lookup some of the stocks that I own and will
get the closing price.  It will then save the data to an Excel spreadsheet.

    To Do: 
    1) Check to see if stocks for today were already fetched/saved
    2) Read in stocks from external file 
    3) Add UI to add/remove stocks
'''

import yfinance as yf
from tkinter import messagebox
from datetime import datetime, timezone
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.styles import Font
from openpyxl.styles import Alignment

# My Stocks
myStocks = ['AAPL', 'ADBE', 'CSCO', 'NTAP', 'MSFT', 'AMZN', 'TSLA', 'VMW', 'DOCU', 'SPLK', 'XLU']

# Get current datetime
now = datetime.now()
utcnow = datetime.now(timezone.utc)

# File to work with
myFile = 'myStocks.xlsx'

# Calculate the difference between today's price and yesterday's price
def getChange(curPrice, oldPrice):
    change = float(curPrice - oldPrice)
    return change

# Calulate the pecent change from today's price and yesterday's price
def getPercentChange(curPrice, oldPrice):
    pchange = float(((curPrice - oldPrice) / oldPrice) * 100)
    return pchange

# Get the index of the first empty row for each sheet in workbook for the Excel file
def getLastRow(sheet):
    last_row = sheet.max_row
    last_col = sheet.max_column
    
    for i in range(last_row):
        for j in range(last_col):
            if sheet.cell(last_row, last_col).value is None:
                last_row -= 1
                last_col -= 1 
    return last_row+1


# Using myStocks, get stock data on each stock and write it out to file
def checkStocks(wb_obj, datestr):
    for stocks in myStocks:
        ticker = yf.Ticker(stocks).info
        curr_symbol = ticker['symbol']
        # For reasons unknown to me, XLU does not have currentPrice as part of Yahoo Finance ticker info.
        # Use navPrice instead
        if curr_symbol == 'XLU':
            current_price = ticker['navPrice']
        else:
            current_price = ticker['currentPrice']
        previous_close_price = ticker['regularMarketPreviousClose']
        change = getChange(current_price, previous_close_price)
        pctChange = getPercentChange(current_price, previous_close_price)
        sheet = wb_obj[curr_symbol]
        lastRow = getLastRow(sheet)
        sheet['A' + str(lastRow)] = datestr
        sheet['B' + str(lastRow)] = curr_symbol
        sheet['C' + str(lastRow)] = current_price
        sheet['D' + str(lastRow)] = previous_close_price
        sheet['E' + str(lastRow)] = change
        sheet['F' + str(lastRow)] = pctChange

        # Write out the data
        # writer.writerow(['', curr_symbol, current_price, previous_close_price, format(change, '.2f') , format(pctChange, '.2f')])

def createSheets(wb_obj):
    # Create the sheets
    for stocks in myStocks:
        if stocks == 'AAPL':
            sheet = wb_obj.active
            sheet.title = stocks
        else:
            sheet = wb_obj.create_sheet(title=stocks)

def createColumnNames(wb_obj):
    # Create the column names in each sheet and set their width
    sheetNames = wb_obj.sheetnames
    for name in sheetNames:
        sheet = wb_obj[name]
        sheet['A1'] = 'Date'
        sheet.column_dimensions['A'].width = 10
        sheet['B1'] = 'Ticker'
        sheet.column_dimensions['B'].width = 10
        sheet['C1'] = 'Closing Price'
        sheet.column_dimensions['C'].width = 12
        sheet['D1'] = 'Previous Close'
        sheet.column_dimensions['D'].width = 14
        sheet['E1'] = 'Change'
        sheet.column_dimensions['E'].width = 12
        sheet['F1'] = '% Change'
        sheet.column_dimensions['F'].width = 12

def formatHeader(wb_obj):
    # Format the top row on each sheet
    lightGrey = 'CCCCCCCC'
    sheetNames = wb_obj.sheetnames
    for name in sheetNames:
        sheet = wb_obj[name]
        for columns in sheet.iter_cols(min_col=1, max_col=6):
            for cell in columns:
                cell.fill = PatternFill(start_color=lightGrey, end_color=lightGrey,
                                        fill_type = "solid")
                cell.font = Font(bold = True)
                cell.alignment = Alignment(horizontal = 'center')

def main():
    # Only check after markets have closed (assumes Pacific Time Zone)
    if utcnow.hour < 20:
        messagebox.showwarning('Markets still open', 'Markets are still open.\nPlease wait until they are closed')
    else:
        # Get current date string formatted my way in user's timezone
        datestr = now.strftime('%Y-%m-%d')

        # Create/open xsl file for storing data
        try:
            # Open workbook
            wb_obj = openpyxl.load_workbook(myFile)
            checkStocks(wb_obj, datestr)
        
        except FileNotFoundError as e:
            wb_obj = Workbook()
            createSheets(wb_obj)
            createColumnNames(wb_obj)
            formatHeader(wb_obj)
            checkStocks(wb_obj, datestr)
            # wb_obj.save('jeffsStocks.xlsx')
 
        except UnboundLocalError as e:
            print(e)
    
        # Save the file
        wb_obj.save(myFile)


if __name__ == "__main__":
    main()
