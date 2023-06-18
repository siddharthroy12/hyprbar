pub mod workspaces;

#[derive(Debug)]
pub enum Module {
    Workspaces(workspaces::Workspaces)
}
