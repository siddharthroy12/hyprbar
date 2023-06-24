use relm4::RelmApp;
use hyprbar::bar::Bar;
use hyprbar::config::Config;

fn main() {
    let app = RelmApp::new("relm4.test.simple_manual");
    app.run::<Bar>(Config::default());
}
