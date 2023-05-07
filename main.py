import os
import subprocess
import psutil
import json
import time
import datetime
import winshell
import win32api
import atexit
import ctypes
from rich.console import Console


# Run this to COMPILE:
# pyinstaller --name=SteamGAU --noconfirm --onefile --icon=app_icon.ico --console main.py

console = Console()
ctypes.windll.kernel32.SetConsoleTitleW("SteamCMD Games Auto-Updater")

def close_window(count_seconds):
    # Loop for the specified number of seconds
    for i in range(count_seconds, 0, -1):
        # Print the time remaining on the same line using '\r'
        print(f"This window will close in {i} seconds...", end='\r')
        # Wait for one second using the time.sleep method
        time.sleep(1)
    exit()


def check_if_already_running(process_name):
    # Count the number of instances of the process running
    count = 0
    for proc in psutil.process_iter(['name']):
        if proc.name() == process_name:
            count += 1
    return count


def create_shortcut():
    # Get the path of the running app
    shortcut_name = "SteamGAU.exe"
    app_path = os.path.abspath(os.getcwd())
    app_path = os.path.join(app_path, shortcut_name)

    # Create a shortcut name and path
    shortcut_path = os.path.join(winshell.startup(), f"{shortcut_name}.lnk")
    if not os.path.exists(shortcut_path):
        # Create the shortcut
        with winshell.shortcut(shortcut_path) as shortcut:
            shortcut.path = app_path
            shortcut.description = "Shortcut for SteamGAI"
            # shortcut.icon_location = "path/to/icon.ico"
        console.log(f"Shortcut created for '{shortcut_name}' at '{shortcut_path}'")
    else:
        console.log("Startup shortcut already exists.")


def create_steamcmd_json():
    # Check if the file exists
    if not os.path.exists("steamcmd.json"):
        console.log("steamcmd.json missing.")
        # Create a dictionary to write to the file
        config = {
            "logon": "anonymous",
            "install_dir": "put_your_install_dir_here",
            "app_id": "740"
        }
        # Write the dictionary to the file as JSON
        with open("steamcmd.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        console.log("steamcmd.json created.")
    else:
        console.log("steamcmd.json exists.")

    return True


def create_servers_json():
    # Check if the file exists
    if not os.path.exists("servers.json"):
        console.log("servers.json missing.")
        # Create a dictionary to write to the file
        configs = [
            {
                "name": "Server Name Goes Here",
                "server_dir": "D:\\example\\folder",
                "launch_parameters": "-game csgo -console -usercon -maxplayers_override 16 -tickrate 128 +game_type 0 +game_mode 1 +mapgroup mg_active +map de_mirage +ip 192.168.0.214 +net_pub",
                "set_steam_account": "<CODE-GOES-HERE>",
                "port": "27015"
            },
            {
                "name": "Server Name Goes Here",
                "server_dir": "D:\\example\\folder",
                "launch_parameters": "-game csgo -console -usercon -maxplayers_override 16 -tickrate 128 +game_type 0 +game_mode 1 +mapgroup mg_active +map de_mirage +ip 192.168.0.214 +net_pub",
                "set_steam_account": "<CODE-GOES-HERE>",
                "port": "27016"
            }
        ]
        # Write the dictionary to the file as JSON
        with open("servers.json", "w", encoding="utf-8") as f:
            json.dump(configs, f, indent=4)
        console.log("servers.json created.")
    else:
        console.log("servers.json exists.")

    return True


def convert_path(path):
    path = path.replace('/', '\\')
    return path


def kill_srcds():
    process_name = "srcds.exe"
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            # Kill the process and all iterations of it
            # os.kill(proc.pid, 9)
            console.log(f"Killing {process_name} process...")
            os.system(f"taskkill /im {process_name} /f")


def start_update():
    # Convert JSON string to Python variable
    with open('steamcmd.json', 'r') as steamcmd:
        steamcmd_config = json.load(steamcmd)
    with open('servers.json', 'r') as servers:
        servers_list = json.load(servers)

    for server in servers_list:
        if server["name"].lower() == "server name goes here":
            console.log("None servers added. Please open up server.json file and add your servers.")
            close_window(30)
            exit()
        elif steamcmd_config["install_dir"].lower() == "put_your_install_dir_here":
            console.log("You didn't changed the SteamCMD install_dir. Please open up steamcmd.json file and add your servers.")
            close_window(30)
            exit()
        else:
            console.log("Checking for updates...")

            # Run script to update game files with STEAMCMD
            steamcmd_path = os.path.join(convert_path(steamcmd_config["install_dir"]), "srcds.exe")
            console.log(f'Updating {server["name"]} server...')
            p = subprocess.Popen(['start', 'cmd', '/c', steamcmd_path + ' +logon '+steamcmd_config["logon"]+' +force_install_dir ' + convert_path(server["server_dir"]) + ' +app_update '+steamcmd_config["app_id"]+' +quit'],shell=True)
            # wait for the process to complete and close the cmd window
            p.communicate()
            p.terminate()

            # Run script to start srcds.exe
            srcds_path = os.path.join(convert_path(server["server_dir"]), "srcds.exe")
            console.log(f'Starting {server["name"]} server...')
            r = subprocess.Popen(['start', 'cmd', '/c', srcds_path + ' ' + server["launch_parameters"] + ' +sv_setsteamaccount ' + server["set_steam_account"] + ' -port ' + server["port"]],shell=True)
            # wait for the process to complete and close the cmd window
            r.communicate()
            r.terminate()


def kick_starter():
    # Set the time to countdown to
    countdown_time = datetime.time(hour=4)

    # Check if shortcut exists, if not, create
    create_shortcut()

    # Loop until the countdown time is reached
    while True:
        # Get the current time
        now = datetime.datetime.now().time()

        # Check if an instance is already working, if not, create one
        if check_if_already_running("SteamGAU.exe") > 2:
            console.log("There is already one instance of SteamGAU.exe running.")
            close_window(10)

        if check_if_already_running("srcds.exe") == 0:
            start_update()

        # Print the current time
        print(f"Currently it's [{now.strftime('%H:%M')}h] -> Next Update Check [04:00h].", end='\r')

        # Check if it's time to stop counting down
        if str(now.strftime('%H:%M')) == str(countdown_time.strftime('%H:%M')):
            create_steamcmd_json()
            create_servers_json()
            if not os.path.exists("steamcmd.json") and not os.path.exists("servers.json"):
                console.log("Config files do not exists for some reason.")
            else:
                start_update()

        # Wait second
        time.sleep(60)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Kill SRCDS windows when app closes
    atexit.register(kill_srcds)
    while True:
        kick_starter()
