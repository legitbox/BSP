import subprocess
import threading
import PySimpleGUI as sg
import re
import time
import os
import configparser
import json
import shutil
import http.server

import addon_manager
import settings

current_dir = os.getcwd()

parent_dir = os.path.dirname(current_dir)

server_dir = os.path.join(parent_dir, "bedrock_server.exe")

properties_dir = os.path.join(parent_dir, "server.properties")

permissions_dir = os.path.join(parent_dir, "permissions.json")

process = None

config_file = 'config.ini'


# check if config file exists
if not os.path.exists(config_file):
    # create new config file with default values
    config = configparser.ConfigParser()
    config['SERVER'] = {'RestartInterval': '6', 'Restartenabled': '0'}
    with open(config_file, 'w') as f:
        config.write(f)

# read config file
config = configparser.ConfigParser()
config.read(config_file)


lock = threading.Lock()

player_list = []

player_count = 0

restart_interval = config['SERVER'].get('RestartInterval', '6 hr')

stop_flag = False  # global flag variable to signal the loop to stop

# regex pattern to match player join event
JOIN_PATTERN = re.compile(r"Player connected: ([^\s]+), xuid: (\d+)")

# regex pattern to match player leave event
LEAVE_PATTERN = re.compile(r"Player disconnected: ([^\s]+), xuid: (\d+)")

# load permissions from file
with open(permissions_dir) as f:
    permissions = json.load(f)

