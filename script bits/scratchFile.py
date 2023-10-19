# Scratch script for practicing code before adding to larger script
import tkinter
import customtkinter

def getTicker():
    theTicker = ticker.get()
    print(theTicker)

app = customtkinter.CTk()
app.geometry('200x140')
app.title('Get Stock Ticker')

label = customtkinter.CTkLabel(app, text='Enter Stock Ticker')
label.pack(padx=10, pady=10)

myTicker = tkinter.StringVar()
ticker = customtkinter.CTkEntry(app, textvariable=myTicker)
ticker.pack()



btn = customtkinter.CTkButton(app, text="Enter", width=50, command=lambda:[getTicker(), app.quit()])
btn.pack(padx=10,pady=20)

app.mainloop()
