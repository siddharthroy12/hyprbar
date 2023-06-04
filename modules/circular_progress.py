import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from math import pi as PI

class CircularProgress(Gtk.DrawingArea):
    def __init__(self, config, progress, radius=5, stroke_width=2, color=(225, 225, 225)):
        super().__init__()

        self.radius = radius
        self.color = color
        self.progress = progress
        self.stroke_width = stroke_width
        self.get_parent()
        self.set_content_width(config["height"])
        self.set_content_height(config["height"])
        self.set_draw_func(self.on_draw)


    def set_progress(self, progress):
        self.progress = progress
        self.queue_draw()

    def on_draw(self, area, cr, width, height):
        cr.set_source_rgb(*self.color)

        center_x = width / 2.0
        center_y = height / 2.0

        start_angle = 0
        end_angle = (self.progress / 100.0) * 2.0 * PI

        cr.arc(center_x, center_y, self.radius, start_angle, end_angle)
        cr.stroke() 

