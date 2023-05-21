import os
import PySimpleGUI as sg
import zipfile
import shutil
import re
import json

# the only difference between this is that everything is in a function, so it can be run from the main file
# this is more of a test

def launch_addon_manager():
    
    def select_world_folder():
        # Get the current working directory
        current_dir = os.getcwd()
    
        # Construct the path to the 'worlds' folder
        worlds_dir = os.path.join(current_dir, 'worlds')
    
        # Check if 'worlds' folder exists
        if not os.path.exists(worlds_dir):
            sg.popup_error("The 'worlds' folder does not exist!")
            return None
    
        # Get a list of all directories inside the 'worlds' folder
        try:
            world_folders = [f.name for f in os.scandir(worlds_dir) if f.is_dir()]
        except:
            sg.popup_error("An error occurred while trying to read the 'worlds' folder!")
            return None
    
        # Check if 'worlds' folder is empty
        if not world_folders:
            sg.popup_error("The 'worlds' folder is empty!")
            return None
    
        # Create a PySimpleGUI layout for selecting the world folder
        layout = [
            [sg.Text('Select the world folder:')],
            [sg.Listbox(values=world_folders, size=(30, 10), key='-WORLD-FOLDER-LIST-')],
            [sg.Button('Select', bind_return_key=True)]
        ]
    
        # Create a PySimpleGUI window
        window = sg.Window('Select World Folder', layout)
    
        # Loop until the user selects a world folder or closes the window
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                # User closed the window, so return None
                return None
            elif event == 'Select':
                # User selected a world folder, so return the path to that folder
                selected_folder = values['-WORLD-FOLDER-LIST-']
                if not selected_folder:
                    sg.popup_error("Please select a world folder!")
                    continue
                selected_folder = selected_folder[0]
                server_world_path = os.path.join(worlds_dir, selected_folder)
                return server_world_path
    server_world_path = ()
    def scan_data_run():
        # define data and resources folders
        data_folder = os.path.join(os.getcwd(), "data")
        resources_folder = os.path.join(os.getcwd(), "resources")
    
        # scan data and resources folders for manifest files
        data_info = {}
        resources_info = {}
    
        for root, _, files in os.walk(resources_folder):
            for file in files:
                if file == "manifest.json":
                    manifest_path = os.path.join(root, file)
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                        uuid = manifest["header"]["uuid"]
                        version = manifest["header"]["version"]
                        resources_info[uuid] = version
    
        for root, _, files in os.walk(data_folder):
            for file in files:
                if file == "manifest.json":
                    manifest_path = os.path.join(root, file)
                    with open(manifest_path) as f:
                        manifest = json.load(f)
                        uuid = manifest["header"]["uuid"]
                        version = manifest["header"]["version"]
                        data_info[uuid] = version
    
        # print info for data folders
        print("\nData folders:")
        for uuid, version in data_info.items():
            print(f"{uuid} [{', '.join(map(str, version))}] (from data)")
    
        # print info for resources folders
        print("\nResources folders:")
        for uuid, version in resources_info.items():
            print(f"{uuid} [{', '.join(map(str, version))}] (from resources)")
    
        # find addon_json folder and write to world_behavior_packs.json
        addon_json_folder = os.path.join(os.getcwd(), "addon_json")
        world_behavior_packs_path = os.path.join(addon_json_folder, "world_behavior_packs.json")
        world_resources_packs_path = os.path.join(addon_json_folder, "world_resource_packs.json")
    
        try:
            with open(world_behavior_packs_path, "w") as f:
                f.write("[\n")
                for uuid, version in data_info.items():
                    f.write(f"  {{\n    \"pack_id\": \"{uuid}\",\n    \"version\": {json.dumps(version)}\n  }},\n")
                # remove the last comma and add a newline and closing bracket
                f.seek(f.tell() - 2, os.SEEK_SET)
                f.write("\n]\n")
            print(f"\nSuccessfully wrote to {world_behavior_packs_path}")
        except IOError:
            print(f"\nError writing to {world_behavior_packs_path}")
    
        try:
            with open(world_resources_packs_path, "w") as f:
                f.write("[\n")
                for uuid, version in resources_info.items():
                    f.write(f"  {{\n    \"pack_id\": \"{uuid}\",\n    \"version\": {json.dumps(version)}\n  }},\n")
                # remove the last comma and add a newline and closing bracket
                f.seek(f.tell() - 2, os.SEEK_SET)
                f.write("\n]\n")
            print(f"\nSuccessfully wrote to {world_resources_packs_path}")
        except IOError:
            print(f"\nError writing to {world_resources_packs_path}")
            
    
    # check and create the addon_json folder if it doesn't exist
    addon_json_path = "./addon_json"
    if not os.path.exists(addon_json_path):
        os.makedirs(addon_json_path)
        print(f"Created folder: {addon_json_path}")
    else:
        print(f"Folder already exists: {addon_json_path}")
    
    # create the world_resource_packs.json and world_behavior_packs.json files if they don't exist
    resource_packs_file = os.path.join(addon_json_path, "world_resource_packs.json")
    behavior_packs_file = os.path.join(addon_json_path, "world_behavior_packs.json")
    if not os.path.exists(resource_packs_file):
        open(resource_packs_file, 'w').close()
        print(f"Created file: {resource_packs_file}")
    else:
        print(f"File already exists: {resource_packs_file}")
    if not os.path.exists(behavior_packs_file):
        open(behavior_packs_file, 'w').close()
        print(f"Created file: {behavior_packs_file}")
    else:
        print(f"File already exists: {behavior_packs_file}")
    print("program loaded!")
    # Define the folder paths
    folders = ['addons', 'data', 'resources', 'addons/archives']
    
    # Loop through each folder path
    for folder in folders:
        path = os.path.join(os.getcwd(), folder)  # Get the full path to the folder
        if not os.path.exists(path):  # Check if the folder exists
            os.makedirs(path)  # Create the folder if it doesn't exist
    data_dir = "data"
    resource_dir = "resources"
    data_files = os.listdir(data_dir)
    resource_files = os.listdir(resource_dir)
    data_files_list = list(data_files)
    resource_files_list = list(resource_files)
            
    sg.theme("DarkAmber")
    # Function to find all subfolders and files in the addons folder
    def get_addons_folders():
        addons_dir = "addons"
        if not os.path.exists(addons_dir):
            os.makedirs(addons_dir)
        addons = [os.path.basename(os.path.join(addons_dir, f)) for f in os.listdir(addons_dir) if os.path.isfile(os.path.join(addons_dir, f)) and f.endswith((".zip", ".mcaddon", ".mcpack"))]
        folders = [os.path.basename(os.path.join(addons_dir, f)) for f in os.listdir(addons_dir) if os.path.isdir(os.path.join(addons_dir, f))]
        
        # Check for archives folder and add archives to the list
        archives_dir = os.path.join(addons_dir, "archives")
        archives = []
        if os.path.exists(archives_dir):
            archives = [f"{filename} (archive)" for filename in os.listdir(archives_dir)]
        
        # Add all addons to the list
        addons_list = sorted(addons + folders + archives)
        return addons_list
    
    
    # Function to find the manifest file and extract information from it
    def scan_folder(folder):
        manifest_file = os.path.join("addons", folder, "manifest.json")
        if not os.path.exists(manifest_file):
            print(f"Error: The manifest file for the '{folder}' folder could not be found.")
            return
    
        with open(manifest_file, "r") as file:
            content = file.read()
            if "type\": \"resources" in content:
                addon_type = "resources"
                print(f"The folder {folder} is a resource type.")
            elif "type\": \"data" in content:
                addon_type = "data"
                print(f"The folder {folder} is a data type.")
            else:
                print(f"Error: The '{folder}' folder has an unknown type.")
                return
    
            if "\"uuid\"" in content:
                uuid = content.split("\"uuid\": \"")[1].split("\"")[0]
                print(f"The UUID of the {folder} folder is {uuid}.")
            else:
                print(f"Error: The UUID for the '{folder}' folder could not be found in the manifest.")
                return
    
        if addon_type == "resources":
            addon_dir = os.path.join("resources")
        elif addon_type == "data":
            addon_dir = os.path.join("data")
        else:
            print(f"Error: The '{folder}' folder has an unknown type.")
            return
    
        os.makedirs(addon_dir, exist_ok=True)
        shutil.move(os.path.join("addons", folder), addon_dir)
    # Callback function for the "Cleanup Archives" button
    def cleanup_archives():
        archives_dir = os.path.join("addons", "archives")
        if os.path.exists(archives_dir):
            shutil.rmtree(archives_dir)
            os.mkdir(archives_dir)
            print("Archives cleaned up.")
        else:
            print("Archives folder not found.")
            
    # Function to unzip addon files
    def extract_archives():
        addons_folder = "addons"
        archives_folder = os.path.join(addons_folder, "archives")
        if not os.path.exists(archives_folder):
            os.mkdir(archives_folder)
        for filename in os.listdir(addons_folder):
            file_path = os.path.join(addons_folder, filename)
            if os.path.isfile(file_path) and filename.endswith((".mcaddon", ".mcpack", ".zip")):
                print(f"Unzipping {filename}...")
                try:
                    with zipfile.ZipFile(file_path, "r") as zip_ref:
                        zip_ref.extractall(addons_folder)
                    os.rename(file_path, os.path.join(archives_folder, filename))
                    print(f"{filename} has been unzipped and moved to the archives folder.")
                    window["folders"].update(values=get_addons_folders())
                except Exception as e:
                    print(f"Error: Could not unzip {filename}: {e}")
    
    
    # Define the GUI layout
    left_column = [
        [sg.Text("Select a folder to Scan n' Move:")],
        [sg.Listbox(values=get_addons_folders(), size=(30, 10), key="folders", select_mode="multiple"), sg.Output(size=(30, 10))],
        [sg.Text("Select file to upload:")],
        [sg.Input(key="-FILE-"), sg.FileBrowse(), sg.Button("Upload", tooltip="Uploads the selected file to addons")],
        [sg.Button("Scan n' Move", tooltip="after selecting a folder,\n press the button and the addon will be scanned for it's type and uuid,\n and get sent to the respective folder (data or resources) "), sg.Button("Refresh All", tooltip='refreshes all file lists'), sg.Button("Extract Uploaded Archives", tooltip='after uploading, select the archive you want to extract and press this button')],
        [sg.Button("Cleanup Archives Folder", tooltip='This cleans the folder where all the old archive files are moved to'), sg.Button("Delete Selected", tooltip="deletes the selected items from the directory")],
        [sg.Text("Version: Helium 4")]
    ]
    
    right_column = [
        [sg.Text("Data packs"), sg.Listbox(values=data_files, size=(25, 5), key='-DATA-', enable_events=True),sg.Text("Resource packs"), sg.Listbox(values=resource_files, size=(25, 5), key='-RESOURCES-', enable_events=True)],
        [sg.Button("Delete a Data Folder"), sg.Button("Delete a Resources Folder", tooltip='cum')],
        [sg.Button("Process Folders", tooltip='creates shortcuts for the addons \nand sends them to their respective folders')],
        [sg.Button("Add the sources to JSON", tooltip='adds all manifest data from addons \nand writes them to JSON files')],
        [sg.Button('Select the world folder', key='-SELECT-FOLDER-', tooltip='select the world for importing JSON addon files')],
        [sg.Text('Selected world folder:'), sg.Text(size=(30, 1), key='-SELECTED-FOLDER-')],
        [sg.Button("Import JSON to Selected World", tooltip='after selecting the world, press this \nto import the JSON addon files to the world ')]
    ]
    
    layout = [[sg.Column(left_column), sg.VSeperator(), sg.Column(right_column)]]
    
    
    
    
    
    # Create the GUI window
    window = sg.Window("BSP Addon Pilot", layout)
    
    # Define a function to add the addon to the JSON file
    def add_to_json(uuid, version):
        # Get the path to the addon_json folder
        addon_json_path = os.path.join(os.getcwd(), "addon_json")
    
        # Make sure the addon_json folder exists
        if not os.path.exists(addon_json_path):
            os.mkdir(addon_json_path)
    
        # Get the path to the world_behavior_packs.json file
        behavior_packs_path = os.path.join(addon_json_path, "world_behavior_packs.json")
    
        # Make sure the world_behavior_packs.json file exists
        if not os.path.exists(behavior_packs_path):
            with open(behavior_packs_path, "w") as f:
                f.write("[]")
    
        # Load the contents of the world_behavior_packs.json file
        with open(behavior_packs_path, "r") as f:
            contents = json.load(f)
    
        # Check if the pack is already in the file
        pack_found = False
        for pack in contents:
            if pack.get("pack_id") == uuid and pack.get("version") == version:
                pack_found = True
                break
            
        # If the pack is not in the file, add it
        if not pack_found:
            contents.append({"pack_id": uuid, "version": version})
            with open(behavior_packs_path, "w") as f:
                json.dump(contents, f)
    
        # Display a success message
        sg.popup("The pack has been added to the JSON file.")
    
    # Event loop
    while True:
        event, values = window.read()
        if event == "Import JSON to Selected World":
            try:
                # Get the selected folder path
                folder_path = server_world_path
                
                # Get the path of the addon_json folder
                json_folder_path = os.path.join(os.getcwd(), "addon_json")
                
                # Copy all the files from the addon_json folder to the selected folder
                for file_name in os.listdir(json_folder_path):
                    file_path = os.path.join(json_folder_path, file_name)
                    if os.path.isfile(file_path):
                        shutil.copy2(file_path, folder_path)
                
                # Show success message
                sg.popup("JSON files imported successfully!")
            
            except Exception as e:
                # Show error message
                sg.popup(f"Error: {e}")
        if event == '-SELECT-FOLDER-':
            # User clicked the 'Select the world folder' button, so call the select_world_folder function
            selected_folder = select_world_folder()
            if selected_folder:
                # User selected a folder, so update the selected folder text in the main window
                window['-SELECTED-FOLDER-'].update(selected_folder)
                server_world_path = (selected_folder)
        if event == "Add the sources to JSON":
            # If the user clicks the "Add the sources to JSON" button, run the Scan operator
            scan_data_run()
        if event == sg.WIN_CLOSED:
            break
        if event == "Scan n' Move":
            selected_folders = values.get("folders", [])
            if not selected_folders:
                print("Error: Please select a folder to scan.")
                continue
            for selected_folder in selected_folders:
                scan_folder(selected_folder)
            window["folders"].update(values=get_addons_folders())
            resource_files = os.listdir("resources")
            window['-RESOURCES-'].update(values=resource_files)
            data_files = os.listdir("data")
            window['-DATA-'].update(values=data_files)
        if event == "Refresh All":
            window["folders"].update(values=get_addons_folders())
            window["folders"].update(values=get_addons_folders())
            resource_files = os.listdir("resources")
            window['-RESOURCES-'].update(values=resource_files)
            data_files = os.listdir("data")
            window['-DATA-'].update(values=data_files)
        #if event == "Unzip Addons":
        #    unzip_addon_files()
        #    window["folders"].update(values=get_addons_folders())
        #    window["folders"].update(values=get_addons_folders())
        #    resource_files = os.listdir("resources")
        #    window['-RESOURCES-'].update(values=resource_files)
        #    data_files = os.listdir("data")
        #    window['-DATA-'].update(values=data_files)
        if event == "Cleanup Archives Folder":
            cleanup_archives()
            window["folders"].update(values=get_addons_folders())
            window["folders"].update(values=get_addons_folders())
            resource_files = os.listdir("resources")
            window['-RESOURCES-'].update(values=resource_files)
            data_files = os.listdir("data")
            window['-DATA-'].update(values=data_files)
        if event == "Extract Uploaded Archives":
            extract_archives()
            window["folders"].update(values=get_addons_folders())
            resource_files = os.listdir("resources")
            window['-RESOURCES-'].update(values=resource_files)
            data_files = os.listdir("data")
            window['-DATA-'].update(values=data_files)
        if event == "Upload":
            # Get the path of the selected file
            file_path = values["-FILE-"]
            if not file_path:
                sg.popup("Please select a file to upload.")
                continue
            
            # Get the filename and extension of the file
            file_name, file_ext = os.path.splitext(file_path)
    
            # Check if the file extension is valid
            if file_ext.lower() not in (".mcaddon", ".mcpack", ".zip"):
                sg.popup(f"Error: Invalid file extension '{file_ext}'. Only .mcaddon, .mcpack, and .zip files are allowed.")
                continue
            
            # Copy the file to the addons folder
            addons_folder = "addons"
            if not os.path.exists(addons_folder):
                os.makedirs(addons_folder)
            shutil.copy(file_path, addons_folder)
    
            sg.popup("File uploaded successfully.")
            window["-FILE-"].update("")
            window["folders"].update(values=get_addons_folders())
            resource_files = os.listdir("resources")
            window['-RESOURCES-'].update(values=resource_files)
            data_files = os.listdir("data")
            window['-DATA-'].update(values=data_files)
        # handle button events
        elif event == "Delete a Data Folder":
            data_folders = values["-DATA-"]
            if data_folders:
                selected_folder = data_folders[0]
                try:
                    if sg.popup_yes_no(f"Delete {selected_folder}?", title="Confirm Delete") == "Yes":
                        shutil.rmtree(os.path.join("data", selected_folder))
                        data_files = os.listdir("data")
                        window['-DATA-'].update(values=data_files)
                except Exception as e:
                    sg.popup_error(f"Error deleting {selected_folder}: {str(e)}")
        elif event == "Delete a Resources Folder":
            resources_folders = values["-RESOURCES-"]
            if resources_folders:
                selected_folder = resources_folders[0]
                try:
                    if sg.popup_yes_no(f"Delete {selected_folder}?", title="Confirm Delete") == "Yes":
                        shutil.rmtree(os.path.join("resources", selected_folder))
                        resource_files = os.listdir("resources")
                        window['-RESOURCES-'].update(values=resource_files)
                except Exception as e:
                    sg.popup_error(f"Error deleting {selected_folder}: {str(e)}")
        elif event == "Delete Selected":
            selected_items = values.get("folders", [])
            if not selected_items:
                print("Error: Please select an item to delete.")
                continue
            for item in selected_items:
                if item == "archives":
                    print("Error: Cannot delete the 'archives' folder.")
                    continue
                file_path = os.path.join("addons", item)
                if os.path.exists(file_path):
                    try:
                        shutil.rmtree(file_path)  # Use shutil.rmtree() to delete a directory and all its contents recursively.
                    except Exception as e:
                        print(f"Error: Failed to delete '{item}' folder with error: {e}")
                else:
                    print(f"Error: '{item}' folder does not exist.")
        elif event == "Process Folders":
            try:
                # Find the data and resources folders
                data_path = os.path.join(os.getcwd(), "data")
                resources_path = os.path.join(os.getcwd(), "resources")
    
                # Get a list of all the subfolders in the data folder and create shortcuts
                for folder_name in os.listdir(data_path):
                    folder_path = os.path.join(data_path, folder_name)
                    if os.path.isdir(folder_path):
                        shortcut_path = os.path.join(os.getcwd(), "behavior_packs", folder_name + "_shortcut")
                        if not os.path.exists(shortcut_path):
                            os.symlink(folder_path, shortcut_path)
    
                # Get a list of all the subfolders in the resources folder and create shortcuts
                for folder_name in os.listdir(resources_path):
                    folder_path = os.path.join(resources_path, folder_name)
                    if os.path.isdir(folder_path):
                        shortcut_path = os.path.join(os.getcwd(), "resource_packs", folder_name + "_shortcut")
                        if not os.path.exists(shortcut_path):
                            os.symlink(folder_path, shortcut_path)
    
                # Move the shortcuts to the appropriate folders
                for folder_name in os.listdir(os.getcwd()):
                    if "_shortcut" in folder_name:
                        shortcut_path = os.path.join(os.getcwd(), folder_name)
                        if "data" in folder_name:
                            destination_path = os.path.join(os.getcwd(), "behavior_packs", folder_name[:-9])
                            if not os.path.exists(destination_path):
                                os.mkdir(destination_path)
                            shutil.move(shortcut_path, destination_path)
                        elif "resources" in folder_name:
                            destination_path = os.path.join(os.getcwd(), "resource_packs", folder_name[:-9])
                            if not os.path.exists(destination_path):
                                os.mkdir(destination_path)
                            shutil.move(shortcut_path, destination_path)
    
                # Display a success message in the console
                print("Folders processed successfully!")
            except Exception as e:
                # Display an error message in the console
                print(f"An error occurred: {e}")
        window["folders"].update(values=get_addons_folders())
    # Close the GUI window
    window.close()