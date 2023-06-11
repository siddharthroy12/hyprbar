from gi.repository import Gtk
from widgets.module_container import ModuleContainer


class SystemStatus(ModuleContainer):
    def __init__(self, config, window):
        super().__init__(config, window, is_button=True)
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        # Create a horizontal box container
        self.set_child(self.box)

        # Load the battery icon
        battery_icon = Gtk.Image.new_from_icon_name("battery-full-symbolic")
        self.box.append(battery_icon)

        # Load the Wi-Fi icon
        wifi_icon = Gtk.Image.new_from_icon_name(
            "network-wireless-signal-excellent-symbolic"
        )
        self.box.append(wifi_icon)

        # Load the sound icon
        sound_icon = Gtk.Image.new_from_icon_name("audio-volume-high-symbolic")
        self.box.append(sound_icon)
