import tkinter as tk
from dataclasses import dataclass


@dataclass
class DoubleScale(tk.Canvas): 
    master: tk.Widget
    from_: float = 0
    to: float = 100
    length: int = 100
    thickness: int = 15
    cursor_width: int = 10
    offset_x: int = 5
    offset_y: int = 15
    precision: int = 0
    
    def __post_init__(self):
        w = self.length + (self.offset_x * 2) + self.cursor_width
        h = self.thickness + (self.offset_y * 2)
        super().__init__(self.master, width=w, height=h)
        
        # Initialize parameters
        self.cursor_half = self.cursor_width / 2
        self.inside_offset = self.cursor_half + 1
        oy = self.offset_y
        self.cursor_y = [oy + 1, oy + self.thickness]
        self.text_y = [oy / 2, oy / 2 + oy + self.thickness]
        self.coeff = self.length / (self.to - self.from_)
        self.value_a = self.from_
        self.value_b = self.to
        
        self.draw_background()
        self.redraw()
        
        # Bind mouse events
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
    
    def value_to_position(self, value):
        """Convert a value to its corresponding position on the scale."""
        return (value - self.from_) * self.coeff + self.offset_x + self.inside_offset
    
    def position_to_value(self, position):
        """Convert a position on the scale back to a value."""
        return (position - self.offset_x - self.inside_offset) / self.coeff + self.from_
    
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
                self.value_a = max(self.from_, min(new_value, self.value_b))
            elif self.dragging_value == 'value_b':
                self.value_b = min(self.to, max(new_value, self.value_a))
            self.redraw()
    
    def draw_background(self):
        """Draw the background of the scale."""
        bx = self.offset_x + self.length + self.cursor_width + 2
        by = self.offset_y + self.thickness
        self.draw_outset_box(self.offset_x, self.offset_y, bx, by)
    
    def redraw(self):
        """Redraw the scale and the cursor positions."""
        self.delete('cursor')
        self.draw_cursor(self.value_to_position(self.value_a), self.value_a)
        self.draw_cursor(self.value_to_position(self.value_b), self.value_b, True)
    
    def draw_cursor(self, x, value, text_under=False):
        """Draw the cursor at the specified position."""
        self.draw_outset_box(x - self.cursor_half, self.cursor_y[0], 
                             x + self.cursor_half, self.cursor_y[1], 
                             '#eee', '#fff', '#555', 'cursor')
        
        y = self.text_y[1] if text_under else self.text_y[0]
        self.create_text(x, y, text=str(value), tags='cursor')
    
    def draw_outset_box(self, ax, ay, bx, by, bg='#bbb', outline_up='#999', 
                        outline_down='#fff', tags='background'):
        """Draw a 3D effect box."""
        self.create_rectangle(ax, ay, bx, by, fill=bg, width=0, tags=tags)
        self.create_line(ax, ay, bx, ay, fill=outline_up, tags=tags)
        self.create_line(ax, ay, ax, by, fill=outline_up, tags=tags)
        self.create_line(ax, by, bx, by, fill=outline_down, tags=tags)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('DoubleScale testing')
    root.geometry('300x300+1000+200')
    DoubleScale(root).pack()
    DoubleScale(root, to=10, precision=2).pack()
    DoubleScale(root, from_=-100).pack()
    DoubleScale(root, offset_y=40).pack()
    root.mainloop()