def run_server_exe():
    global process
    global player_list
    global player_count
    global latest_message

    with lock:
        if process is None:
            process = subprocess.Popen([server_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True, shell=True)

    output = ""
    while True:
        line = process.stdout.readline()
        
        if line == '' and process.poll() is not None:
            with lock:
                process = None
            break

        if line:
            line = re.sub(r'\033\[\d{1,2}m', '', line)
            #if 'Scripting' not in line:
            output += line
            window['output'].update(output.strip())

            match = JOIN_PATTERN.search(line)
            if match:
                player_name = match.group(1)
                xuid = match.group(2)
                with open(permissions_dir) as f:
                    permissions = json.load(f)
                level = None
                for permission in permissions:
                    if permission['xuid'] == xuid:
                        level = permission['permission'].capitalize()
                        break
                player_list.append([player_name, xuid, level])
                window['player_list'].update(values=player_list)
                player_count += 1
                window['-ONLINE_PLAYERS-'].update(player_count)

            match = LEAVE_PATTERN.search(line)
            if match:
                player_name = match.group(1)
                player_list = [p for p in player_list if p[0] != player_name]
                window['player_list'].update(values=player_list)
                player_count -= 1
                window['-ONLINE_PLAYERS-'].update(player_count)

            if 'Scripting' in line:
                match = re.search(r'\[Scripting\] \[([^\]]+)\]', line)
                if match:
                    sender_name = match.group(1)
                    message_match = re.search(r'\[([^\]]+)\]$', line)
                    if message_match:
                        message = message_match.group(1)
                        formatted_message = f"<{sender_name}> {message}"
                        save_message_to_file(formatted_message)
                        message_list.append(formatted_message)
                        window["ingame_chat"].update(values=message_list)


        if 'Starting Server' in line:
            window['-SERVER_STATE-'].update('Starting')
        elif 'Server started.' in line:
            window['-SERVER_STATE-'].update('Running')
        elif 'Server stop requested.' in line:
            window['-SERVER_STATE-'].update('Stopping')
        elif 'Quit correctly' in line:
            window['-SERVER_STATE-'].update('Stopped')
        elif "Fail" in line or "Error" in line or "error" in line or "fail" in line or "exit" in line or "Exit" in line or "ERROR" in line:
            window['-SERVER_STATE-'].update('Error')




def start_server():
    window.Element('output').Update('')
    thread = threading.Thread(target=run_server_exe, daemon=True)
    thread.start()

def restart_server():
    print("Inactive")

def stop_server():
    command = ("stop")
    process.stdin.write(command + "\n")
    process.stdin.flush()

def run_command(values):
    command = values['input']
    process.stdin.write(command + "\n")
    process.stdin.flush()

def update_permissions_thread():
    time.sleep(1)
    row_number = values['player_list'][0]
    xuid = player_list[row_number][1]
    # Update the player level
    with open(permissions_dir) as f:
        permissions = json.load(f)       
    level = None
    for permission in permissions:
        if permission['xuid'] == xuid:
            level = permission['permission'].capitalize()
            break
    player_list[row_number][2] = level
    window['player_list'].update(values=player_list)  # update player list with list of dictionaries

def update_permissions():
    t = threading.Thread(target=update_permissions_thread)
    t.start()

def op_player():
    if values['player_list']:
        row_number = values['player_list'][0]
        player_name = player_list[row_number][0]
        if player_name:
            command = f"op {player_name}"
            #print(command)
            process.stdin.write(command + "\n")
            process.stdin.flush()
            update_permissions()

def deop_player():
    if values['player_list']:
        row_number = values['player_list'][0]
        player_name = player_list[row_number][0]
        if player_name:
            command = f"deop {player_name}"
            #print(command)
            process.stdin.write(command + "\n")
            process.stdin.flush()
            update_permissions()

def kick_player():
    if values['player_list']:
        row_number = values['player_list'][0]
        player_name = player_list[row_number][0]
        if player_name:
            command = f"kick {player_name}"
            #print(command)
            process.stdin.write(command + "\n")
            process.stdin.flush()

def send_chat():
    if values['chat_input']:
        chat_message = values['chat_input']
        command = f"say {chat_message}"
        process.stdin.write(command + "\n")
        process.stdin.flush() 
        message_list.append(f'[Server] {chat_message}')
        window["ingame_chat"].update(values=message_list)
        window['chat_input'].update('')



# create the GUI layout

headings = ['Name', 'Xuid', 'Level']

#sg.theme('DefaultNoMoreNagging')
sg.theme('Darkamber')

# a list of all the settings and their default values

SETTINGS1 = settings.SETTINGS1 
    
SETTINGS2 = settings.SETTINGS2

SETTINGS3 = settings.SETTINGS3

# ----------------- update the settings gui with values from server.properties----------------- #

def update_settings(settings_list):
    # Open the server.properties file
    with open(properties_dir, 'r') as f:
        # Read the file contents into a dictionary
        settings = {line.split('=')[0].strip().lower().replace(' ', '-'): line.split('=')[1].strip() for line in f if '=' in line and not line.strip().startswith('# ')}

    # Iterate over the settings list and update the setting value from the file, if available
    for i, setting in enumerate(settings_list):
        # Only update the setting value if it is not None
        if setting[1] is not None:
            # Format the setting name to match the format in the file
            setting_name = setting[0].lower().replace(' ', '-')
            # If the setting name is found in the file, update the value in the settings list
            if setting_name in settings:
                # Use the code to capitalize the words with the condition you provided
                setting_value = settings[setting_name]
                capitalized_value = " ".join(word.title() if word.islower() else word for word in setting_value.split()).replace('-', ' ')
                # Add boolean value if setting is "true" or "false"
                if setting_value.lower() == "true":
                    settings_list[i] = (setting[0], True, setting[2], setting[3], setting[4])
                elif setting_value.lower() == "false":
                    settings_list[i] = (setting[0], False, setting[2], setting[3], setting[4])
                else:
                    # Convert to int or float if possible
                    try:
                        int_value = int(setting_value)
                        settings_list[i] = (setting[0], int_value, setting[2], setting[3], setting[4])
                    except ValueError:
                        try:
                            float_value = float(setting_value)
                            settings_list[i] = (setting[0], float_value, setting[2], setting[3], setting[4])
                        except ValueError:
                            settings_list[i] = (setting[0], capitalized_value, setting[2], setting[3], setting[4])


update_settings(SETTINGS1)
update_settings(SETTINGS2)
update_settings(SETTINGS3)

# ----------------- update the settings gui with values from server.properties----------------- #

message_list = []

menu_column = [
    [sg.Text("Bedrock Server Pilot", font = "lucida 12", justification = "center", pad = (8,2))],
    [sg.Button("Home", size = (27,2), pad = 10, font = "lucida 10")],
    [sg.Button("Addon Manager", size = (27,2), pad = 10, font = "lucida 10")],
    [sg.Button("Player Manager", size = (27,2), pad = 10, font = "lucida 10")],
    [sg.Button("Backup Manager", size = (27,2), pad = 10, font = "lucida 10")],
    [sg.Button("Analasys", size = (27,2), pad = 10, font = "lucida 10")],
    [sg.Button("Server Settings", size = (27,2), pad = (10, 10), font = "lucida 10")],
    [sg.Button("BSPilot Settings", size = (27,2), pad = (10, 10), font = "lucida 10")],
    ]

menu_column += [[sg.Text(" ")] for i in range(23)]

home_operations_column = [
    [sg.Text("Server Status:", pad=(0,0)), sg.Text("Stopped", key="-SERVER_STATE-")],
    [sg.Button('Start', button_color="green", size = (17,2)), 
     sg.Button('Restart', button_color="#DBA800", size = (17,2)), 
     sg.Button('Stop', button_color="red", size = (17,2))],
    [sg.Button('Shortcut1', size = (27,0)), sg.Button('Shortcut3', size = (27,0))], 
    [sg.Button('Shortcut2', size = (27,0)), sg.Button('Shortcut4', size = (27,0))], 
    
    [sg.Text('—'*35, pad = (0,0), justification = "center")],
    [sg.Text("Online Players:"), sg.Text("0", key=("-ONLINE_PLAYERS-"))],
    [sg.Table(headings=headings, values=player_list, enable_events=True, justification='center', auto_size_columns=False, def_col_width=16, num_rows= 19, key='player_list')],
    [sg.Button('OP', size = (17,0)), 
     sg.Button('DEOP', size = (17,0)), 
     sg.Button('Kick', size = (17,0))],
    [sg.Button("Test", key=("-TEST-"), visible=False)],
    [sg.Text('—'*35, pad = (0,0), justification = "center")],
    [sg.Text("Ingame Chat:")],
    [sg.Listbox(values=message_list, size=(60, 20), key='ingame_chat')],
    [sg.InputText(size=(51,1), key='chat_input'), sg.Button('Send', size=(8,1), key='send_chat')],
    ]
    
home_output_column = [
    [sg.Text(' Console Output:')],
    [sg.Multiline(size=(160, 30), key='output', autoscroll=True, disabled=True)],
    [sg.InputText(size=(154,1), key='input'), sg.Button('Run', size=(5,1))],
    [sg.Text('Server Information', font=('Helvetica', 16), size=(53,0), justification='right', pad=(0,10))],
    [sg.Text('Server Name:', size=(40,0), justification='left', ), sg.Text('Info6:', size=(40,0), justification='center'), sg.Text('Info11:', size=(40,0), justification='right')],
    [sg.Text('Level Name:', size=(40,0), justification='left'), sg.Text('Info7:', size=(40,0), justification='center'), sg.Text('Info12:', size=(40,0), justification='right')],
    [sg.Text('Gamemode:', size=(40,0), justification='left'), sg.Text('Info8:', size=(40,0), justification='center'), sg.Text('Info13:', size=(40,0), justification='right')],
    [sg.Text('Difficulty', size=(40,0), justification='left'), sg.Text('Info9:', size=(40,0), justification='center'), sg.Text('Info14:', size=(40,0), justification='right')],
    [sg.Text('Info5:', size=(40,0), justification='left'), sg.Text('Info10:',size=(40,0), justification='center'), sg.Text('Info15:', size=(40,0), justification='right')],
    [sg.Text('—'*88, pad = (0,0), justification = "center")],
    [sg.Text('CPU / Ram Usage', font=('Helvetica', 16), size=(53,0), justification='right', pad=(0,10))],
    ]
    
    
home_column = [
[sg.Column(home_output_column, justification = "left", vertical_alignment = ("top")),
sg.Column(home_operations_column, justification = "right", vertical_alignment = ("top"))]]

addon_manager_column = [
    [sg.Text('Addon Manager', font=('Helvetica', 24))],
    [sg.Button('Lauch Addon Manager', size=(27,2))]
    ]

player_manager_column = [[sg.Text('Player Manager UI')]]

backup_manager_column = [[sg.Text('Backup Manager UI')]]

analasys_column = [[sg.Text('Analasys UI')]]

# ------------------ code to assemble settings gui from settings.py ------------------------ #

server_settings_column1 = []

for setting_name, setting_value, options, description, tooltip in SETTINGS1:
    if options is None and description is None and setting_value is None:
        server_settings_column1.append([sg.Text(setting_name)])
    else:
        setting_name_f = setting_name.lower().replace(' ', '-')
        if isinstance(setting_value, bool):
            value_input = sg.Checkbox('', default=setting_value, key=setting_name_f)
        elif options is not None:
            value_input = sg.Combo(options, default_value=setting_value, size=(15,0), key=setting_name_f, readonly=True)
        else:
            value_input = sg.InputText(str(setting_value), size=(17,0), key=setting_name_f)

        setting_layout = [
            [value_input, sg.Text('?', tooltip=tooltip, pad=(0,0), text_color='cyan'), sg.Text(setting_name)],
            [sg.Text(description)]
        ]

        setting_column = sg.Column(setting_layout, element_justification='left')

        server_settings_column1.append([setting_column])


# Create the layout for the server settings window
server_settings_column2 = []

for setting_name, setting_value, options, description, tooltip in SETTINGS2:
    if options is None and description is None and setting_value is None:
        server_settings_column2.append([sg.Text(setting_name)])
    else:
        setting_name_f = setting_name.lower().replace(' ', '-')
        if isinstance(setting_value, bool):
            value_input = sg.Checkbox('', default=setting_value, key=setting_name_f)
        elif options is not None:
            value_input = sg.Combo(options, default_value=setting_value, size=(15,0), key=setting_name_f, readonly=True)
        else:
            value_input = sg.InputText(str(setting_value), size=(17,0), key=setting_name_f)

        setting_layout = [
            [value_input, sg.Text('?', tooltip=tooltip, pad=(0,0), text_color='cyan'), sg.Text(setting_name)],
            [sg.Text(description)]
        ]

        setting_column = sg.Column(setting_layout, element_justification='left')

        server_settings_column2.append([setting_column])

server_settings_column3 = []

for setting_name, setting_value, options, description, tooltip in SETTINGS3:
    if options is None and description is None and setting_value is None:
        server_settings_column3.append([sg.Text(setting_name)])
    else:
        setting_name_f = setting_name.lower().replace(' ', '-')
        if isinstance(setting_value, bool):
            value_input = sg.Checkbox('', default=setting_value, key=setting_name_f)
        elif options is not None:
            value_input = sg.Combo(options, default_value=setting_value, size=(15,0), key=setting_name_f, readonly=True)
        else:
            value_input = sg.InputText(str(setting_value), size=(17,0), key=setting_name_f)

        setting_layout = [
            [value_input, sg.Text('?', tooltip=tooltip, pad=(0,0), text_color='cyan'), sg.Text(setting_name)],
            [sg.Text(description)]
        ]

        setting_column = sg.Column(setting_layout, element_justification='left')

        server_settings_column3.append([setting_column])

# ------------------ code to assemble settings gui from settings.py ----------------------- #

# Combine the columns into a single layout
server_settings_column = [
    [sg.Text(' Server Settings', font=('Helvetica', 24))], 
    [sg.Column(server_settings_column1, element_justification='left', vertical_alignment='top'), 
     sg.Column(server_settings_column2, element_justification='left', vertical_alignment='top'), 
     sg.Column(server_settings_column3, element_justification='left', vertical_alignment='top')],
    [sg.Text('—'*130, pad = (0,0), justification = "center")],
    [sg.Button('Save', size=(65,1)), sg.Button('Reset', size=(65,1)), sg.Button('Save Config', size=(66,1))]
]

bspilot_settings_column = [
    [sg.Text('BSPilot Settings UI')]
                              
    ]

layout = [
    [
    sg.Column(menu_column,visible=True ,justification = "left", vertical_alignment = ("top")),
    sg.VerticalSeparator(pad = (8,8)),
    sg.Column(home_column, justification = "left", key='-COLHome-', vertical_alignment = ("top")), 
    sg.Column(addon_manager_column, visible=False, justification = "left", key='-COLAddon Manager-', vertical_alignment = ("top")),
    sg.Column(player_manager_column, visible=False, justification = "left", key='-COLPlayer Manager-', vertical_alignment = ("top")),
    sg.Column(backup_manager_column, visible=False, justification = "left", key='-COLBackup Manager-', vertical_alignment = ("top")),
    sg.Column(analasys_column, visible=False, justification = "left", key='-COLAnalasys-', vertical_alignment = ("top")),
    sg.Column(server_settings_column, visible=False, justification = "left", key='-COLServer Settings-', vertical_alignment = ("top")),
    sg.Column(bspilot_settings_column, visible=False, justification = "left", key='-COLBSPilot Settings-', vertical_alignment = ("top")),
    ]]

window = sg.Window('Bedrock Server Pilot', layout, size = (1200,600), finalize=True, resizable=True)
window.maximize()
layout = ("Home")



def save_config(): # saves the current server.properties with users name to settings_backups folder
    # Define the layout of the popup window
    layout = [
        [sg.Text('Enter a name for the save:')],
        [sg.Input(key='save_name', size=(45,0))],
        [sg.Button('Cancel', size=(18,0)), sg.Button('Save', bind_return_key=True, size=(19,0))]
    ]

    # Create the popup window
    window = sg.Window('Save Config', layout)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Cancel'):
            break
        elif event == 'Save':
            save_name = values['save_name'].replace(' ', '_')

            # Validate the save name
            if save_name:
                # Create the 'settings_backups' folder if it doesn't exist
                backup_folder = os.path.join(os.getcwd(), 'settings_backups')
                os.makedirs(backup_folder, exist_ok=True)

                # Check if a backup with the same name already exists
                backup_name = f"{save_name}.properties"
                backup_path = os.path.join(backup_folder, backup_name)
                backup_count = 2

                while os.path.exists(backup_path):
                    # Append a number to the backup name
                    backup_name = f"{save_name}_{backup_count}.properties"
                    backup_path = os.path.join(backup_folder, backup_name)
                    backup_count += 1

                # Copy server.properties to the backup folder with the final backup name
                shutil.copyfile(properties_dir, backup_path)
                sg.Popup(f"Settings config saved as: {backup_name}")
                break
            else:
                sg.Popup('Please enter a valid save name.')

    window.close()



def reset_settings(): # resets settings to values from server.properties if you have changed unwanted settings
    # Read the current server properties and store them in a dictionary
    with open(properties_dir, 'r') as f:
        current_settings = dict(line.strip().split('=') for line in f if '=' in line and not line.startswith('#'))

    # Update the GUI with the current settings
    for settings_list in [SETTINGS1, SETTINGS2, SETTINGS3]:
        for setting_name, setting_value, options, description, tooltip in settings_list:
            if options is None and description is None and setting_value is None:
                server_settings_column3.append([sg.Text(setting_name)])
            else:
                setting_name_formatted = setting_name.lower().replace(' ', '-')
                if setting_name_formatted in current_settings:
                    # Find the GUI element by its key and update its value
                    element_key = setting_name_formatted

                    # Convert the string value to boolean
                    setting_value1 = current_settings[setting_name_formatted].title().replace('-', ' ')
                    setting_value_f = " ".join(word.title() if word.islower() else word for word in setting_value1.split()).replace('-', ' ')
                    if setting_value_f.lower() == 'true':
                        setting_value_f = True
                    elif setting_value_f.lower() == 'false':
                        setting_value_f = False

                    window[element_key].update(setting_value)

    # Refresh the GUI window to reflect the updated values
    window.refresh()


def save_settings(values): # save changed settings to server.properties and ask the user to confirm with a popup and list of all changed settings
    # Read the current server properties and store them in a list of lines
    with open(properties_dir, 'r') as f:
        lines = [line.strip() for line in f]

    # Update the settings from the GUI input and check for changes
    changed_settings = []
    for settings_list in [SETTINGS1, SETTINGS2, SETTINGS3]:
        for setting_name, setting_value, options, description, tooltip in settings_list:
            if options is None and description is None and setting_value is None:
                server_settings_column3.append([sg.Text(setting_name)])
            else:
                setting_name_formatted = setting_name.lower().replace(' ', '-')
                if setting_name_formatted in values:
                    updated_setting_value = values[setting_name_formatted]
                    for i, line in enumerate(lines):
                        if line.startswith(setting_name_formatted + '='):
                            current_value = " ".join(word.title() if word.islower() else word for word in line.split('=', 1)[1].split()).replace('-', ' ')

                            if current_value.lower() == "true":
                                current_value = True
                            elif current_value.lower() == "false":
                                current_value = False
                            if current_value != updated_setting_value:
                                changed_settings.append(f"{setting_name}: {current_value} -> {updated_setting_value}")
                            lines[i] = f"{setting_name_formatted}={updated_setting_value}"
                            break

    # If there are changed settings, prompt the user to confirm before saving
    if changed_settings:
        confirm_popup_layout = [
            [sg.Text('Are You Sure You Want To Change The Following Settings:')],
            [sg.Multiline('\n'.join(changed_settings), size=(60, 10), disabled=True)],
            [sg.Button('Cancel', size=(26,1)), sg.Button('Save', bind_return_key=True, size=(26,1))]
        ]
        confirm_popup = sg.Window('Confirm Settings Change', confirm_popup_layout)

        while True:
            event, _ = confirm_popup.read()
            if event in (sg.WIN_CLOSED, 'Cancel'):
                break
            elif event == 'Save':
                # Write the updated settings back to the file
                with open(properties_dir, 'w') as f:
                    for line in lines:
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                
                            if line.startswith('server-name=') or line.startswith('level-name=') or line.startswith('server-build-radius-ratio=') or line.startswith('chat-restriction='):
                                f.write(f"{line}\n")

                            else:
                                formatted_value = '-'.join(word.lower() for word in value.split())
                                f.write(f"{key}={formatted_value}\n")
                        else:
                            f.write(f"{line}\n")


                break

        confirm_popup.close()
    else:
        sg.Popup('No Settings Have Been Changed')

#---------chat stuff----------#

message_log_file = "message_log.txt"  # File to save the messages

def save_message_to_file(message):
    global latest_message
    with open(message_log_file, "a") as file:
        file.write(message + "\n")
    latest_message = message

#---------chat stuff----------#

while True:
    # read the window's events
    event, values = window.read()
    print(event)

    if event is not None and event in 'Home, Addon Manager, Player Manager, Backup Manager, Analasys, Server Settings, BSPilot Settings':
        window[f'-COL{layout}-'].update(visible=False)
        layout = str(event)
        window[f'-COL{layout}-'].update(visible=True)
        window.read

    if event == 'Start':
    # Check if the process is already running
        if process is not None:
            sg.popup('Server is already running')
        else:
            # run the .bat file with the command as an argument
            stop_flag = False
            start_server()
            #http_server_thread.start()

    if event == 'Restart': # i removed all restart and auto restart code as it was unstable, will work on it later
        window["ingame_chat"].update(values=message_list)
        restart_server()

    if event == 'Stop':
        if process is None:
            sg.popup('Server is not running')
        else:
            stop_server()
            #stop_http_server()
            player_list = []  # clear the player list
            window['player_list'].update(values=player_list)
            player_count = 0  # reset the player count
            window['-ONLINE_PLAYERS-'].update(player_count)
            window["ingame_chat"].update('')

    if event == 'Run':
        print("run", values['input'])
        run_command(values)

    if event == 'OP':
        op_player()

    if event == 'DEOP':
        deop_player()

    if event == 'Kick':
        kick_player()

    elif event == 'send_chat':
        send_chat()

    elif event == "Shortcut1":
        print('Shortcut1') 

    elif event == "Shortcut2":
        print('Shortcut2')

    elif event == "Shortcut3":
        print('Shortcut3')

    elif event == "Shortcut4":
        print('Shortcut4')

    elif event == "Lauch Addon Manager":
        addon_manager.launch_addon_manager()

    elif event == 'Save':
        save_settings(values)

    elif event == 'Reset':
        reset_settings()
    
    elif event == 'Save Config':
        save_config()


    # if the 'Exit' button is clicked or the window is closed
    if event in (None,):
        if process is not None:
            stop_server()
            #stop_http_server()
            break
        else:
            break

# close the window
window.close()

