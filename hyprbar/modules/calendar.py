from gi.repository import Gtk, GLib
from hyprbar.widgets.module_container import ModuleContainer
from datetime import datetime


class Calendar(ModuleContainer):
    def __init__(self, config, window):
        super().__init__(config, window, is_button=True)

        box = Gtk.Box()

        calendar = Gtk.Calendar()
        box.append(calendar)

        self.popover = Gtk.Popover()
        self.popover.set_child(box)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        self.popover.set_has_arrow(False)
        self.popover.set_offset(0, 8)
        self.popover.set_parent(self.container)
        self.container.connect("clicked", self.on_click)

        self.label = Gtk.Label()
        self.update_date_time()
        self.set_child(self.label)

    def on_click(self, window):
        self.popover.popup()

    def update_date_time(self):
        self.label.set_markup(f"<b>{self.get_date_time()}</b>")
        GLib.timeout_add(1000, self.update_date_time)

    def get_date_time(self):
        now = datetime.now()
        return now.strftime("%b %d %I:%M %p")
