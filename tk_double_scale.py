import tkinter as tk
from dataclasses import dataclass


@dataclass
class Cursor:
    width: int
    height: int
    value: float
    y1: int
    y2: int
    text_under: bool = False
    
    def __post_init__(self):
        pass


@dataclass
class DoubleScale(tk.Canvas): 
    master: tk.Widget
    from_: float = 0        # value min
    to: float = 100         # value max
    length: int = 100       # widget length and thickness in pixels
    thickness: int = 15
    cursor_width: int = 10
    offset_x: int = 5       # widget top left corner
    offset_y: int = 15
    precision: int = 0      # number of decimals (value <= 0: int, value > 0: float)
    
    def __post_init__(self):
        w = self.length + (self.offset_x * 2) + self.cursor_width
        h = self.thickness + (self.offset_y * 2)
        super().__init__(self.master, width=w, height=h)
        
        # Initialize parameters
        self.precision = abs(self.precision)
        self.cursor_half = self.cursor_width / 2
        self.inside_offset = self.cursor_half + 1
        oy = self.offset_y
        self.cursor_y_delimiter = oy + (self.thickness / 2)
        self.cursor_y_a = [oy + 1, self.cursor_y_delimiter - 1]
        self.cursor_y_b = [self.cursor_y_delimiter, oy + self.thickness - 1]
        self.text_y = [oy / 2, oy / 2 + oy + self.thickness]
        self.coeff = self.length / (self.to - self.from_)
        
        cursor_height = self.thickness - 3 / 2
        self.cursor_a = Cursor(
            self.cursor_width, 
            cursor_height, 
            value=self.from_, 
            y1=self.offset_y + 1, 
            y2=self.cursor_y_delimiter - 1
        )
        self.cursor_b = Cursor(
            self.cursor_width, 
            cursor_height, 
            value=self.to, 
            y1=self.cursor_y_delimiter, 
            y2=self.offset_y + self.thickness - 1,
            text_under = True
        )
        
        self.draw_background()
        self.redraw()
        
        # Bind mouse events
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
    
    def get_values(self):
        return [self.cursor_a.value, self.cursor_b.value]
    
    def set_values(self, a, b):
        self.cursor_a.value = a
        self.cursor_b.value = b
        self.redraw()
    
    def value_to_position(self, value):
        """Convert a value to its corresponding position on the scale."""
        return (value - self.from_) * self.coeff + self.offset_x + self.inside_offset
    
    def position_to_value(self, position):
        """Convert a position on the scale back to a value."""
        return (position - self.offset_x - self.inside_offset) / self.coeff + self.from_
    
    def pos_to_value_rounded(self, position):
        new_value = round(self.position_to_value(position), self.precision)
        return int(new_value) if self.precision == 0 else new_value
    
    def on_click(self, event):
        """Determine which value is being dragged."""
        self.dragged_cursor = None
        xa = self.value_to_position(self.cursor_a.value)
        xb = self.value_to_position(self.cursor_b.value)
        
        if self.cursor_a.value == self.cursor_b.value:
            
            if self.cursor_a.value == self.from_:
                self.dragged_cursor = self.cursor_b
            
            elif self.cursor_b.value == self.to:
                self.dragged_cursor = self.cursor_a
            
            elif abs(event.x - xa) < 10:
                # use y to determine which cursor should be moved
                self.dragged_cursor = (self.cursor_a if event.y < self.cursor_y_delimiter 
                                       else self.cursor_b)
        
        elif abs(event.x - xa) < 10:
            self.dragged_cursor = self.cursor_a
        
        elif abs(event.x - xb) < 10:
            self.dragged_cursor = self.cursor_b
    
    def on_drag(self, event):
        """Update the value based on the drag position."""
        if self.dragged_cursor:
            new_value = self.pos_to_value_rounded(event.x)
            
            if self.dragged_cursor == self.cursor_a:
                self.cursor_a.value = max(self.from_, min(new_value, self.cursor_b.value))
            
            elif self.dragged_cursor == self.cursor_b:
                self.cursor_b.value = min(self.to, max(new_value, self.cursor_a.value))
            
            self.redraw()
    
    def draw_background(self):
        """Draw the background of the scale."""
        bx = self.offset_x + self.length + self.cursor_width + 2
        by = self.offset_y + self.thickness
        self.draw_outset_box(self.offset_x, self.offset_y, bx, by)
    
    def redraw(self):
        """Redraw the scale and the cursor positions."""
        self.delete('cursor')
        self.draw_cursor(self.cursor_a)
        self.draw_cursor(self.cursor_b)
    
    def draw_cursor(self, cursor):
        """Draw the cursor at the specified position."""
        x = self.value_to_position(cursor.value)
        
        cursor_y = self.cursor_y_b if cursor.text_under else self.cursor_y_a
        self.draw_outset_box(x - self.cursor_half, cursor_y[0], 
                             x + self.cursor_half, cursor_y[1], 
                             '#eee', '#fff', '#555', 'cursor')
        
        y = self.text_y[1] if cursor.text_under else self.text_y[0]
        self.create_text(x, y, text=str(cursor.value), tags='cursor')
    
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
    DoubleScale(root, to=10, precision=1).pack()
    DoubleScale(root, to=1, precision=-2).pack()
    DoubleScale(root, from_=-100).pack()
    DoubleScale(root, offset_y=40).pack()
    root.mainloop()