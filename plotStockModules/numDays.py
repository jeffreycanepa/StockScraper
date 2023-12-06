# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   numDays.py
-       This module has a method that asks the user to provide
-       the number of days the use wishes to look up stock date for. 
-       It then uses that number of days to calculate a start/end date.
-       Dates are calculated to the correct format to work with yfinance
-       and matplotlib.  Dates are saved to an array
-       
-
-   Required Packages (required in imported Modules):
-       tkinter: built-in
-       datetime: built-in
-
-   Required Modules:
-
-   Methods:
-       set_winsize()
-       get_num_days()
-       get_dates()
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Dec 2023
--------------------------------------------------------------
'''

from tkinter import *
from tkinter.simpledialog import askinteger, askstring
from tkinter import messagebox
from datetime import datetime, timedelta

# Global variable(s)
global days
global dates

def set_winsize(cwindow):
    winWidth = 200
    winHeight = 140
    x = (cwindow.winfo_screenwidth() / 2) - (winWidth / 2)
    winGeometry = f'{winWidth}x{winHeight}+{int(x)}+{80}'
    return winGeometry

def get_num_days():
    # Function to use with bind event on dialog button
    def click_return(event):
        getValue()

    # Create customtkinter window
    days_window = Tk()
    days_window.geometry(set_winsize(days_window))
    days_window.title('Number of Days')

    # Get the value entered
    def getValue():
        global days
        days = entryField.get()
        sdays = int(days)
        msg = ''

        if len(days) == 0:
            msg = 'Input field \'Days\' can\'t be empty'
        else:
            if sdays > 3652:
                msg = 'Too many days!\rLimit of 10 years (3652 days)'
            else:
                msg = 'Success'

        if msg != 'Success':
            messagebox.showinfo('message', msg)
        else:
            days = sdays
            days_window.destroy()

    # Validate the data entered into the field.
    def validate(u_input):
        return u_input.isdigit()
    my_valid = days_window.register(validate)

    # Add label to window
    label = Label(days_window, text='Enter the Number of Days')
    label.pack(padx=10, pady=10)

    # Add field to get ticker.  Make it accessible with tkinter.StringVar()
    myDays = StringVar()
    entryField = Entry(days_window,validate='key',
                                        width= 6,
                                        validatecommand=(my_valid,'%S'), 
                                        textvariable=myDays)
    entryField.insert(0, 365)
    entryField.pack()

    # Add button to window.  Add commands to validate data input and to quit window when validation is completed        
    btn = Button(days_window, text="Enter", command=getValue)
    btn.bind('<Return>', click_return)   
    btn.focus()
    btn.pack(padx=10,pady=20)

    days_window.mainloop()

# get_dates()- Get start/end dates for stock lookup.
# Requires: 
#   numdays- Number of days to lookup stock data for
# Returns:
#   a list containing start/end dates for yfinance lookup and for matplotlib labels
#
def get_dates():
    global days
    global dates
    now = datetime.now()
    then = now - timedelta(days)
    # yfinance dates must be in the format ("%Y-%m-%d") That is, year-month-day
    yfinance_start_date = (now - timedelta(days=days)).strftime('%Y-%m-%d')
    yfinance_end_date = (now + timedelta(days=1)).strftime('%Y-%m-%d')
    # date strings I use in the UI are in format ("%b %d, %Y")
    start_date = (now - timedelta(days=days)).strftime('%b %d, %Y')
    end_date = now.strftime('%b %d, %Y')
    dates = [now, then, yfinance_start_date, yfinance_end_date, start_date, end_date] 