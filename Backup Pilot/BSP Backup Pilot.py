import os
import shutil
from datetime import datetime
import zipfile
import PySimpleGUI as sg
import configparser
import threading
import time

# Configuration file path
CONFIG_FILE = 'config.ini'

# Create a default config file if it doesn't exist
if not os.path.exists(CONFIG_FILE):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'backup_location': '', 'zip_backup': 'False'}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

# Load config file
config = configparser.ConfigParser()
config.read(CONFIG_FILE)
backup_location = config['DEFAULT']['backup_location']
zip_backup = config['DEFAULT'].getboolean('zip_backup')

# Set the theme to DarkAmber
sg.theme('DarkAmber')

# GUI layout
layout = [
    [sg.Text('Backup Location'), sg.InputText(default_text=backup_location, key='-FOLDER-'), sg.FolderBrowse(target='-FOLDER-')],
    [sg.Checkbox('Store backup as a zip file', default=zip_backup, key='-ZIP-')],
    [sg.Text("Set timer in minutes:"), sg.Input(key="-MINUTES-", size=(10, 1))],
    [sg.Button("Start"), sg.Button("Stop")],
    [sg.Text("Timer: ", key="-TIMER-")],
    [sg.Output(size=(60, 10), key='-OUTPUT-')],
    [sg.Text("Version: Hydrogen 2")],
    [sg.Button('Exit')]
]

# Create the window
window = sg.Window('Backup Program', layout)

# Event loop
active = [False]

def start_timer(minutes, active, window):
    while active[0]:
        seconds = minutes * 60
        while seconds > 0:
            if not active[0]:
                return
            window.write_event_value('-UPDATE-', f"{seconds // 60}:{seconds % 60:02}")
            time.sleep(1)
            seconds -= 1
        window.write_event_value('-UPDATE-', "Making the backup!")
        perform_backup()
        time.sleep(1)  # Wait for 1 second before starting the timer again

def perform_backup():
    backup_location = window['-FOLDER-'].get()
    zip_backup = window['-ZIP-'].get()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    try:
        if zip_backup:
            # Create a zip file
            zip_filename = os.path.join(backup_location, f'backup_{timestamp}.zip')
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
                for root, dirs, files in os.walk('.'):
                    for file in files:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path)
                        backup_zip.write(file_path, arcname=rel_path)
            print(f'Backup created successfully as a zip file at: {zip_filename}')
        else:
            backup_folder = os.path.join(backup_location, f'backup_{timestamp}')
            shutil.copytree('.', backup_folder)
            print(f'Backup created successfully at: {backup_folder}')
    except Exception as e:
        print(f'Error occurred during backup: {e}')

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Start':
        if not active[0]:
            try:
                minutes = int(values["-MINUTES-"])
                if minutes > 0:
                    active[0] = True
                    timer_thread = threading.Thread(target=start_timer, args=(minutes, active, window))
                    timer_thread.daemon = True
                    timer_thread.start()
                else:
                    sg.popup("Please enter a valid number of minutes.")
            except ValueError:
                sg.popup("Please enter a valid number of minutes.")
    elif event == 'Stop':
        if active[0]:
            active[0] = False
            window['-TIMER-'].update('')
            time.sleep(1)  # Wait for the timer thread to complete
            continue
    elif event == 'Backup Now':
        perform_backup()

    if event == "-UPDATE-":
        window['-TIMER-'].update(values[event])

# Close the window
window.close()
