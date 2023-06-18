use std::process::Command;

pub fn execute_command(command: &str) -> String {
    let mut parts = command.split_whitespace();
    let command = parts.next().expect("No command provided");
    let args = parts.collect::<Vec<_>>();

    match Command::new(command).args(args).output() {
        Ok(output) => {
            if output.status.success() {
                String::from_utf8_lossy(&output.stdout).to_string()
            } else {
                String::from_utf8_lossy(&output.stderr).to_string()
            }
        }
        Err(err) => {
            eprintln!("Failed to execute \"{command}\": {err}");
            String::new()
        }
    }
}
