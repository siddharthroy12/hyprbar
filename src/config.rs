#[derive(Debug, Clone)]
pub struct BarMargin {
    pub top: i32,
    pub bottom: i32,
    pub left: i32,
    pub right: i32,
}

#[derive(Eq, PartialEq, Debug, Clone)]
pub enum BarPosition {
    Top,
    Left,
    Right,
    Bottom,
}

#[derive(Debug, Clone)]
pub enum ModuleName {
    Workspaces,
    AppTitle,
    Calendar,
}

#[derive(Debug, Clone)]
pub struct BarSettings {
    pub border_radius: i32,
    pub height: i32,
    pub margin: BarMargin,
    pub position: BarPosition,
}

#[derive(Debug, Clone)]
pub struct Modules {
    pub start_modules: Vec<ModuleName>,
    pub center_modules: Vec<ModuleName>,
    pub end_modules: Vec<ModuleName>,
}

#[derive(Debug, Clone)]
pub struct Config {
    pub bar: BarSettings,
    pub modules: Modules,
}

impl Default for Config {
    fn default() -> Self {
        Config {
            bar: BarSettings {
                border_radius: 100,
                height: 40,
                margin: BarMargin {
                    top: 5,
                    bottom: 0,
                    left: 5,
                    right: 5,
                },
                position: BarPosition::Top,
            },
            modules: Modules {
                start_modules: vec![ModuleName::Workspaces, ModuleName::AppTitle],
                center_modules: vec![ModuleName::Calendar],
                end_modules: vec![],
            },
        }
    }
}
