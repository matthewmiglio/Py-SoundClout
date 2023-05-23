import PySimpleGUI as sg

from .stats import stat_box, stats

info_text = (
    """Py-SoundClout is a program for farming your own SoundCloud listen statistics."""
)

instructions_text = """1. \nEnter your SoundCloud username\n\n2. \nThen select a number of concurrent drivers to use (15 is the fastest, but most resource intensive)
"""

# defining various things that r gonna be in the gui.
main_layout = [
    # info box
    [
        sg.Frame(
            layout=[[sg.Text(info_text, size=(35, None))]],
            title="Info",
            relief=sg.RELIEF_SUNKEN,
            expand_x=True,
        ),
    ],
    # directions box
    [
        sg.Frame(
            layout=[[sg.Text(instructions_text, size=(35, None))]],
            title="Directions",
            relief=sg.RELIEF_SUNKEN,
            expand_x=True,
        ),
    ],
    # user input box
    [
        sg.Frame(
            layout=[
                [sg.Text("Select driver count:")],
                [
                    sg.DropDown(
                        list(range(1, 16)), key="driver_count", default_value="1"
                    )
                ],
            ],
            title="Driver Controls",
            relief=sg.RELIEF_SUNKEN,
            expand_x=True,
        )
    ],
    [
        sg.Frame(
            layout=[
                [sg.Text("Your Soundcloud Username:")],
                [
                    sg.Input(
                        key="username_input",
                    )
                ],
            ],
            title="SoundCloud Username",
            relief=sg.RELIEF_SUNKEN,
            expand_x=True,
        )
    ],
    # stats
    [
        sg.Frame(layout=stats, title="Stats", relief=sg.RELIEF_SUNKEN, expand_x=True),
    ],
    # buttons
    [
        sg.Frame(
            layout=[
                [
                    sg.Column(
                        [
                            [
                                sg.Button("Start"),
                                sg.Button("Stop", disabled=True),
                                sg.Checkbox(
                                    text="Auto-start",
                                    key="autostart",
                                    default=False,
                                    enable_events=True,
                                ),
                            ]
                        ],
                        element_justification="left",
                        expand_x=True,
                    ),
                    sg.Column(
                        [
                            [
                                sg.Button("Help"),
                                sg.Button("Issues?", key="issues-link"),
                                sg.Button("Donate"),
                            ]
                        ],
                        element_justification="right",
                        expand_x=True,
                    ),
                ],
            ],
            title="Controls",
            relief=sg.RELIEF_SUNKEN,
            expand_x=True,
        ),
    ],
    [
        stat_box("time_since_start", size=(7, 1)),
        sg.InputText(
            "Idle",
            key="program_status",
            use_readonly_for_disable=True,
            disabled=True,
            text_color="blue",
            expand_x=True,
        ),
    ],
    # https://www.paypal.com/donate/?business=YE72ZEB3KWGVY&no_recurring=0&item_name=Support+my+projects%21&currency_code=USD
]

# a list of all the keys that contain user configuration
# user_config_keys = ["rows_to_target", "remove_offers_timer", "autostart"]
user_config_keys = [
    # "rows_to_target",
    # "remove_offers_timer",
    "autostart",
    "driver_count",
    "username_input",
]

# list of button and checkbox keys to disable when the bot is running
disable_keys = user_config_keys + ["Start"]
