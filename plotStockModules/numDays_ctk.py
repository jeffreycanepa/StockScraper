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
-       get_lookup_dates(): Puts up two customtkinter windows containing a 
-           tkcalendar calendar widget.  These are used to allow the user to select 
-           a Start Date and an End Date. These dates are then formatted into date 
-           strings that can be used with yfinance and for my own use in other dialogs.  
-           The dates (with appropriate formatting) are stored in an array named 'dates'
-
-           Requires:
-               global dates array
-
-           Returns:
-               array of formatted dates
-
-       set_winsize(): Set the location/size of the window 
-           Requires:
-              object cwindow- The window object
-
-           Returns:
-               string winGeometry- a string of the window dimensions to use.
-
-       getNumDays(): Using customtkinter put up a dialog that asks user to input a number 
-                     of days to use for stock look up.
-           Requires:
-
-           Returns:
-               int days- the number of days (from today) to lookup stock data for.
-
-       getDates(): Using int days it calculates formatted date strings to use with yfinance
-                   and for my use in dialogs.
-            Requires:
-               int days
-               array dates
-
-            Returns:
-
-
-   Jeff Canepa
-   jeff.canepa@gmail.com
-   Nov 2023
--------------------------------------------------------------
'''
import customtkinter
import tkinter
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime, date, timedelta


# Global variable(s)
global days
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

        # Function to use with bind event for dialog button
        def click_return(event):
            get_day(self)
            root.destroy()
    
        # Get today's date
        today = date.today()
        oneYearAgo = today - timedelta(days=365)
        maxDate = today - timedelta(days=1)
        minDate = today - timedelta(days=7305) #20 years(ish)

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
        bt1.bind('<Return>', click_return)
        bt1.focus()
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

def set_winsize(cwindow):
    winWidth = 200
    winHeight = 140
    x = (cwindow.winfo_screenwidth() / 2) - (winWidth / 2)
    winGeometry = f'{winWidth}x{winHeight}+{int(x)}+{80}'
    return winGeometry

def getNumDays():
    # Function to use with bind event on dialog button
    def click_return(event):
        getValue()

    # Create customtkinter window
    days_window = customtkinter.CTk()
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
    label = customtkinter.CTkLabel(days_window, text='Enter the Number of Days')
    label.pack(padx=10, pady=10)

    # Add field to get ticker.  Make it accessible with tkinter.StringVar()
    myDays = tkinter.StringVar()
    entryField = customtkinter.CTkEntry(days_window,validate='key',
                                        width= 50,
                                        validatecommand=(my_valid,'%S'), 
                                        textvariable=myDays)
    entryField.insert(0, 365)
    entryField.pack()

    # Add button to window.  Add commands to validate data input and to quit window when validation is completed        
    btn = customtkinter.CTkButton(days_window, text="Enter", width=20, height=10, command=getValue)
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
