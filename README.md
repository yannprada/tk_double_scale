# DoubleScale

tkinter widget

Methods:
```python
DoubleScale.get_values()			# -> [float, float]
DoubleScale.set_values(a: float, b: float)
```

DoubleScale parameters currently supported:

```python
master: tk.Widget
from_: float      	# value min
to: float         	# value max
length: int       	# widget length and thickness in pixels
thickness: int
cursor_width: int 	# cursor width
offset_x: int		# widget top left corner
offset_y: int
decimals: int		# values precision
bg_color: str		# color options
bg_outline_up: str
bg_outline_down: str
cursor_color: str
cursor_outline_up: str
cursor_outline_down: str
```

## Demo

```python
import tkinter as tk

root = tk.Tk()
root.title('DoubleScale testing')
root.geometry('300x500+1000+200')
DoubleScale(root).pack()
DoubleScale(root, to=10, decimals=1).pack()
DoubleScale(root, to=1, decimals=-2).pack()
DoubleScale(root, from_=-100).pack()
DoubleScale(root, offset_y=40, cursor_color='blue', cursor_outline_up='lightblue', 
			cursor_outline_down='darkblue', bg_color='#0ff').pack()
DoubleScale(root, length=50).pack()
DoubleScale(root, length=200, thickness=30, cursor_width=30).pack()
root.mainloop()
```

![DoubleScale test](https://github.com/yannprada/tk_double_scale/blob/12be68222b6f1f63bd104862c56a196fb3490a64/test.png "DoubleScale test")
