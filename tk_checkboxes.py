# tk_checkboxes.py
# This is a script I used to learn about working with checkboxes 
# in a tkinter window. Put up a window with checkboxes and get 
# a string based on the checkbox's state
#
# Jeff Canepa
# 02-09-23

#!/usr/bin/env python
import tkinter as tk

companies = [['Apple','AAPL'],['Adobe','ADBE'],['Cisco','CSCO'],['NetApp','NTAP'],
             ['Microsoft','MSFT'],['Amazon','AMZN'],['Tesla','TSLA'],['VMWare','VMW'],
             ['DocuSign','DOCU'],['Splunk','SPLK'],['XLU Utilities','XLU']] 
tickers = ['AAPL','ADBE','CSCO','NTAP','MSFT','AMZN','TSLA','VMW','DOCU','SPLK','XLU']
company_names = ['Apple','Adobe','Cisco','NetApp','Microsoft','Amazon','Tesla',
                 'VMWare', 'DocuSign', 'Splunk', 'XLU Utilities']
cbuts = []
selectedCompanies = []
btvars = []
tl = None

def getselecteCompanies(company_names):
    window = tk.Tk()
    window.title('My Window')
    window.geometry('200x460')
    tline = tk.IntVar()
    cb = tk.IntVar()

    # Create a LabelFrame
    frame =tk.LabelFrame(window, text="Select the Companies", padx=20, pady=20)
    frame.pack(padx=10) #pady=20, padx=10

    # Create a frame for checkboxes
    frame2 = tk.Frame(window)
    frame2.pack()

    # Add method to select all checkboxes
    def select_all():
        if cb.get() == 1:
            for i in cbuts:
                i.select()
        else:
            for i in cbuts:
                i.deselect()
    
    def showline():
        global tl
        if tline.get() == 1:
            tl = 1

    # array of the button values
    for x in range(11):
        btvars.append(tk.IntVar())

    for index, item in enumerate(company_names):
        cbuts.append(tk.Checkbutton(frame, text=item, anchor='w', width=50, variable=btvars[index], onvalue=1, offvalue=0, command=tline))
        cbuts[index].pack()
    tk.Checkbutton(frame2, text='Select All', anchor='w', width=15, variable=cb, onvalue=1, offvalue=0, command=select_all).pack()
    tk.Checkbutton(frame2, text='Display Trendline', anchor='w', width=15, variable=tline, onvalue=1, offvalue=0, command=showline).pack()
    tk.Button(window, text='Enter', command=lambda:[setSelectedCompanies(), window.destroy()]).pack()
                
    window.mainloop()

def setSelectedCompanies():
    for index, item in enumerate(company_names):
        if btvars[index].get() == 1:
            selectedCompanies.append([item,tickers[index]])

def main():
    getselecteCompanies(company_names)
    # print(selectedCompanies)
    print(tl)

if __name__ == "__main__":
    main()
    