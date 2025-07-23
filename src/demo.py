import tkinter as tk

from tk_double_scale import DoubleScale

root = tk.Tk()
root.title('DoubleScale testing')
root.geometry('300x500+1000+200')
root.configure(bg='grey')

DoubleScale(root, font='Calibri 20').pack(pady=5)
DoubleScale(root, to=10, decimals=1).pack(pady=5)
DoubleScale(root, to=1, decimals=-2).pack(pady=5)
DoubleScale(root, from_=-100).pack(pady=5)
DoubleScale(root, cursor_color='blue', bg_color='#0ff', text_color='blue'
    ).pack(pady=5)
DoubleScale(root, length=50, font='Calibri 5', cursor_width=5).pack(pady=5)
DoubleScale(root, length=200, thickness=30, cursor_width=30).pack(pady=5)

root.mainloop()