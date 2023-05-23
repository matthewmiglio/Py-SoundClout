import os
import PySimpleGUI as sg




# method to get appdata directory
def get_appdata_dir():
    return os.environ["APPDATA"]


# method to make a file called py-soundclout in the appdata directory
def make_soundclout_folder():
    appdata_dir = get_appdata_dir()
    file_path = os.path.join(appdata_dir, "Py-SoundClout")
    print(f"Made SoundClout folder at [{file_path}]")
    os.mkdir(file_path)
    return file_path


# method to checck if the Py-SoundClout file exists in the appdata directory
def check_if_soundclout_folder_exists():
    appdata_dir = get_appdata_dir()
    file_path = os.path.join(appdata_dir, "Py-SoundClout")
    return os.path.exists(file_path)


# method to make a file called soundcloud_link.txt in the Py-SoundClout file
def make_link_file():
    appdata_dir = get_appdata_dir()
    file_path = os.path.join(appdata_dir, "Py-SoundClout", "soundcloud_link.txt")
    print(f"Made SoundClout Link File at [{file_path}]")
    file = open(file_path, "w+")
    file.write("https://soundcloud.com/mattproduction")
    return file_path


# method to check if the soundcloud_link.txt file exists in the Py-SoundClout file
def check_if_link_file_exists():
    appdata_dir = get_appdata_dir()
    file_path = os.path.join(appdata_dir, "Py-SoundClout", "soundcloud_link.txt")
    return os.path.exists(file_path)


# method to get the first line from the soundcloud_link.txt file
def get_link_from_file():
    appdata_dir = get_appdata_dir()
    file_path = os.path.join(appdata_dir, "Py-SoundClout", "soundcloud_link.txt")
    file = open(file_path, "r")
    return file.readline()


def show_missing_creds_gui(directory):
    THEME = "SystemDefaultForReal"
    out_text = (f"You must put your soundcloud profile link in the file at {directory}")

    sg.theme(THEME)
    layout = [
        [sg.Text(out_text)],
    ]
    window = sg.Window("Py-TarkBot", layout)
    while True:
        read = window.read()
        event, _ = read or (None, None)
        if event in [sg.WIN_CLOSED, "Exit"]:
            break
    window.close()


if not check_if_soundclout_folder_exists():
    make_soundclout_folder()

if not check_if_link_file_exists():
    path = make_link_file()
    show_missing_creds_gui(path)
