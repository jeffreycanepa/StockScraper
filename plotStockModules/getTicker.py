# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   getTicker.py
-       This module has a method that asks the user for a 
-       stock ticker. It also has a method that calculates 
-       where on the screen to display the dialog (to my preferences)
-       
-
-   Required Packages:
-       tkinter: built-in
-
-   Required Modules:
-
-   Methods:
-       set_winsize()
-       get_ticker()
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Dec 2023
--------------------------------------------------------------
'''
from tkinter import *
from tkinter import messagebox

# Global variable
ticker = None
numdays = None

# set_winsize()- Set the location/size of the window 
#
# Requires:
#   cwindow- The window object
#
# Returns:
#   string of the window dimensions to use.
#
def set_winsize(cwindow):
    winWidth = 200
    winHeight = 140
    x = (cwindow.winfo_screenwidth() / 2) - (winWidth / 2)
    winGeometry = f'{winWidth}x{winHeight}+{int(x)}+{80}'
    return winGeometry

# getTicker(): Using customtkinter put up a dialog that ask user to input a stock ticker to look up.
def getTicker():
    # Function to use with bind event for dialog button
    def click_return(event):
        validate()

    # Create kinter window
    ticker_window = Tk()
    ticker_window.geometry(set_winsize(ticker_window))
    ticker_window.title('Get Stock Ticker')

    # Add label to window
    labelStr = StringVar(value= 'Enter Stock Ticker')
    label = Label(ticker_window, textvariable= labelStr)
    label.pack(padx=10, pady=10)

    # Add field to get ticker.  Make it accessible with tkinter.StringVar()
    myTicker = StringVar()
    entryField = Entry(ticker_window, width = 6, textvariable=myTicker)
    entryField.pack()

    # Validate the data entered into the field.
    def validate():
        global ticker
        ticker = entryField.get()
        ticker = ticker.upper()
        
        # List of Special Characters to not allow
        special_ch = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_',
                   '+', '=', '{', '}', '[', ']', '|', '\\', '/', ':', ';', '"', "'",
                    '<', '>', ',', '?']
        msg = ''

        if len(ticker) == 0:
            msg = 'Entry field \'Stock Ticker\' can\'t be empty'
        else:
            try:
                if any(ch in special_ch for ch in ticker):
                    msg = 'Stock Ticker cannot contain special characters'
                elif any(ch.isdigit() for ch in ticker):
                    msg = 'Stock Ticker can\'t contain numbers'
                elif len(ticker) > 5:
                    msg = 'Ticker is too long.'
                else:
                    msg = 'Success'
            except Exception as ep:
                messagebox.showerror('error', ep)
        
        if msg != 'Success':
            messagebox.showinfo('message', msg)
        else:
            ticker_window.destroy()

    # Add button to window.  Add commands to validate data input and to quit window when validation is completed        
    btn = Button(ticker_window, text="Enter", command=validate)
    btn.bind('<Return>', click_return)
    btn.focus()
    btn.pack(padx=10,pady=20)

    ticker_window.mainloop()