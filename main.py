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

from gi.repository import Gtk, Gdk, Adw
from gi.repository import Gtk4LayerShell as LayerShell
import socket
import os
from datetime import datetime
import threading
from common import Message
import json
import compositor
from default_config import default_config
from modules.app_title import AppTitle
from modules.circular_progress import CircularProgress
from modules.sni_system_tray import Tray, init_tray
from modules.workspaces import Workspaces
from modules.calendar import Calendar
from modules.system_status import SystemStatus
from modules.power_menu import PowerMenu

MODULE_MAP = {
    "workspaces": Workspaces,
    "app_title": AppTitle,
    "calendar": Calendar,
    "system_status": SystemStatus,
    "power_menu": PowerMenu
}

class HyprbarWindow(Gtk.ApplicationWindow):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config

        style_context = self.get_style_context()
        fg_color = style_context.lookup_color('accent_color')[1]
        card_bg_color = style_context.lookup_color('card_bg_color')[1]
        self.css_provider = None

        self.set_default_size(100, config["height"])

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
        
        self.set_style()
        self.setup_modules()

    def set_style(self):
        if self.css_provider != None:
            self.get_style_context().remove_provider(self.provider)

        css_provider = Gtk.CssProvider()
        css = f"""
        window.background {{
            border-radius: {self.config["bar_radius"]}px;
        }}
        button {{
            border: 1px solid white;
            }}
        """
        css_provider.load_from_data(css, len(css))
        self.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.provider = css_provider

    # Setup left, right, center modules
    # If it's already setup then it'll reload it
    def setup_modules(self):
        center_box = Gtk.CenterBox()

        for side in ["start", "center", "end"]:
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            for module in self.config[f"{side}_modules"]:
                if module in MODULE_MAP:
                    widget_of_module = MODULE_MAP[module]
                    box.append(widget_of_module(self.config, self))

            set_side_widget = getattr(center_box, f'set_{side}_widget')
            set_side_widget(box)

        self.set_child(center_box)

class Hyprbar(Adw.Application):
    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = HyprbarWindow(self.config, application=app)
        self.win.present()


def background_thread():
    socket = compositor.connect_to_hyprland_socket()

    while True:
        compositor.read_hyprland_socket(socket)



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
    # Starting background thread
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()

    app = Hyprbar(config, application_id='com.github.wmww.gtk4-layer-shell.py-example')
    app.run(None)

