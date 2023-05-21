import os
import PySimpleGUI as sg
import shutil
def backup():
    try:
        backup_location = values[0]
        file_format = values[1]
        backup_name = os.path.basename(os.getcwd()) + '_' + file_format[1:]
        shutil.make_archive(backup_name, file_format[1:], os.getcwd())
        shutil.move(backup_name + '.' + file_format[1:], backup_location)
        print(f'Backup created at {backup_location}')
    except Exception as e:
        print(f'Error: {e}')
sg.theme('DarkAmber')

layout = [[sg.Text('Select Backup Location'), sg.Input(), sg.FolderBrowse()],
          [sg.Text('Select File Format'), sg.Combo(['.zip', '.tar.gz'], default_value='.zip')],
          [sg.Output(size=(60, 10))],
          [sg.Button('Backup Now'), sg.Button('Cancel')]]

window = sg.Window('Backup Program', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == 'Backup Now':
        backup()

window.close()
