import os
import shutil
import time
import asyncio
import PySimpleGUI as sg
import configparser

CONFIG_FILE = "config.ini"

async def main():
    # Load backup settings from the config file
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    backup_folder = config.get("BACKUP", "BackupFolder", fallback="")
    backup_location = config.get("BACKUP", "BackupLocation", fallback="")
    backup_interval = config.getint("BACKUP", "BackupInterval", fallback=3600)
    autostart_enabled = config.getboolean("BACKUP", "AutostartEnabled", fallback=False)

    # Define the window's contents
    layout = [[sg.Text("Backup Folder")],
              [sg.Input(default_text=backup_folder), sg.FolderBrowse()],
              [sg.Text("Backup Location")],
              [sg.Input(default_text=backup_location), sg.FolderBrowse()],
              [sg.Text("Backup Interval (in seconds)")],
              [sg.InputText(default_text=str(backup_interval))],
              [sg.Checkbox("Autostart", default=autostart_enabled, key="autostart")],
              [sg.Output(size=(60, 10))],
              [sg.Button("Start Backup"), sg.Button("Backup Now"), sg.Button("Exit")]]
    # Create the window
    window = sg.Window("Folder Backup", layout, enable_close_attempted_event=True)

    # Event loop for the GUI
    while True:
        event, values = window.read(timeout=10)

        if event == "Exit" or event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
            break
        elif event == "Backup Now":
            await backup_folder(values[0], values[1])
        elif event == "Start Backup":
            try:
                print("Starting timer process")
                interval = int(values[2])
                asyncio.create_task(run_backup_interval(values[0], values[1], interval))
            except ValueError:
                print("Invalid interval value")

        await asyncio.sleep(0)  # Allow other tasks to run

    window.close()

    # Save backup settings to the config file
    config["BACKUP"] = {
        "BackupFolder": values[0],
        "BackupLocation": values[1],
        "BackupInterval": values[2],
        "AutostartEnabled": str(values["autostart"])
    }
    with open(CONFIG_FILE, "w") as config_file:
        config.write(config_file)

    # Start backup loop if autostart is enabled
    if values["autostart"]:
        asyncio.create_task(run_backup_interval(values[0], values[1], int(values[2])))

async def run_backup_interval(src_folder, dst_folder, interval):
    while True:
        await backup_folder(src_folder, dst_folder)
        await asyncio.sleep(interval)

async def backup_folder(src_folder, dst_folder):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    zip_filename = os.path.join(dst_folder, f"backup_{timestamp}.zip")
    print(f"Backing up {src_folder} to {zip_filename}")
    await asyncio.to_thread(shutil.make_archive, zip_filename[:-4], "zip", src_folder)

if __name__ == "__main__":
    asyncio.run(main())
