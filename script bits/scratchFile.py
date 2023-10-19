# Scratch script for practicing code before adding to larger script
import tkinter
import customtkinter

app = customtkinter.CTk()
app.geometry('400x200')
app.title('Get Stock Ticker')

label = customtkinter.CTkLabel(app, text='Enter Stock Ticker')
label.pack(padx=10, pady=10)

myTicker = tkinter.StringVar()
ticker = customtkinter.CTkEntry(app, width=200, height=10, textvariable=myTicker)
ticker.pack()

def getTicker():
    print(myTicker)

btn = customtkinter.CTkButton(app, text="Enter", command=getTicker)
btn.pack(padx=10,pady=20)

app.mainloop()
