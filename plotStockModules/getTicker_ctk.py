# Use customtkinter to ask user for a stock ticker.  Still require tkinter for get() and for messagebox
import tkinter
from tkinter import messagebox
import customtkinter

# Global variable
ticker = None
numdays = None

# getTicker(): Using customtkinter put up a dialog that ask user to input a stock ticker to look up.
def getTicker():
    # Function to use with bind event for dialog button
    def click_return(event):
        global ticker
        ticker = myTicker.get()
        app.destroy()

    # Create customtkinter window
    app = customtkinter.CTk()
    app.geometry('200x140+200+40')
    app.title('Get Stock Ticker')

    # Add label to window
    labelStr = tkinter.StringVar(value= 'Enter Stock Ticker')
    label = customtkinter.CTkLabel(app, textvariable= labelStr)
    label.pack(padx=10, pady=10)

    # Add field to get ticker.  Make it accessible with tkinter.StringVar()
    myTicker = tkinter.StringVar()
    entryField = customtkinter.CTkEntry(app, textvariable=myTicker)
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
            app.destroy()

    # Add button to window.  Add commands to validate data input and to quit window when validation is completed        
    btn = customtkinter.CTkButton(app, text="Enter", width=20, height=10, command=lambda:[validate()])
    btn.bind('<Return>', click_return)
    btn.focus()
    btn.pack(padx=10,pady=20)

    app.mainloop()

