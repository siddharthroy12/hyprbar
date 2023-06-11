from gi.repository import Gtk, GLib
import compositor
from widgets.module_container import ModuleContainer
from datetime import datetime

class Calendar(ModuleContainer):
    def __init__(self, config, window):
        super().__init__(config, window, is_button=True)
        self.label = Gtk.Label()
        self.update_date_time()
        self.set_child(self.label)

    def update_date_time(self):
        self.label.set_markup(f"<b>{self.get_date_time()}</b>")
        GLib.timeout_add(1000, self.update_date_time) 
    
    def get_date_time(self):
        now = datetime.now()
        return now.strftime("%b %d %I:%M %p")

