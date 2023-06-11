from gi.repository import Gtk
import compositor
from widgets.module_container import ModuleContainer

class AppTitle(ModuleContainer):
    def __init__(self, config, window):
        super().__init__(config, window)
        lable = Gtk.Label()
        compositor.active_window_title.add_listener(lambda value : lable.set_markup(f"<b>{value if len(value) else '-'}</b>"))
        self.set_child(lable)


