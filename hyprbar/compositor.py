# This file contains functions to interact with compositor
import json
import os
import socket
from hyprbar.common import run_command
from hyprbar.common import Message

# Track if selection layer was just closed
selection_was_closed = False


# Get active window title
def get_active_window_title():
    return json.loads(run_command("hyprctl activewindow -j"))["title"]


# Get workspaces
def get_workspaces():
    workspace_list = json.loads(run_command("hyprctl workspaces -j"))
    return [entry["id"] for entry in workspace_list]


# Get active worksapce
def get_active_workspace():
    return json.loads(run_command("hyprctl activeworkspace -j"))["id"]


def set_active_workspace(workspace):
    return run_command(f"hyprctl dispatch workspace {workspace}")


# Messages for compositor properties
active_window_title = Message(get_active_window_title())
workspaces = Message(get_workspaces())
active_workspace = Message(get_active_workspace())


# Connect to hyprlaond socket to get info like changing window and workspace
# https://wiki.hyprland.org/IPC/
def connect_to_hyprland_socket():
    # Hyprland Instance Signature (HIS)
    his = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")

    # Create a socket object
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Connect to the socket file
    sock.connect(f"/tmp/hypr/{his}/.socket2.sock")

    return sock


def read_hyprland_socket(sock):
    global selection_was_closed
    try:
        data = sock.recv(1024)  # Got this number from ChatGPT
        if data:
            data = data.decode()
            for line in data.split("\n"):
                if line != "":
                    if line.startswith("activewindow>>"):
                        if not selection_was_closed:
                            active_window_title.set_value(
                                line[14:].split(",")[0])
                    if line.startswith("workspace>>"):
                        active_workspace.set_value(int(line[11:]))
                    if line.startswith("createworkspace>>"):
                        new_list = workspaces.get_value()
                        new_list.append(int(line[17:]))
                        new_list.sort()
                        workspaces.set_value(new_list)
                    if line.startswith("destroyworkspace>>"):
                        new_list = workspaces.get_value()
                        new_list.remove(int(line[18:]))
                        new_list.sort()
                        workspaces.set_value(new_list)
                    # To fix the empty app title during screenshot
                    # using hyprshot. Do not update app title
                    # when the selection has just stopped
                    if line == "closelayer>>selection":
                        selection_was_closed = True
                    else:
                        selection_was_closed = False

    except socket.error as e:
        print("Socket error:", e)
