import tkinter as tk
from tkinter import ttk
import sv_ttk
from sprnldata.update.monaupdate import monaupdate
from datetime import datetime

root = tk.Tk()
root.geometry('500x200')
root.title('Retrieving Data')

page = tk.Frame(root)
page.pack(expand=True)

# Enter version number
label = ttk.Label(page, text='Version:')
label.grid(row=0, column=0, padx=10, pady=10)
entry_version = ttk.Entry(page, width=20)
entry_version.insert(0, datetime.strftime(datetime.now(), '%Y%m%d'))
entry_version.grid(row=0, column=1, columnspan=2, pady=10)

# Button
monabutton = ttk.Button(page, text='MONA Update', command=lambda : monaupdate(entry_version))
monabutton.grid(row=1, column=0, columnspan=3, pady=10)

sv_ttk.set_theme("dark")
root.mainloop()