from gi.repository import Gtk


class ModuleContainer(Gtk.Box):
    def __init__(self, config, window, is_button=False):
        super().__init__()
        self.is_button = is_button
        self.container = Gtk.Button() if is_button else Gtk.Box()
        self.config = config
        self.window = window
        self.container.get_style_context().add_class("module-container")
        self.background = self.get_style_color("card_bg_color")
        self.padding_x = 10
        self.padding_y = 0
        self.css_provider = None
        self.set_style()
        self.append(self.container)

    def set_style(self):
        if self.css_provider is not None:
            self.container.get_style_context()\
                .remove_provider(self.css_provider)

        css_provider = Gtk.CssProvider()
        css = f"""
        .module-container {{
            background: rgba({self.background.red*255},
                        {self.background.green*255},
                        {self.background.blue*255},
                        {self.background.alpha});
            border-radius: {self.config["module_radius"]}px;
            padding: {self.padding_y}px {self.padding_x}px;
            margin: 5px;
        }}
        """
        css_provider.load_from_data(css, len(css))
        self.container.get_style_context().add_provider(
            css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.css_provider = css_provider

    def get_style_color(self, color):
        style_context = self.window.get_style_context()
        return style_context.lookup_color(color)[1]

    def set_child(self, child):
        if self.is_button:
            self.container.set_child(child)
        else:
            self.container.append(child)
