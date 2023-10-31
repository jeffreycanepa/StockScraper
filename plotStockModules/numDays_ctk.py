import customtkinter
import tkinter
from tkinter import messagebox
from datetime import datetime, timedelta


# Global variable(s)
global days
global dates

# get_winsize()- Set the location/size of the window 
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

# getNumdays(): Using customtkinter put up a dialog that ask user to input a number of days to use for stock look up.
def getNumDays():
    # Function to use with bind event on dialog button
    def click_return(event):
        getValue()

    # Create customtkinter window
    days_window = customtkinter.CTk()
    days_window.geometry(set_winsize(days_window))
    days_window.title('Get Number of Days')

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
    label = customtkinter.CTkLabel(days_window, text='Enter the Number of Days')
    label.pack(padx=10, pady=10)

    # Add field to get ticker.  Make it accessible with tkinter.StringVar()
    myDays = tkinter.StringVar()
    entryField = customtkinter.CTkEntry(days_window,validate='key',validatecommand=(my_valid,'%S'), textvariable=myDays)
    entryField.insert(0, 365)
    entryField.pack()

    # Add button to window.  Add commands to validate data input and to quit window when validation is completed        
    btn = customtkinter.CTkButton(days_window, text="Enter", width=20, height=10, command=lambda:[getValue()])
    btn.bind('<Return>', click_return)   
    btn.focus()
    btn.pack(padx=10,pady=20)

    days_window.mainloop()

def getDates():
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
