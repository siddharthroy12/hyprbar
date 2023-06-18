use relm4::{gtk::{prelude::*, glib::SignalHandlerId}, RelmRemoveAllExt};
use gtk::glib::clone;
use relm4::{gtk, ComponentParts, ComponentSender, SimpleComponent};
use crate::compositor::{Compositor, CompositorOutput};

#[tracker::track]
#[derive(Debug)]
pub struct Workspaces {
    workspaces: Vec<i32>,
    active_workspace: i32,
}

#[derive(Debug)]
pub enum WorkspacesInput {
    CompositorOutput(CompositorOutput)
}

pub struct WorkspacesWidgets {
    buttons_container: gtk::Box,
    radio_buttons: Vec::<gtk::CheckButton>,
    // Signal handlers are stored to block the signal
    // that changes current workspace when the state of the toggle button is changed
    // programatically which could cause a loop
    signal_handler_ids: Vec::<SignalHandlerId>
}

pub struct WorkspacesConfig {}

impl Workspaces {
    fn generate_buttons(&self, container: &gtk::Box) -> (Vec::<gtk::CheckButton>, Vec::<SignalHandlerId>) {
        let mut buttons = vec![];
        let mut signal_handler_ids = vec![];

        // Because if there's only one button it won't show as a radio button
        let hidden_radio_button = gtk::CheckButton::new();
        hidden_radio_button.set_visible(false);
        container.append(&hidden_radio_button);

        for workspace in &self.workspaces {
            let workspace  = workspace.clone();

            let radio_button = gtk::CheckButton::new();
            if workspace == self.active_workspace {
                radio_button.set_active(true);
            }
            radio_button.set_group(Some(&hidden_radio_button));

            let signal_handler_id = radio_button.connect_toggled(clone!(@strong workspace => move |btn| {
                if btn.is_active() {
                    Compositor::set_active_workspace(workspace);
                }
            }));

            container.append(&radio_button);
            buttons.push(radio_button);
            signal_handler_ids.push(signal_handler_id);
        }

        (buttons, signal_handler_ids)
    }

}

impl SimpleComponent for Workspaces {
    type Input = WorkspacesInput;
    type Output = ();
    type Init = WorkspacesConfig;
    type Root = gtk::Box;
    type Widgets = WorkspacesWidgets;

    fn init_root() -> Self::Root {
        let root_box = gtk::Box::new(gtk::Orientation::Horizontal, 5);
        root_box.set_css_classes(&["workspaces"]);
        return root_box;
    }

    /// Initialize the UI and model.
    fn init(
        _config: Self::Init,
        root_box: &Self::Root,
        _sender: ComponentSender<Self>,
    ) -> relm4::ComponentParts<Self> {
        let model = Workspaces {
            workspaces: Compositor::get_workspaces(),
            active_workspace: Compositor::get_active_workspace(),
            tracker: 0
        };
            
        let buttons_container = gtk::Box::new(gtk::Orientation::Horizontal, 5);

        let (radio_buttons, signal_handler_ids) = model.generate_buttons(&buttons_container);

        
        root_box.append(&buttons_container);

        let widgets = WorkspacesWidgets { buttons_container, radio_buttons, signal_handler_ids };

        ComponentParts { model, widgets }
    }

    /// Update model based on message
    fn update(&mut self, message: Self::Input, _sender: ComponentSender<Self>) {
        self.reset(); 
        match message {
            WorkspacesInput::CompositorOutput(output) => {
                match output {
                    CompositorOutput::ActiveWorkspace(active_workspace) => {
                        self.set_active_workspace(active_workspace);
                    }
                    CompositorOutput::CreateWorkspace(workspace) => {
                        let workspaces = self.get_workspaces();
                        let mut workspaces = workspaces.to_owned();
                        workspaces.push(workspace);
                        workspaces.sort();
                        self.set_workspaces(workspaces);
                    }
                    CompositorOutput::DestroyWorkspace(workspace) => {
                        let workspaces = self.get_workspaces();
                        let mut workspaces = workspaces.to_owned();

                        let index = self.workspaces.iter().position(|&w| {w == workspace});
                        if let Some(index) = index {
                            workspaces.remove(index);
                            self.set_workspaces(workspaces);
                        }

                    }
                    _ => {}
                }
            }
        }
    }

    /// Update the view to represent the updated model.
    fn update_view(&self, widgets: &mut Self::Widgets, _sender: ComponentSender<Self>) {
        if self.changed(Workspaces::active_workspace()) {
            let index = self.workspaces.iter().position(|&w| {w == self.active_workspace});
            if let Some(index) = index {
                let signal_handler_id = &widgets.signal_handler_ids[index];
                let radio_button = &widgets.radio_buttons[index];
                radio_button.block_signal(signal_handler_id);
                radio_button.set_active(true);
                radio_button.unblock_signal(signal_handler_id);
            }
        }

        if self.changed(Workspaces::workspaces()) {
            widgets.buttons_container.remove_all();
            (widgets.radio_buttons, widgets.signal_handler_ids) = self.generate_buttons(&widgets.buttons_container);
        }
    }
}
