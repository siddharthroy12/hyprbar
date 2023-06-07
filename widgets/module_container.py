from gi.repository import Gtk
import compositor

class ModuleContainer(Gtk.Box):
    def __init__(self, config, window):
        super().__init__()
        self.config = config
        self.window = window
        self.get_style_context().add_class("module-container")
        self.css_provider = None
        self.set_style()
    
    def set_style(self):
        if self.css_provider != None:
            self.get_style_context().remove_provider(self.provider)

        card_bg_color = self.get_style_color("card_bg_color")
        css_provider = Gtk.CssProvider()
        css = f"""
        .module-container {{
            background: rgba({card_bg_color.red*255}, {card_bg_color.green*255}, {card_bg_color.blue*255}, {card_bg_color.alpha});
            border-radius: {self.config["module_radius"]}px;
            padding: 0 15px;
            margin: 5px;
        }}
        """
        css_provider.load_from_data(css, len(css))
        self.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        self.css_provider = css_provider

    def get_style_color(self, color):
        style_context = self.window.get_style_context()
        return style_context.lookup_color(color)[1]



    
