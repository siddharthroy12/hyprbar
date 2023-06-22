use chrono::{DateTime, Local};
use relm4::gtk::prelude::*;
use relm4::{gtk, Component, ComponentParts, ComponentSender};
use std::{thread, time};

#[derive(Debug, Clone)]
pub struct Calendar {
    current_time: DateTime<Local>,
}

#[derive(Debug)]
pub enum CalendarInput {
    UpdateCurrentTime,
}

#[derive(Debug)]
pub enum CommandMsg {
    LocalTime(DateTime<Local>),
}

#[relm4::component(pub)]
impl Component for Calendar {
    type CommandOutput = CommandMsg;
    type Input = CalendarInput;
    type Output = ();
    type Init = ();

    view! {
        gtk::Box {
            gtk::Button {
                set_css_classes: &["calendar-toggle-button"],
                gtk::Label {
                    #[watch]
                    set_label: &model.current_time.format("%d %b %I:%M %p").to_string()
                },
                connect_clicked[popover] => move |_| {
                    popover.popup();
                }
            },
            #[name = "popover"]
            gtk::Popover {
                set_has_arrow: false,
                set_offset: (0, 8),
                gtk::Box {
                    set_orientation: gtk::Orientation::Vertical,
                    gtk::Label {
                        set_css_classes: &["title-1", "big-date-time"],
                        #[watch]
                        set_label: &model.current_time.format("%I : %M").to_string()
                    },
                    gtk::Label {
                        set_css_classes: &["title-4", "full-date"],
                        #[watch]
                        set_label: &model.current_time.format("%A, %d %B").to_string()
                    },
                    gtk::Calendar {}
                }
            }
        }
    }

    /// Initialize the UI and model.
    fn init(
        _config: Self::Init,
        root_box: &Self::Root,
        sender: ComponentSender<Self>,
    ) -> relm4::ComponentParts<Self> {
        let model = Calendar {
            current_time: Local::now(),
        };

        let widgets = view_output!();

        let _ = sender.input_sender().send(CalendarInput::UpdateCurrentTime);

        ComponentParts { model, widgets }
    }

    /// Update model based on message
    fn update(&mut self, msg: Self::Input, sender: ComponentSender<Self>, _: &Self::Root) {
        match msg {
            CalendarInput::UpdateCurrentTime => {
                sender.oneshot_command(async {
                    thread::sleep(time::Duration::from_secs(1));
                    // Run async background task
                    CommandMsg::LocalTime(Local::now())
                });
            }
        }
    }

    // Update model based of command output
    fn update_cmd(
        &mut self,
        message: Self::CommandOutput,
        sender: ComponentSender<Self>,
        _: &Self::Root,
    ) {
        match message {
            CommandMsg::LocalTime(time) => {
                self.current_time = time;
                let _ = sender.input_sender().send(CalendarInput::UpdateCurrentTime);
            }
        }
    }
}
