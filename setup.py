import os
from setuptools import setup, find_packages


# Utility function to read the README file.
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="hyprbar",
    version="0.0.1",
    author="Siddharth Roy",
    author_email="siddharthroy36912@gmail.com",
    description="A status bar for Hyprland",
    license="BSD",
    keywords="statusbar hyprland wayland gtk libadwaita gtk-layer-shell",
    url="https://github.com/siddharthroy12/hyprbar",
    entry_points={
        'console_scripts': [
            'hyprbar = hyprbar:main',
        ],
    },
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Desktop Environment :: Window Managers :: Status bar",
        "License :: OSI Approved :: BSD License",
    ],
)
