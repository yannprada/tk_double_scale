import tkinter as tk


class DoubleScale(tk.Canvas):
    def __init__(self, master, from_=0, to=100, length=100, thickness=15, 
                 cursor_width=10, offset=(5, 15), precision=0):
        ox, oy = offset
        w = length + (ox * 2) + cursor_width
        h = thickness + (oy * 2)
        super().__init__(master, width=w, height=h)
        
        # Initialize parameters
        self.min_value = from_
        self.max_value = to
        self.length = length
        self.thickness = thickness
        self.cursor_width = cursor_width
        self.inside_offset = cursor_width / 2 + 1
        self.offset = offset
        self.coeff = length / (self.max_value - self.min_value)
        self.precision = precision
        self.value_a = self.min_value
        self.value_b = self.max_value
        
        self.draw_background()
        self.redraw()
        
        # Bind mouse events
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
    
    def value_to_position(self, value):
        """Convert a value to its corresponding position on the scale."""
        return (value - self.min_value) * self.coeff + self.offset[0] + self.inside_offset
    
    def position_to_value(self, position):
        """Convert a position on the scale back to a value."""
        return (position - self.offset[0] - self.inside_offset) / self.coeff + self.min_value
    
    def on_click(self, event):
        """Determine which value is being dragged."""
        pos = event.x
        if abs(pos - self.value_to_position(self.value_a)) < 10:
            self.dragging_value = 'value_a'
        elif abs(pos - self.value_to_position(self.value_b)) < 10:
            self.dragging_value = 'value_b'
        else:
            self.dragging_value = None
    
    def on_drag(self, event):
        """Update the value based on the drag position."""
        if self.dragging_value:
            new_value = round(self.position_to_value(event.x), self.precision)
            if self.precision == 0:
                new_value = int(new_value)
            if self.dragging_value == 'value_a':
                self.value_a = max(self.min_value, min(new_value, self.value_b))
            elif self.dragging_value == 'value_b':
                self.value_b = min(self.max_value, max(new_value, self.value_a))
            self.redraw()
    
    def draw_background(self):
        """Draw the background of the scale."""
        ox, oy = self.offset
        bx, by = ox + self.length + self.cursor_width + 2, oy + self.thickness
        self.draw_outset_box(ox, oy, bx, by)
    
    def redraw(self):
        """Redraw the scale and the cursor positions."""
        self.delete('cursor')
        self.draw_cursor(self.value_to_position(self.value_a), self.value_a)
        self.draw_cursor(self.value_to_position(self.value_b), self.value_b, True)
    
    def draw_cursor(self, cursor_x, value, text_under=False):
        """Draw the cursor at the specified position."""
        w = self.cursor_width / 2
        oy = self.offset[1]
        self.draw_outset_box(cursor_x - w, oy + 1, cursor_x + w, oy + self.thickness, 
                             '#eee', '#fff', '#555', 'cursor')
        y = oy / 2
        if text_under:
            y += oy + self.thickness
        self.create_text(cursor_x, y, text=str(value), tags='cursor')
    
    def draw_outset_box(self, ax, ay, bx, by, bg='#bbb', outline_up='#999', 
                        outline_down='#fff', tags='background'):
        """Draw a 3D effect box."""
        self.create_rectangle(ax, ay, bx, by, fill=bg, width=0, tags=tags)
        self.create_line(ax, ay, bx, ay, fill=outline_up, tags=tags)
        self.create_line(ax, ay, ax, by, fill=outline_up, tags=tags)
        self.create_line(ax, by, bx, by, fill=outline_down, tags=tags)


if __name__ == '__main__':
    root = tk.Tk()
    DoubleScale(root).pack()
    DoubleScale(root, to=10, precision=2).pack()
    DoubleScale(root, from_=-100).pack()
    root.mainloop()