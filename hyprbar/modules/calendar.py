from gi.repository import Gtk, GLib
from hyprbar.widgets.module_container import ModuleContainer
from datetime import datetime


class CalendarPopoverContent(Gtk.Box):
    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        calendar = Gtk.Calendar()
        self.time_label = Gtk.Label(label="13 : 56")
        self.time_label.get_style_context().add_class("title-1")
        self.time_label.get_style_context().add_class("big-date-time")
        self.date_label = Gtk.Label(label="Wednesday, 24 August")
        self.date_label.get_style_context().add_class("title-4")
        self.date_label.get_style_context().add_class("full-date")
        self.append(self.time_label)
        self.append(self.date_label)
        self.append(calendar)


class Calendar(ModuleContainer):
    def __init__(self, config, window):
        super().__init__(config, window, is_button=True)

        self.popover_content = CalendarPopoverContent()

        self.popover = Gtk.Popover()
        self.popover.set_child(self.popover_content)
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
        now = datetime.now()
        self.label.set_markup(f"<b>{now.strftime('%d %b  %I:%M %p')}</b>")
        self.popover_content.time_label.set_label(now.strftime("%I : %M"))
        self.popover_content.date_label.set_label(now.strftime("%A, %d %B"))
        GLib.timeout_add(1000, self.update_date_time)
