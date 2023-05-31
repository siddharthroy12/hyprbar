class AppTitle(Gtk.Label):
    def __init__(self):
        super().__init__()
        compositor.active_window_title.add_listener(lambda value : self.set_label(value))


