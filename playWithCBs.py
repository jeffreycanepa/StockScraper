import tkinter as tk

def create_cbuts():
    for index, item in enumerate(cbuts_text):
        cbuts.append(tk.Checkbutton(frame, text = item))
        cbuts[index].pack()

def select_all():
    for i in cbuts:
        i.select()

def deselect_all():
    for i in cbuts:
        i.deselect()

root = tk.Tk()
root.geometry('200x300')
# Create a LabelFrame
frame =tk.LabelFrame(root, text="Select Checkboxes", labelanchor='nw' ,padx=20, pady=20)
frame.pack(pady=20, padx=10)

cbuts_text = ['a','b','c','d']
cbuts = []
create_cbuts()
tk.Checkbutton(root, text = 'all', command = select_all).pack()
tk.Button(root, text = 'none', command = deselect_all).pack()
tk.mainloop()