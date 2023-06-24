use relm4::{gtk, ComponentParts, ComponentSender, SimpleComponent, RelmWidgetExt, WidgetTemplate};
use relm4::gtk::prelude::*;
use crate::common::execute_command;

#[derive(Debug)]
pub struct PowerMenu {
}

#[derive(Debug)]
pub enum PowerMenuInput {
    Shutdown,
    Restart,
    Sleep,
    Logout
}

#[relm4::widget_template(pub)]
impl WidgetTemplate for MenuButton {
    view! {
        gtk::Button {
            add_css_class: "flat",
        }

    }
}

#[relm4::widget_template(pub)]
impl WidgetTemplate for MenuButtonBox {
    view! {
        gtk::Box {
            set_orientation: gtk::Orientation::Horizontal,
            set_spacing: 10,
        }
    }
}


#[relm4::component(pub)]
impl SimpleComponent for PowerMenu {
    type Input = PowerMenuInput;
    type Output = ();
    type Init = ();

    view!{
        gtk::Box {
            gtk::Button {
                inline_css: "background: transparent; padding: 0px 8px",
                gtk::Image::from_icon_name("system-shutdown-symbolic") {
                },
                connect_clicked[popover] => move |_| {
                    popover.popup();
                }

            },
            #[name = "popover"]
            gtk::Popover {
                set_has_arrow: false,
                set_offset: (-44, 8),
                gtk::Box {
                    set_orientation: gtk::Orientation::Vertical,
                    #[template]
                    MenuButton {
                        connect_clicked: |_| {
                            execute_command("shutdown now");
                        },
                        #[template]
                        MenuButtonBox {
                            gtk::Image::from_icon_name("system-shutdown-symbolic") {},
                            gtk::Label::new(Some("Shutdown")) {}
                        },
                    },
                    #[template]
                    MenuButton {
                        connect_clicked: |_| {
                            execute_command("reboot");
                        },
                        #[template]
                        MenuButtonBox {
                            gtk::Image::from_icon_name("system-reboot-symbolic") {},
                            gtk::Label::new(Some("Reboot")) {}
                        }
                    },
                    #[template]
                    MenuButton {
                        connect_clicked: |_| {
                            execute_command("hyprctl dispatch exit");
                        },
                        #[template]
                        MenuButtonBox {
                            gtk::Image::from_icon_name("system-log-out-symbolic") {},
                            gtk::Label::new(Some("Logout")) {}
                        }
                    },
                    #[template]
                    MenuButton {
                        connect_clicked: |_| {
                            execute_command("systemctl suspend");
                        },
                        #[template]
                        MenuButtonBox {
                            gtk::Image::from_icon_name("weather-clear-night-symbolic") {},
                            gtk::Label::new(Some("Sleep")) {}
                        }
                    }

                }
            }

        }
    } 

    /// Initialize the UI and model.
    fn init(
        _config: Self::Init,
        root_box: &Self::Root,
        _sender: ComponentSender<Self>,
    ) -> relm4::ComponentParts<Self> {
        let model = PowerMenu {
        };

        let widgets = view_output!();

        ComponentParts { model, widgets }
    }

    /// Update model based on message
    fn update(&mut self, message: Self::Input, _sender: ComponentSender<Self>) {
        match message {
            PowerMenuInput::Shutdown =>  {}
            PowerMenuInput::Restart =>  {}
            PowerMenuInput::Sleep =>  {}
            PowerMenuInput::Logout =>  {}
        }
    }
}
