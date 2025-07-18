# DoubleScale

```
import tkinter as tk

root = tk.Tk()
root.title('DoubleScale testing')
root.geometry('300x300+1000+200')
DoubleScale(root).pack()
DoubleScale(root, to=10, decimals=1).pack()
DoubleScale(root, to=1, decimals=-2).pack()
DoubleScale(root, from_=-100).pack()
DoubleScale(root, offset_y=40, cursor_color='blue', cursor_outline_up='lightblue', 
			cursor_outline_down='darkblue', bg_color='#0ff').pack()
root.mainloop()
```

![DoubleScale test](/repository/blob/main/test.png?raw=true "DoubleScale test")