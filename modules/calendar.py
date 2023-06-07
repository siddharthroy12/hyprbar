from gi.repository import Gtk
import compositor
from widgets.module_container import ModuleContainer

class Calendar(ModuleContainer):
    def __init__(self, config, window):
        super().__init__(config, window)
        lable = Gtk.Label()
        lable.set_label("10:20")
        self.append(lable)


