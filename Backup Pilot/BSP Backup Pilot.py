import os
import shutil
from datetime import datetime
import zipfile
import PySimpleGUI as sg
import configparser

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
    [sg.Output(size=(60, 10), key='-OUTPUT-')],
    [sg.Button('Backup Now'), sg.Button('Exit')]
]

# Create the window
window = sg.Window('Backup Program', layout)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Backup Now':
        backup_location = values['-FOLDER-']
        zip_backup = values['-ZIP-']
        
        # Update config file
        config['DEFAULT']['backup_location'] = backup_location
        config['DEFAULT']['zip_backup'] = str(zip_backup)
        with open(CONFIG_FILE, 'w') as configfile:
            config.write(configfile)
        
        # Perform backup
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
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

# Close the window
window.close()
