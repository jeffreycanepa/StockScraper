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
             ['DocuSign','DOCU'],['Splunk','SPLK'],['XLU Utilities','XLU'],['Broadcom','AVGO']] 
tickers = ['AAPL','ADBE','CSCO','NTAP','MSFT','AMZN','TSLA','VMW','DOCU','SPLK','XLU','AVGO']
company_names = ['Apple','Adobe','Cisco','NetApp','Microsoft','Amazon','Tesla',
                 'VMWare', 'DocuSign', 'Splunk', 'XLU Utilities','Broadcom']

cbuts = []
selectedCompanies = []
btvars = []
tl = None
winsize = None

def getwinsize():
    winHeight = 120 + (len(company_names) * 23)
    winGeometry = '200x{}+200+40'
    return winGeometry.format(winHeight)

def getselecteCompanies(company_names):
    winsize = getwinsize()
    window = tk.Tk()
    window.title('Select')
    window.geometry(winsize)
    tline = tk.IntVar()
    cb = tk.IntVar()

    # Method to validate is any checkbuttons are checked. If they are, then enable the enter button.
    def is_checkbox_checked():
        my_flag=False
        # ischecked = False
        for index, item in enumerate(company_names):
            if btvars[index].get() == 1:
                my_flag = True               
        if my_flag == True:
            bt1.config(state='normal')
        else:
            bt1.config(state='disabled')

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

    # Create a LabelFrame
    frame =tk.LabelFrame(window, text="Select Companies", padx=5, pady=5)
    frame.pack(padx=10, pady=10)

    # Create a frame for checkboxes
    frame2 = tk.Frame(window, padx=17)
    frame2.pack()

    # Create Enter button
    bt1 = tk.Button(window, text='Enter', state='disabled', command=lambda:[setSelectedCompanies(), window.destroy()])

    # Array of the checkbutton values
    for x in range(len(company_names)):
        btvars.append(tk.IntVar())

    for index, item in enumerate(company_names):
        cbuts.append(tk.Checkbutton(frame, text=item, anchor='w', width=50, variable=btvars[index], onvalue=1, offvalue=0, command=is_checkbox_checked))
        cbuts[index].pack()
    tk.Checkbutton(frame2, text='Select All', anchor='w', width=50, variable=cb, onvalue=1, offvalue=0, command=lambda:[select_all(),is_checkbox_checked()]).pack()
    # tk.Checkbutton(frame2, text='Display Trendline', anchor='w', width=15, variable=tline, onvalue=1, offvalue=0, command=showline).pack()
    bt1.pack()
    
    window.mainloop()

def setSelectedCompanies():
    for index, item in enumerate(company_names):
        if btvars[index].get() == 1:
            selectedCompanies.append([item,tickers[index]])

def main():
    getselecteCompanies(company_names)
    print(selectedCompanies)
    # print(tl)

if __name__ == "__main__":
    main()
    