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

def getselecteCompanies(company_names):
    window = tk.Tk()
    window.title('My Window')
    window.geometry('200x440')
 
    # Create a LabelFrame
    frame =tk.LabelFrame(window, text="Select the Companies", padx=20, pady=20)
    frame.pack(pady=20, padx=10)

    # Add method to select all checkboxes
    def select_all():
        for i in cbuts:
            i.select()

    # array of the button values
    for x in range(11):
        btvars.append(tk.IntVar())

    for index, item in enumerate(company_names):
        cbuts.append(tk.Checkbutton(frame, text=item, anchor='w', width=50, variable=btvars[index], onvalue=1, offvalue=0))
        cbuts[index].pack()
    tk.Checkbutton(window, text='Select All', width=10, height=2, command=select_all).pack()
    tk.Button(window, text='Enter', command=lambda:[setSelectedCompanies(), window.destroy()]).pack()
                
    window.mainloop()

def setSelectedCompanies():
    for index, item in enumerate(company_names):
        if btvars[index].get() == 1:
            selectedCompanies.append([item,tickers[index]])

def main():
    getselecteCompanies(company_names)
    print(selectedCompanies)

if __name__ == "__main__":
    main()