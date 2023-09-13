# A second scratch script for testing ideas before integrating into larger scripts
# Vaidate checkbox and textentry before enabling Enter key
import tkinter as tk
my_w = tk.Tk()
my_w.geometry('400x200')  # Size of the window 
my_w.title("www.plus2net.com")  #  title

def my_check(*args):
    my_flag=False
    if(len(e1.get()) <3 ):my_flag=True # Minimum 3 char for entry
    if(c1_v1.get() != 'Yes'):my_flag=True # Check box is not checked   
    if my_flag != True:b1.config(state='normal',bg='lightgreen')    
    else:b1.config(state='disabled',bg='lightyellow')
l1=tk.Label(my_w,text='Name',font=20)
l1.grid(row=0,column=0,padx=10,pady=10)
str1=tk.StringVar()
e1=tk.Entry(my_w,bg='grey',font=20,textvariable=str1)
e1.grid(row=0,column=1)
str1.trace('w',my_check)
c1_v1=tk.StringVar(my_w)
c1_v1.set('')
c1=tk.Checkbutton(my_w,text='I agree',variable=c1_v1,
                  onvalue='Yes',offvalue='',command=my_check,font=24)
c1.grid(row=1,column=1,sticky='w')
b1=tk.Button(my_w,text='Submit',bg='lightyellow', font=20,state='disabled', command=my_w.destroy)
b1.grid(row=2,column=1,padx=10,pady=5)
my_w.mainloop()  # Keep the window open