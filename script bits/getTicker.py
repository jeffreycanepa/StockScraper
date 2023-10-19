# Use customtkinter to ask user for a stock ticker.  Still require tkinter for get() and for messagebox
import tkinter
from tkinter import messagebox
import customtkinter

# Global variable
ticker = None

# getTicker(): Using customtkinter put up a dialog that ask user to input a stock ticker to look up.
def getTicker():    
    # Create customtkinter window
    app = customtkinter.CTk()
    app.geometry('200x140')
    app.title('Get Stock Ticker')

    # Add label to window
    label = customtkinter.CTkLabel(app, text='Enter Stock Ticker')
    label.pack(padx=10, pady=10)

    # Add field to get ticker.  Make it accessible with tkinter.StringVar()
    myTicker = tkinter.StringVar()
    entryField = customtkinter.CTkEntry(app, textvariable=myTicker)
    entryField.pack()

    # Validate the data entered into the field.
    def validate():
        # List of Special Characters to not allow
        special_ch = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_',
                   '+', '=', '{', '}', '[', ']', '|', '\\', '/', ':', ';', '"', "'",
                    '<', '>', ',', '?']
        global ticker
        ticker = entryField.get()
        msg = ''

        if len(ticker) == 0:
            msg = 'Field \'Ticker\' can\'t be empty'
        else:
            try:
                if any(ch in special_ch for ch in ticker):
                    msg = 'Ticker cannot have special characters'
                elif any(ch.isdigit() for ch in ticker):
                    msg = 'Ticker can\'t have numbers'
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
    btn = customtkinter.CTkButton(app, text="Enter", width=50, command=lambda:[validate()])
    btn.pack(padx=10,pady=20)

    app.mainloop()

def main():
    getTicker()
    print(ticker)

if __name__ == "__main__":
    main()
