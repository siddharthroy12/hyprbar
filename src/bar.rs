use crate::compositor::{Compositor, CompositorInput, CompositorOutput};
use crate::config::BarPosition;
use crate::modules::app_title::{AppTitle, AppTitleInput};
use crate::modules::workspaces::{Workspaces, WorkspacesConfig, WorkspacesInput};
use relm4::adw::prelude::*;
use relm4::prelude::*;
use relm4::{
    adw, gtk, set_global_css, ComponentParts, ComponentSender, Controller, SimpleComponent,
    WorkerController,
};

use super::config::*;

pub struct Bar {
    config: Config,
    controllers: Vec<ModuleController>,
}

#[derive(Debug)]
pub enum BarInput {
    ChangePosition(BarPosition),
    ChangeMargin(BarMargin),
    ChangeBorderRadius(i32),
    CompositorOutput(CompositorOutput),
}

enum ModuleController {
    WorkspacesController(Controller<Workspaces>),
    AppTitleContoller(Controller<AppTitle>),
}

pub struct BarWidgets {}

impl Bar {
    fn module_controller_from_name(
        name: ModuleName,
        _sender: &ComponentSender<Self>,
    ) -> (ModuleController, impl IsA<gtk::Widget>) {
        match name {
            ModuleName::Workspaces => {
                let controller = Workspaces::builder().launch(WorkspacesConfig {}).detach();
                let widget = controller.widget().to_owned();
                (ModuleController::WorkspacesController(controller), widget)
            }
            ModuleName::AppTitle => {
                let controller = AppTitle::builder().launch(()).detach();
                let widget = controller.widget().to_owned();
                (ModuleController::AppTitleContoller(controller), widget)
            }
        }
    }

    fn wrap_module<T: IsA<gtk::Widget>>(widget: &T) -> gtk::Box {
        let wrap = gtk::Box::new(gtk::Orientation::Horizontal, 0);
        wrap.append(widget);
        wrap.set_css_classes(&["module"]);
        wrap
    }

    fn set_style(&self) {
        let bar_border_radius = 50;
        let module_border_radius = 50;

        let css = format!(
            "
        window.background {{
            border-radius: {}px;
            background: @headerbar_bg_color;
        }}
        .module {{
            background: @window_bg_color;
            margin: 5px;
            border-radius: {}px;
        }}
        .workspaces {{
            padding: 0 8px;
        }}
        .app-title {{
            padding: 0 10px;
        }}

        checkbutton radio {{
            min-width: 8px;
            min-height: 8px;
            -gtk-icon-size: 8px;
            padding: 0;
            box-shadow: 0 0 0 2px @window_fg_color;
        }}
        checkbutton:checked radio {{
            color: @window_fg_color;
        }}

        calendar {{
            background: rgba(0, 0, 0, 0.2);
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
        ",
            bar_border_radius, module_border_radius
        );
        set_global_css(&css);
    }
}

impl SimpleComponent for Bar {
    type Input = BarInput;
    type Output = ();
    type Init = Config;
    type Root = adw::ApplicationWindow;
    type Widgets = BarWidgets;

    fn init_root() -> Self::Root {
        let window = adw::ApplicationWindow::builder()
            .title("Simple app")
            .default_width(300)
            .default_height(100)
            .build();

        // Before the window is first realized, set it up to be a layer surface
        gtk4_layer_shell::init_for_window(&window);

        // Display above normal windows
        gtk4_layer_shell::set_layer(&window, gtk4_layer_shell::Layer::Overlay);

        // Push other windows out of the way
        gtk4_layer_shell::auto_exclusive_zone_enable(&window);

        return window;
    }

    /// Initialize the UI and model.
    fn init(
        config: Self::Init,
        window: &Self::Root,
        sender: ComponentSender<Self>,
    ) -> relm4::ComponentParts<Self> {
        let mut model = Bar {
            config,
            controllers: vec![],
        };

        model.set_style();

        // Set height
        window.set_default_height(model.config.bar.height);

        // Set position
        // Anchors are if the window is pinned to each edge of the output
        let anchors = [
            (
                gtk4_layer_shell::Edge::Left,
                model.config.bar.position != BarPosition::Right,
            ),
            (
                gtk4_layer_shell::Edge::Right,
                model.config.bar.position != BarPosition::Left,
            ),
            (
                gtk4_layer_shell::Edge::Top,
                model.config.bar.position != BarPosition::Bottom,
            ),
            (
                gtk4_layer_shell::Edge::Bottom,
                model.config.bar.position != BarPosition::Top,
            ),
        ];

        for (anchor, state) in anchors {
            gtk4_layer_shell::set_anchor(window, anchor, state);
        }

        // Set Margin
        gtk4_layer_shell::set_margin(
            window,
            gtk4_layer_shell::Edge::Left,
            model.config.bar.margin.left,
        );
        gtk4_layer_shell::set_margin(
            window,
            gtk4_layer_shell::Edge::Right,
            model.config.bar.margin.right,
        );
        gtk4_layer_shell::set_margin(
            window,
            gtk4_layer_shell::Edge::Top,
            model.config.bar.margin.top,
        );
        gtk4_layer_shell::set_margin(
            window,
            gtk4_layer_shell::Edge::Bottom,
            model.config.bar.margin.bottom,
        );

        let center_box = gtk::CenterBox::new();

        let compositor: WorkerController<Compositor> = Compositor::builder()
            .detach_worker(())
            .forward(sender.input_sender(), |msg| BarInput::CompositorOutput(msg));

        // Start listening to Hyprland compositor's socket in different thread
        let _ = compositor.sender().send(CompositorInput::StartListening);

        let start_box = gtk::Box::new(gtk::Orientation::Horizontal, 2);
        for module_name in &model.config.modules.start_modules {
            let (controller, widget) =
                Bar::module_controller_from_name(module_name.to_owned(), &sender);
            model.controllers.push(controller);

            start_box.append(&Bar::wrap_module(&widget))
        }
        center_box.set_start_widget(Some(&start_box));

        window.set_content(Some(&center_box));

        let widgets = BarWidgets {};

        ComponentParts { model, widgets }
    }

    /// Update model based on message
    fn update(&mut self, message: Self::Input, _sender: ComponentSender<Self>) {
        match message {
            BarInput::CompositorOutput(output) => {
                for controller in &self.controllers {
                    match controller {
                        ModuleController::WorkspacesController(controller) => {
                            let _ = controller
                                .sender()
                                .send(WorkspacesInput::CompositorOutput(output.to_owned()));
                        }
                        ModuleController::AppTitleContoller(controller) => {
                            let _ = controller
                                .sender()
                                .send(AppTitleInput::CompositorOutput(output.to_owned()));
                        }
                    }
                }
            }
            _ => {}
        }
    }

    /// Update the view to represent the updated model.
    fn update_view(&self, _widgets: &mut Self::Widgets, _sender: ComponentSender<Self>) {}
}
