use relm4::RelmApp;
use rust_playground::bar::Bar;
use rust_playground::config::Config;

fn main() {
    let app = RelmApp::new("relm4.test.simple_manual");
    app.run::<Bar>(Config::default());
}
