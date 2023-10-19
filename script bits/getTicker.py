# Use customtkinter to ask user for a stock ticker
import tkinter
import customtkinter

ticker = None
def getTicker():
    def returnTicker():
        global ticker
        ticker = entryField.get()
        return ticker

    app = customtkinter.CTk()
    app.geometry('200x140')
    app.title('Get Stock Ticker')

    label = customtkinter.CTkLabel(app, text='Enter Stock Ticker')
    label.pack(padx=10, pady=10)

    myTicker = tkinter.StringVar()
    entryField = customtkinter.CTkEntry(app, textvariable=myTicker)
    entryField.pack()



    btn = customtkinter.CTkButton(app, text="Enter", width=50, command=lambda:[returnTicker(), app.quit()])
    btn.pack(padx=10,pady=20)

    app.mainloop()

def main():
    global ticker
    getTicker()
    print(ticker)

if __name__ == "__main__":
    main()