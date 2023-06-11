from gi.repository import Gtk
from hyprbar.common import add_css_to_widget


class ModuleContainer(Gtk.Box):
    def __init__(self, config, window, is_button=False):
        super().__init__()
        self.is_button = is_button
        self.container = Gtk.Button() if is_button else Gtk.Box()
        self.config = config
        self.window = window
        self.container.get_style_context().add_class("module-container")
        self.background = window.get_style_color("headerbar_bg_color")
        self.padding_x = 10
        self.padding_y = 0
        self.css_provider = None
        self.set_style()
        self.append(self.container)

    def set_style(self):
        if self.css_provider is not None:
            self.container.get_style_context()\
                .remove_provider(self.css_provider)

        css = f"""
        .module-container {{
            background: rgba({255},
                        {255},
                        {255},
                        0.08);
            border-radius: {self.config["module_radius"]}px;
            padding: {self.padding_y}px {self.padding_x}px;
            margin: 5px;
        }}
        """

        self.css_provider = add_css_to_widget(self.container, css)

    def set_child(self, child):
        if self.is_button:
            self.container.set_child(child)
        else:
            self.container.append(child)
