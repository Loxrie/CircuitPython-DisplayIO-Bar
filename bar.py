# Write your code here :-)
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
import terminalio
import displayio
import math

class Bar(displayio.Group):
    def __init__(self, min_val, max_val, width, height, n_segments=12,
                 colours=[
                    0x00FF00, 0x00FF00, 0x00FF00, # Green 0-2
                    0xFFFF00, 0xFFFF00, 0xFFFF00, # Yellow 3-5
                    0xFF6400, 0xFF6400,           # Amber 6-7
                    0xFF0000, 0xFF0000, 0xFF0000, # Red 8-10
                    0x7F00FF                      # Violet 11+
                ] , display_value=True,
                 label="", arc_colour=0xFF0000, colour_fade=False):
        super().__init__()
        self.min_val = min_val
        self.max_val = max_val
        self.width = width
        self.height = height
        self.n_segments = n_segments
        self.colours = colours

        self.d_label = Label(terminalio.FONT, text=label, color=0xFFFFFF)
        self.data = Label(terminalio.FONT, text=label, color=0xFFFFFF)
        self.direction = self.height > self.width

        self.prospective_label_width = 0
        if self.direction:
            self.colours.reverse()
            self.data.x = 0
            self.data.y = self.height - self.data.height
            self.d_label.x = 0
            self.d_label.y = self.data.y - self.d_label.height
            self.segment_size = round((self.d_label.y - 15) / self.n_segments)
        else:
            self.d_label.x = 0
            self.d_label.y = 0
            self.data.x = 0
            self.data.y = self.d_label.height
            d_label = Label(terminalio.FONT, text=f"{self.max_val}.0", color=0xFFFFFF)
            self.prospective_label_width = d_label.width + 10
            self.segment_size = round((self.width - self.prospective_label_width) / self.n_segments)

        super().append(self.d_label)
        super().append(self.data)
        self.segments = draw_segments(self.width, self.height, self.segment_size, self.n_segments, self.colours, direction=self.direction, label_width=self.prospective_label_width)
        for segment in self.segments: super().append(segment)

    def update(self, value):
        segment_width = self.max_val / self.n_segments
        index = round(value / segment_width)
        num_hidden = 0
        num_to_hide = self.n_segments - index
        #print(f"V: {value} SW: {segment_width} I: {index} NTH: {num_to_hide}")
        t_iter = iter(self) if (self.direction) else iter(reversed(self))
        for layer in t_iter:
            if type(layer) is Rect:
                if num_hidden < num_to_hide:
                    num_hidden = num_hidden + 1
                    layer.hidden = True
                else:
                    layer.hidden = False
        self.data.text = f"{value}"

def draw_segments(width, height, segment_size, number_segments, colours, direction = 1, label_width = 0):
    segments = []
    for i in range(0, number_segments):
        this_colour = colours[i]
        if (direction == 1):
            segment = Rect(0, segment_size * i, width, segment_size, fill=this_colour)
        else:
            segment = Rect((segment_size * i) + label_width,0, segment_size, height, fill=this_colour)
        segment.hidden = True
        segments.append(segment)

    return segments
