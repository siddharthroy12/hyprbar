from gi.repository import Gtk
from hyprbar.widgets.module_container import ModuleContainer
from hyprbar import system


class SystemStatus(ModuleContainer):
    def __init__(self, config, window):
        super().__init__(config, window, is_button=True)
        system.battery.add_listener(lambda value: print(value))
        self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

        # Create a horizontal box container
        self.set_child(self.box)

        # Load the battery icon
        self.battery_box = Gtk.Box()
        battery_icon = Gtk.Image.new_from_icon_name("battery-full-symbolic")
        self.battery_box.append(battery_icon)
        self.box.append(self.battery_box)

        # Load the Wi-Fi icon
        wifi_icon = Gtk.Image.new_from_icon_name(
            "network-wireless-signal-excellent-symbolic"
        )
        self.box.append(wifi_icon)

        # Load the sound icon
        sound_icon = Gtk.Image.new_from_icon_name("audio-volume-high-symbolic")
        self.box.append(sound_icon)
