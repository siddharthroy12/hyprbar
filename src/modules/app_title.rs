use crate::compositor::{Compositor, CompositorOutput};
use relm4::gtk::prelude::*;
use relm4::{gtk, ComponentParts, ComponentSender, SimpleComponent};

#[derive(Debug)]
pub struct AppTitle {
    title: String,
}

#[derive(Debug)]
pub enum AppTitleInput {
    CompositorOutput(CompositorOutput),
}

pub struct AppTitleWidgets {
    label: gtk::Label,
}

impl SimpleComponent for AppTitle {
    type Input = AppTitleInput;
    type Output = ();
    type Init = ();
    type Root = gtk::Box;
    type Widgets = AppTitleWidgets;

    fn init_root() -> Self::Root {
        let root_box = gtk::Box::new(gtk::Orientation::Horizontal, 5);
        root_box.set_css_classes(&["app-title"]);
        return root_box;
    }

    /// Initialize the UI and model.
    fn init(
        _config: Self::Init,
        root_box: &Self::Root,
        _sender: ComponentSender<Self>,
    ) -> relm4::ComponentParts<Self> {
        let model = AppTitle {
            title: Compositor::get_active_window_title(),
        };

        let label = gtk::Label::new(Some(&model.title));
        label.set_markup(&format!(
            "<b>{}</b>",
            if model.title.len() > 0 {
                &model.title
            } else {
                "-"
            }
        ));
        root_box.append(&label);

        let widgets = AppTitleWidgets { label };

        ComponentParts { model, widgets }
    }

    /// Update model based on message
    fn update(&mut self, message: Self::Input, _sender: ComponentSender<Self>) {
        match message {
            AppTitleInput::CompositorOutput(output) => match output {
                CompositorOutput::ActiveWindow(active_window) => {
                    self.title = active_window;
                }
                _ => {}
            },
        }
    }

    /// Update the view to represent the updated model.
    fn update_view(&self, widgets: &mut Self::Widgets, _sender: ComponentSender<Self>) {
        widgets.label.set_markup(&format!(
            "<b>{}</b>",
            if &self.title.len() > &0 {
                &self.title
            } else {
                "-"
            }
        ));
    }
}
