import subprocess
import math
from gi.repository import Gtk


# Run command and return output
def run_command(command):
    call_result = subprocess.run(command.split(
        " "), stdout=subprocess.PIPE, text=True)
    return call_result.stdout


def is_point_in_circle(
    point_x, point_y, circle_center_x, circle_center_y, circle_radius
):
    distance = math.sqrt(
        (point_x - circle_center_x) ** 2 + (point_y - circle_center_y) ** 2
    )
    return distance <= circle_radius


def add_css_to_widget(widget, css):
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(css, len(css))
    widget.get_style_context().add_provider(
        css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    return css_provider


# PUB/SUB
class Message:
    def __init__(self, initialValue):
        self._value = initialValue
        self.listiners = []

    def add_listener(self, callback):
        self.listiners.append(callback)
        callback(self._value)

    def get_value(self):
        return self._value

    def set_value(self, value):
        for listiner in self.listiners:
            listiner(value)
        self._value = value
