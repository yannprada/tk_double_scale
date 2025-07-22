import tkinter as tk
from dataclasses import dataclass


@dataclass
class Cursor:
    width: int
    height: int
    value: float
    y1: int
    y2: int
    text_y: int
    text_under: bool = False
    
    def __post_init__(self):
        self.half_width = self.width / 2


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
    decimals: int = 0       # number of decimals
    bg_color: str = '#bbb'
    bg_outline_up: str = '#999'
    bg_outline_down: str = '#fff'
    cursor_color: str = '#eee'
    cursor_outline_up: str = '#fff'
    cursor_outline_down: str = '#555'
    
    def __post_init__(self):
        width = self.length + (self.offset_x * 2) + self.cursor_width
        height = self.thickness + (self.offset_y * 2)
        super().__init__(self.master, width=width, height=height)
        
        # Initialize parameters
        self.decimals = abs(self.decimals)
        self.inside_offset = self.cursor_width / 2 + 1
        self.cursor_y_delimiter = self.offset_y + (self.thickness / 2)
        self.coeff = self.length / (self.to - self.from_)
        
        cursor_height = (self.thickness - 3) / 2
        self.cursor_a = Cursor(
            self.cursor_width, 
            cursor_height, 
            value=self.from_, 
            y1=self.offset_y + 1, 
            y2=self.cursor_y_delimiter - 1,
            text_y=self.offset_y / 2
        )
        self.cursor_b = Cursor(
            self.cursor_width, 
            cursor_height, 
            value=self.to, 
            y1=self.cursor_y_delimiter, 
            y2=self.offset_y + self.thickness - 1,
            text_y=self.offset_y * 1.5 + self.thickness,
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
        return ((value - self.from_) * self.coeff + self.offset_x 
                + self.inside_offset)
    
    def position_to_value(self, position):
        """Convert a position on the scale back to a value."""
        return ((position - self.offset_x - self.inside_offset) / self.coeff 
                + self.from_)
    
    def pos_to_value_rounded(self, position):
        """Convert a position on the scale back to a value, rounded."""
        return round(self.position_to_value(position), self.decimals)
    
    def on_click(self, event):
        """Determine which cursor is being dragged."""
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
                self.dragged_cursor = (self.cursor_a 
                                       if event.y < self.cursor_y_delimiter 
                                       else self.cursor_b)
        
        elif abs(event.x - xa) < 10:
            self.dragged_cursor = self.cursor_a
        
        elif abs(event.x - xb) < 10:
            self.dragged_cursor = self.cursor_b
    
    def on_drag(self, event):
        """Update the value based on the cursor position, and redraw the cursors."""
        if self.dragged_cursor:
            new_value = self.pos_to_value_rounded(event.x)
            
            if self.dragged_cursor == self.cursor_a:
                self.cursor_a.value = max(self.from_, min(new_value, 
                                                          self.cursor_b.value))
            
            elif self.dragged_cursor == self.cursor_b:
                self.cursor_b.value = min(self.to, max(new_value, 
                                                       self.cursor_a.value))
            
            self.redraw()
    
    def draw_background(self):
        """Draw the background of the scale."""
        xb = self.offset_x + self.length + (self.inside_offset * 2)
        yb = self.offset_y + self.thickness
        self.draw_outset_box(
            self.offset_x, self.offset_y, xb, yb, self.bg_color, 
            self.bg_outline_up, self.bg_outline_down, tags='background'
        )
    
    def redraw(self):
        """Redraw the cursors."""
        self.delete('cursor')
        self.draw_cursor(self.cursor_a)
        self.draw_cursor(self.cursor_b)
    
    def draw_cursor(self, cursor):
        """Draw the cursor."""
        x = self.value_to_position(cursor.value)
        
        self.draw_outset_box(x - cursor.half_width, cursor.y1, 
                             x + cursor.half_width, cursor.y2, 
                             self.cursor_color, self.cursor_outline_up, 
                             self.cursor_outline_down, tags='cursor')
        
        display_val = int(cursor.value) if self.decimals == 0 else cursor.value
        self.create_text(x, cursor.text_y, text=str(display_val), tags='cursor')
    
    def draw_outset_box(self, xa, ya, xb, yb, bg_color, outline_up, 
                        outline_down, tags):
        """Draw a 3D effect box."""
        self.create_rectangle(xa, ya, xb, yb, fill=bg_color, width=0, tags=tags)
        self.create_line(xa, ya, xb, ya, fill=outline_up, tags=tags)
        self.create_line(xa, ya, xa, yb, fill=outline_up, tags=tags)
        self.create_line(xa, yb, xb, yb, fill=outline_down, tags=tags)
        self.create_line(xb, ya, xb, yb, fill=outline_down, tags=tags)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('DoubleScale testing')
    root.geometry('300x500+1000+200')
    DoubleScale(root).pack()
    DoubleScale(root, to=10, decimals=1).pack()
    DoubleScale(root, to=1, decimals=-2).pack()
    DoubleScale(root, from_=-100).pack()
    DoubleScale(root, offset_y=40, cursor_color='blue', 
                cursor_outline_up='lightblue', cursor_outline_down='darkblue', 
                bg_color='#0ff').pack()
    DoubleScale(root, length=50).pack()
    DoubleScale(root, length=200, thickness=30, cursor_width=30).pack()
    root.mainloop()