import PySimpleGUI as sg

from .theme import THEME

sg.theme(THEME)


def stat_box(stat_name: str, size=(5, 1), background_color="white"):
    return sg.Text(
        "0",
        key=stat_name,
        relief=sg.RELIEF_SUNKEN,
        text_color="blue",
        size=size,
        background_color=background_color,
    )


stats_title = [
    [
        [
            sg.Text("Driver 1 plays: "),
        ],
        [
            sg.Text("Driver 2 plays: "),
        ],
        [
            sg.Text("Driver 3 plays: "),
        ],
        [
            sg.Text("Driver 4 plays: "),
        ],
        [
            sg.Text("Driver 5 plays: "),
        ],
        [
            sg.Text("Driver 6 plays: "),
        ],
        [
            sg.Text("Driver 7 plays: "),
        ],
        [
            sg.Text("Driver 8 plays: "),
        ],
    ],
    [
        [
            sg.Text("Driver 9 plays"),
        ],
        [
            sg.Text("Driver 10 plays"),
        ],
        [
            sg.Text("Driver 11 plays"),
        ],
        [
            sg.Text("Driver 12 plays"),
        ],
        [
            sg.Text("Driver 13 plays"),
        ],
        [
            sg.Text("Driver 14 plays"),
        ],
        [
            sg.Text("Driver 15 plays"),
        ],
        [
            sg.Text("Total Plays"),
        ],
    ],
]


stats_values = [
    [
        [
            stat_box("driver_1_plays"),
        ],
        [
            stat_box("driver_2_plays"),
        ],
        [
            stat_box("driver_3_plays"),
        ],
        [
            stat_box("driver_4_plays"),
        ],
        [
            stat_box("driver_5_plays"),
        ],
        [
            stat_box("driver_6_plays"),
        ],
        [
            stat_box("driver_7_plays"),
        ],
        [
            stat_box("driver_8_plays"),
        ],
    ],
    [
        [
            stat_box("driver_9_plays"),
        ],
        [
            stat_box("driver_10_plays"),
        ],
        [
            stat_box("driver_11_plays"),
        ],
        [
            stat_box("driver_12_plays"),
        ],
        [
            stat_box("driver_13_plays"),
        ],
        [
            stat_box("driver_14_plays"),
        ],
        [
            stat_box("driver_15_plays"),
        ],
        [
            stat_box("total_plays"),
        ],
    ],
]

stats = [
    [
        sg.Column(stats_title[0], element_justification="right"),
        sg.Column(stats_values[0], element_justification="left"),
        sg.Column(stats_title[1], element_justification="right"),
        sg.Column(stats_values[1], element_justification="left"),
    ]
]
