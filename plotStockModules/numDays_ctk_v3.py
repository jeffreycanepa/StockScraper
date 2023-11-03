# /opt/homebrew/bin/python3
'''
--------------------------------------------------------------
-   numDays_ctk.py
-       This Module is for use with my stock lookup scripts. This Module contains 
-           the Class calendar_Window and method get_lookup_dates()
-
-       Class calendar_Window: Class that uses customtkinter and tkcalendar to create
-           window objects that contain all of the necessary strings, labels, buttons
-           and window properties for getting/accessing date strings.
-       
-       Method get_lookup_dates(): Puts up two customtkinter windows containing a 
-           tkcalendar calendar widget.  These are used to allow the user to select 
-           a Start Date and an End Date. These dates are then formatted into date 
-           strings that can be used with yfinance and for my own use in other dialogs.  
-           The dates (with appropriate formatting) are stored in an array named 'dates'
-
-   Required Packages:
-       tkinter: 
-       customtkinter: 5.2.1
-       tkcalendar: 1.6.1
-       datetime:
-
-   Classes:
-       calendar_Window
-
-   Methods:
-       get_lookup_dates()
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Nov 2023
--------------------------------------------------------------
'''

import customtkinter
from tkinter import *
from tkcalendar import Calendar
from datetime import datetime, date, timedelta


# Global variable(s)
global dates

class calendar_Window:
    # Initialize with strings for Button and Window Title
    def __init__(self, btnStr, winTitle):
        self.title = btnStr
        self.winTitle = winTitle
        self.myDate = None
    
    # accessor for date string
    def __str__(self):
        return self.myDate
    
    # Configure window so it shows up in a location that works well for me
    def set_winsize(self, root):
        winWidth = 300
        winHeight = 300
        x = (root.winfo_screenwidth() / 2) - (winWidth / 2)
        winGeometry = f'{winWidth}x{winHeight}+{int(x)}+{80}'
        return winGeometry
    
    # Display the window
    def show_Window(self):
        # Create Window
        root = customtkinter.CTk()
    
        # Set geometry and Title
        root.geometry(self.set_winsize(root))
        root.title(self.title)
    
        # Get today's date
        today = date.today()
        oneYearAgo = today - timedelta(days=365)
        maxDate = today - timedelta(days=1)
        minDate = today - timedelta(days=3652) #10 years(ish)

        # Add Instruction String
        lbl1 = customtkinter.CTkLabel(root, text=self.winTitle).pack(pady=5)

        # Add Calendar with appropriate max/min date
        if self.title == 'Start Date':
            cal = Calendar(root, font = 'Arial 14', selectmode = 'day',
                        year = oneYearAgo.year, 
                        month = today.month,
                        day = oneYearAgo.day,
                        showweeknumbers = False,
                        maxdate = maxDate,
                        mindate = minDate,
                        disabledforeground ='red')
        else:
            cal = Calendar(root, font = 'Arial 14', selectmode = 'day',
                        year = today.year, 
                        month = today.month,
                        day = today.day,
                        showweeknumbers = False,
                        maxdate = today,
                        mindate = minDate,
                        disabledforeground = 'red')
        cal.pack(pady = 10)

        # method called by button to get the selected date
        def get_day(self):
            self.myDate = cal.get_date()

        # Add Button
        bt1 = customtkinter.CTkButton(root, text = ('Set ' + self.title), 
            command = lambda:[get_day(self), root.destroy()])
        bt1.pack(pady=5)

        root.mainloop()

def get_lookup_dates():
    global dates
    sDate = calendar_Window('Start Date', 'Pick a Start Date')
    sDate.show_Window()
    eDate = calendar_Window('End Date', 'Pick an End Date')
    eDate.show_Window()

    format_date = '%m/%d/%y'

    now = datetime.strptime(eDate.__str__(), format_date)
    then = datetime.strptime(sDate.__str__(), format_date)
    yfinance_start_date = then.strftime('%Y-%m-%d')
    yfinance_end_date = now.strftime('%Y-%m-%d')
    start_date = then.strftime('%b %d, %Y')
    end_date = now.strftime('%b %d, %Y')
    dates = [now, then, yfinance_start_date, yfinance_end_date, start_date, end_date] 