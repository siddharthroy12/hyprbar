# flake8: noqa
# Widget and status bar for wlroots based wayland compositors
# like Hyprland and sway
# WARNING: This is in heavy development and only supports Hyprland

# For GTK4 Layer Shell to get linked before libwayland-client
# we must explicitly load it before importing with gi

import gi
from ctypes import CDLL
gi.require_version("Gtk4LayerShell", "1.0")
CDLL("libgtk4-layer-shell.so")

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gdk
from gi.repository import Gtk4LayerShell as LayerShell
import os
import threading
import json
import hyprbar.compositor as compositor
from hyprbar.default_config import default_config
from hyprbar.modules.app_title import AppTitle
from hyprbar.modules.workspaces import Workspaces
from hyprbar.modules.calendar import Calendar
from hyprbar.modules.system_status import SystemStatus
from hyprbar.modules.power_menu import PowerMenu


MODULE_MAP = {
    "workspaces": Workspaces,
    "app_title": AppTitle,
    "calendar": Calendar,
    "system_status": SystemStatus,
    "power_menu": PowerMenu,
}


class HyprbarWindow(Gtk.ApplicationWindow):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
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
        LayerShell.set_margin(self, LayerShell.Edge.LEFT,
                              config["margin_left"])
        LayerShell.set_margin(self, LayerShell.Edge.RIGHT,
                              config["margin_right"])
        LayerShell.set_margin(self, LayerShell.Edge.BOTTOM,
                              config["margin_bottom"])
        LayerShell.auto_exclusive_zone_enable(self)

        self.set_style()
        self.setup_modules()

    def set_style(self):
        if self.css_provider is not None:
            self.get_style_context().remove_provider(self.provider)


        css_provider = Gtk.CssProvider()
        css = f"""
        window.background {{
            border-radius: {self.config["bar_radius"]}px;
        }}
        calendar.view {{
            border: none;
            border-radius: 10px;
            padding: 20px 20px;
        }}
        calendar.view header {{
            border: none;
        }}

        calendar grid label {{
            border-radius: 100px;
            padding: 9px 0;
        }}

        calendar button {{
            border-radius: 100px;
        }}

        .big-date-time {{
            font-size: 60px;
            margin-bottom: 5px;
            margin-top: 20px;
        }}

        .full-date {{
            margin-bottom: 30px;
        }}
        """

        css_provider.load_from_data(css, len(css))
        self.get_style_context().add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
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

            set_side_widget = getattr(center_box, f"set_{side}_widget")
            set_side_widget(box)

        self.set_child(center_box)


class Hyprbar(Adw.Application):
    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = HyprbarWindow(self.config, application=app)
        self.win.present()


def background_thread():
    socket = compositor.connect_to_hyprland_socket()

    while True:
        compositor.read_hyprland_socket(socket)


def main():
    config = default_config
    config_path = "~/.config/hyprbar/config.json"
    if os.path.exists(config_path):
        try:
            config_file = open(os.path.expanduser(
                "~/.config/hyprbar/config.json"))
            data = json.load(config_file)
            config = config | data
            print(f"Using config from {config_path}")
        except (any):
            print(
                f"Failed to load config from {config_path},\
                using default config")
    print(config)
    # Starting background thread
    thread = threading.Thread(target=background_thread)
    thread.daemon = True
    thread.start()

    app = Hyprbar(
        config, application_id="com.github.wmww.gtk4-layer-shell.py-example")
    app.run(None)
