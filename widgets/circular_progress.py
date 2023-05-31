class CircularProgress(Gtk.DrawingArea):
    def __init__(self, config, radius, stroke_width, color):
        super().__init__()

        self.radius = 10
        self.color = color
        self.progress = 50
        self.get_parent()
        self.set_content_width(config["height"])
        self.set_content_height(config["height"])
        self.set_draw_func(self.on_draw)


    def set_progress(self, progress):
        self.progress = progress
        self.queue_draw()

    def on_draw(self, area, cr, width, height):
        cr.set_source_rgb(0.5, 0.5, 0.9)

        center_x = width / 2.0
        center_y = height / 2.0

        start_angle = 0
        end_angle = (self.progress / 100.0) * 2.0 * PI

        cr.arc(center_x, center_y, self.radius,
             start_angle, end_angle)
        cr.stroke() 

