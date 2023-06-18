// This file contains a worker to read hyprland socket and send signals
use relm4::{ComponentSender, Worker};
use std::env;
use std::io::{BufRead, BufReader};
use std::os::unix::net::UnixStream;
use crate::common::execute_command;
use serde_json::Value;

#[derive(Debug, Clone)]
pub enum CompositorOutput {
    ActiveWorkspace(i32),
    ActiveWindow(String),
    CreateWorkspace(i32),
    DestroyWorkspace(i32),
}

#[derive(Debug, Clone, Copy)]
pub enum CompositorInput {
    StartListening,
}

pub struct Compositor;

impl Compositor {
    pub fn get_active_window_title() -> String {
        let json = execute_command("hyprctl activewindow -j");

        if let Ok(parsed) = serde_json::from_str::<Value>(&json) {
            return parsed["title"].to_string()
        } else {
            return String::new()
        }
    }

    pub fn get_workspaces() -> Vec<i32> {
        let json = execute_command("hyprctl workspaces -j");
        let mut result = vec![];

        if let Ok(parsed) = serde_json::from_str::<Value>(&json) {
            if parsed.is_array() {
                for workspace in parsed.as_array().unwrap() {
                    if let Some(id) = workspace.get("id") {
                        if let Some(id) = id.as_i64() {
                            if let Ok(id) = id.try_into() {
                                result.push(id);
                            }
                        }
                    }
                }

            }
        }

        result.sort();

        return result;
    }

    pub fn get_active_workspace() -> i32 {
        let json = execute_command("hyprctl activeworkspace -j");

        if let Ok(parsed) = serde_json::from_str::<Value>(&json) {
            return parsed["id"].as_i64().unwrap_or(0).try_into().unwrap_or(0);
        } else {
            return 0
        }
    }

    pub fn set_active_workspace(workspace: i32) {
        let _ = execute_command(&format!("hyprctl dispatch workspace {workspace}"));
    }
}

impl Worker for Compositor {
    type Init = ();
    type Input = CompositorInput;
    type Output = CompositorOutput;

    fn init(_init: Self::Init, _sender: ComponentSender<Self>) -> Self {
        Self
    }

    fn update(&mut self, msg: CompositorInput, sender: ComponentSender<Self>) {
        match msg {
            CompositorInput::StartListening => {
                // Get Hyprland Instance Signature
                match env::var("HYPRLAND_INSTANCE_SIGNATURE") {
                    Ok(value) => {
                        let socket_path = format!("/tmp/hypr/{value}/.socket2.sock");
                        // Connect to Hyprland socket
                        match UnixStream::connect(socket_path) {
                            Ok(stream) => {
                                // Read each line from socket
                                let reader = BufReader::new(stream);
                                for line in reader.lines() {
                                    let line = line.unwrap_or(String::from(""));
                                    let line = line.replace("\n", "");
                                    let line = line.trim();
                                    let split: Vec<&str> = line.splitn(2, ">>").collect();

                                    // Parse the line and convert it to relavant CompositorOutput
                                    if split.len() > 1 {
                                        let output = match split.as_slice() {
                                            // TODO: This signal needs to be delayed by few
                                            // miliseconds when workspace is changed from a empty
                                            // one to another empty one to fix the glitch
                                            ["workspace", num] => num
                                                .parse()
                                                .ok()
                                                .map(CompositorOutput::ActiveWorkspace),
                                            ["activewindow", value] => Some(
                                                CompositorOutput::ActiveWindow(value.to_string()),
                                            ),
                                            ["createworkspace", num] => num
                                                .parse()
                                                .ok()
                                                .map(CompositorOutput::CreateWorkspace),
                                            ["destroyworkspace", num] => num
                                                .parse()
                                                .ok()
                                                .map(CompositorOutput::DestroyWorkspace),
                                            _ => None,
                                        };

                                        if let Some(output) = output {
                                            let _ = sender.output(output);
                                        }
                                    }
                                }
                            }
                            Err(_) => {
                                eprintln!("Failed to connect to Hyprland socket")
                            }
                        }
                    }
                    Err(_) => {
                        eprintln!("Failed to get Hyprland instance signaure.");
                    }
                }
            }
        }
    }
}
