# This file contains Messages related to system
# infomations, like battery, cpu, ram, network, etc

from hyprbar.common import Message
import psutil
from gi.repository import GLib


# Battery
battery = Message({
    "present": psutil.sensors_battery() is not None,
    "percent": 0,
    "charging": False
})
# CPU

# RAM

# Network

# Bluetooth

# Update all status


def update_status():
    if battery.get_value()["present"]:
        value = {**battery.get_value()}
        value["percent"] = int(psutil.sensors_battery().percent)
        value["charging"] = psutil.sensors_battery().power_plugged
        battery.set_value(value)
    GLib.timeout_add(1000, update_status)


update_status()
