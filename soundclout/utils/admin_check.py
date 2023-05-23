import ctypes
import PySimpleGUI as sg
import os


# method to check if the user is an admin
def isAdmin():
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin


def show_admin_mode_gui():
    THEME = "SystemDefaultForReal"
    out_text = "Program must be ran in admin mode."

    sg.theme(THEME)
    layout = [
        [sg.Text(out_text)],
    ]
    window = sg.Window("Py-SoundClout", layout)
    while True:
        read = window.read()
        event, _ = read or (None, None)
        if event in [sg.WIN_CLOSED, "Exit"]:
            break
    window.close()


if not isAdmin():
    show_admin_mode_gui()
    exit()
