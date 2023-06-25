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
            gtk::Box {
                set_orientation: gtk::Orientation::Horizontal,
                set_spacing: 10,
                #[name = "image"]
                gtk::Image {},
                #[name = "label"]
                gtk::Label {}
            }
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
                set_css_classes: &["popover-padding"],
                set_has_arrow: false,
                gtk::Box {
                    set_orientation: gtk::Orientation::Vertical,
                    #[template]
                    MenuButton {
                        connect_clicked: |_| {
                            execute_command("shutdown now");
                        },
                        #[template_child]
                        image {
                            set_from_icon_name: Some("system-shutdown-symbolic"),
                        },
                        #[template_child]
                        label {
                            set_label: "Shutdown"
                        }
                    },
                    #[template]
                    MenuButton {
                        connect_clicked: |_| {
                            execute_command("reboot");
                        },
                        #[template_child]
                        image {
                            set_from_icon_name: Some("system-reboot-symbolic"),
                        },
                        #[template_child]
                        label {
                            set_label: "Reboot"
                        }
                    },
                    #[template]
                    MenuButton {
                        connect_clicked: |_| {
                            execute_command("hyprctl dispatch exit");
                        },
                        #[template_child]
                        image {
                            set_from_icon_name: Some("system-log-out-symbolic"),
                        },
                        #[template_child]
                        label {
                            set_label: "Logout"
                        }
                    },
                    #[template]
                    MenuButton {
                        connect_clicked: |_| {
                            execute_command("systemctl suspend");
                        },
                        #[template_child]
                        image {
                            set_from_icon_name: Some("weather-clear-night-symbolic"),
                        },
                        #[template_child]
                        label {
                            set_label: "Sleep"
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
