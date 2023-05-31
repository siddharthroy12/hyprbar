# Widget and status bar for wlroots based wayland compositors
# like Hyprland and sway
# WARNING: This is in heavy development, only supports Hyprland, and I have no idea
# who this will end up

# For GTK4 Layer Shell to get linked before libwayland-client we must explicitly load it before importing with gi
from ctypes import CDLL
CDLL('libgtk4-layer-shell.so')

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
gi.require_version('Gtk4LayerShell', '1.0')

#type: ignore
from gi.repository import Gtk, Gdk, Adw
from gi.repository import Gtk4LayerShell as LayerShell
import socket
import os
import threading
from common import Message
import json
import compositor
from default_config import default_config
import compositor
from widgets import AppTitle, CircularProgress
from nwg_panel.modules import sni_system_tray

class HyprbarWindow(Gtk.ApplicationWindow):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configuraiton = config

        self.set_default_size(100, config["height"])

        # Load the stylesheet
        if "stylesheet" in config:
            css_provider = Gtk.CssProvider()
            css_provider.load_from_path(os.path.expanduser(config["stylesheet"]))
            Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # Setup our Lord and saviour LayerShell that
        # made this bar and widget thing possible
        # on wl-roots based Wayland compositors like Sway and Hyprland
        LayerShell.init_for_window(self)
        LayerShell.set_layer(self, LayerShell.Layer.TOP)
        LayerShell.set_anchor(self, LayerShell.Edge.TOP, True)
        LayerShell.set_anchor(self, LayerShell.Edge.LEFT, True)
        LayerShell.set_anchor(self, LayerShell.Edge.RIGHT, True)
        LayerShell.set_margin(self, LayerShell.Edge.TOP, config["margin_top"])
        LayerShell.set_margin(self, LayerShell.Edge.LEFT, config["margin_left"])
        LayerShell.set_margin(self, LayerShell.Edge.RIGHT, config["margin_right"])
        LayerShell.set_margin(self, LayerShell.Edge.BOTTOM, config["margin_bottom"])
        LayerShell.auto_exclusive_zone_enable(self)

        center_box = Gtk.CenterBox()
        button_left = Gtk.Button(label="Something on left")
        button_right = Gtk.Button(label="Something on right")
        center_box.set_start_widget(CircularProgress(config, 0, 0 ,0))
        center_box.set_center_widget(AppTitle())
        center_box.set_end_widget(sni_system_tray)
        self.set_child(center_box)

class Hyprbar(Adw.Application):
    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = HyprbarWindow(self.config, application=app)
        self.win.present()


if __name__ == "__main__":
    config = default_config
    config_path = "~/.config/hyprbar/config.json"
    if os.path.exists(config_path):
        try:
            config_file = open(os.path.expanduser('~/.config/hyprbar/config.json'))
            data = json.load(config_file)
            config = config | data
            print(f"Using config from {config_path}")
        except:
            print(f"Failed to load config from {config_path}, using default config");
    print(config)
    app = Hyprbar(config, application_id='com.github.wmww.gtk4-layer-shell.py-example')
    app.run(None)

