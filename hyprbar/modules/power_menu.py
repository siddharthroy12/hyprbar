from gi.repository import Gtk
from hyprbar.widgets.module_container import ModuleContainer
from hyprbar.common import run_command

OPTIONS = [
    {
        "title": "Shutdown",
        "icon": "system-shutdown-symbolic",
        "command": "shutdown now",
    },
    {"title": "Reboot", "icon": "system-reboot-symbolic", "command": "reboot"},
    {
        "title": "Logout",
        "icon": "system-log-out-symbolic",
        "command": "hyprctl dispatch exit",
    },
    {
        "title": "Sleep",
        "icon": "weather-clear-night-symbolic",
        "command": "systemctl suspend",
    },
]


class PowerMenu(ModuleContainer):
    def __init__(self, config, window):
        super().__init__(config, window, is_button=True)
        shutdown_icon = Gtk.Image.new_from_icon_name(
            "system-shutdown-symbolic")
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        for option in OPTIONS:
            button = Gtk.Button()
            button.add_css_class("flat")
            button_box = Gtk.Box(
                orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            button_box.append(Gtk.Image.new_from_icon_name(option["icon"]))
            button_box.append(Gtk.Label(label=option["title"]))
            button.set_child(button_box)

            # command=option["command"] is needed
            # to sure all functions don't end up being the same
            def on_click(_, command=option["command"]):
                run_command(command)

            button.connect("clicked", on_click)
            box.append(button)

        self.set_child(shutdown_icon)

        self.popover = Gtk.Popover()
        self.popover.set_child(box)
        self.popover.set_position(Gtk.PositionType.BOTTOM)
        self.popover.set_has_arrow(False)
        self.popover.set_offset(-42, 8)
        self.popover.set_parent(self.container)
        self.container.connect("clicked", self.on_click)

    def on_click(self, window):
        self.popover.popup()
