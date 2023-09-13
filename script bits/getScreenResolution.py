# importing tkinter module
from tkinter import * 
from tkinter import messagebox

# creating then hiding a tkinter window
root = Tk()
root.withdraw()

# getting screen's height in pixels
height = root.winfo_screenheight()

# getting screen's width in pixels
width = root.winfo_screenwidth()

# Displaying the data
messagebox.showinfo('Screen Resolution', 'Screen Resolution is:\n%d x %d' %(width, height))

# mainloop()
