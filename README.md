# A status bar for Hyprland

# Run, Build, Install

```sh
# Clone the repo
git clone https://github.com/siddharthroy12/hyprbar.git
cd hyprbar

# Setup virtural environment
python -m venv .env
source .env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run hyprbar
python -m hyprbar

# Installing for user (outside virtual environment)
deactivate # If virtual environment is activated
pip install -r requirements.txt # If dependencies are not installed
python setup.py install --user
```
