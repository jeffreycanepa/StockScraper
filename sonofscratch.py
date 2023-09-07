import tkinter as tk
from tkinter.simpledialog import askinteger

def main():
    root = tk.Tk()
    root.withdraw()
    prompt = askinteger("Input", "Input an Integer")
    root.destroy()
    root.mainloop()

    print(prompt)

if __name__ == "__main__":
    main()