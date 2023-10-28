# A second scratch script for testing ideas before integrating into larger scripts
import tkinter as tk
from tkinter import ttk

def click_return(event):
    window.destroy()

def lft_mouse_click(event):
    stk = answer.get()
    if stk == '':
       labelString.set('You must enter a stock ticker!')
    else:
        window.destroy()

window = tk.Tk()
window.geometry('800x600+700+200')
window.title('Jeff\'s Window')

answer= tk.StringVar()
labelString = tk.StringVar(value= 'Enter Stock Ticker')
label = ttk.Label(window,  textvariable=labelString).pack(pady = 10)
entry = ttk.Entry(window, textvariable= answer).pack()


bt1 = ttk.Button(window, text= 'Click Me')
bt1.bind('<Return>', click_return)
bt1.bind('<Button-1>', lft_mouse_click)

bt1.focus()
bt1.pack(pady = 10)

window.mainloop()

print(answer.get())