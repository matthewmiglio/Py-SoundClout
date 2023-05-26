import time
import webbrowser
from queue import Queue

import PySimpleGUI as sg

import soundclout.utils.admin_check
from soundclout.interface import (
    disable_keys,
    main_layout,
    show_help_gui,
    user_config_keys,
    driver_keys,
)
from soundclout.spammer import Spammer
from soundclout.utils.caching import (
    cache_user_settings,
    check_user_settings,
    read_user_settings,
)
from soundclout.utils.logger import Logger
from soundclout.utils.thread import StoppableThread, ThreadKilled


def save_current_settings(values):
    # read the currently selected values for each key in user_config_keys
    user_settings = {key: values[key] for key in user_config_keys if key in values}

    print("user_settings", user_settings)
    # cache the user settings
    cache_user_settings(user_settings)


def load_last_settings(window):
    if check_user_settings():
        window.read(timeout=10)  # read the window to edit the layout
        user_settings = read_user_settings()
        if user_settings is not None:
            for key in user_config_keys:
                if key in user_settings:
                    window[key].update(user_settings[key])
        window.refresh()  # refresh the window to update the layout


def shutdown_thread(thread: StoppableThread | None, kill=True):
    if thread is not None:
        thread.shutdown_flag.set()
        if kill:
            thread.kill()


def update_layout(window: sg.Window, logger: Logger):
    # comm_queue: Queue[dict[str, str | int]] = logger.queue
    window["time_since_start"].update(logger.calc_time_since_start())  # type: ignore
    # update the statistics in the gui

    if not logger.queue.empty():
        # read the statistics from the logger
        for stat, val in logger.queue.get().items():
            # print the elements in window to debug
            # print(window.AllKeysDict)

            window[stat].update(val)  # type: ignore

    # change driver colors according to state
    colors = get_driver_colors(logger)
    driver_key_count = 15
    for index in range(driver_key_count):
        window[driver_keys[index]].update(background_color=colors[index])


def get_driver_colors(logger):
    driver_color_list = []
    drivers = [
        logger.driver_1_state,
        logger.driver_2_state,
        logger.driver_3_state,
        logger.driver_4_state,
        logger.driver_5_state,
        logger.driver_6_state,
        logger.driver_7_state,
        logger.driver_8_state,
        logger.driver_9_state,
        logger.driver_10_state,
        logger.driver_11_state,
        logger.driver_12_state,
        logger.driver_13_state,
        logger.driver_14_state,
        logger.driver_15_state,
    ]

    for status in drivers:
        if status == "Failed":
            driver_color_list.append("Red")
        elif status == "Running" or status == "Starting" or status == 'Listening' or status == 'Starting' or status == 'Success' or status == 'listening':
            driver_color_list.append("Green")
        else:
            driver_color_list.append("Grey")

    return driver_color_list


def start_button_event(logger: Logger, spammer, window, values):
    # insert code for checking if user input vars are good

    logger.update_program_status("Starting")

    # disable keys upon program start
    for key in disable_keys:
        window[key].update(disabled=True)

    # # change driver colors according to state
    # colors = get_driver_colors(logger)
    # driver_key_count = 15
    # for index in range(driver_key_count):
    #     window[driver_keys[index]].update(background_color=colors[index])

    # unpack user input vars
    count = values["driver_count"]
    username = values["username_input"]

    # start worker thread using user input vars
    thread = WorkerThread(logger, spammer, [count, username])
    thread.start()

    # enable the stop button after the thread is started
    window["Stop"].update(disabled=False)

    return thread


def stop_button_event(logger: Logger, window, thread):
    logger.update_program_status("Stopping")
    window["Stop"].update(disabled=True)
    shutdown_thread(thread, kill=True)  # send the shutdown flag to the thread


class WorkerThread(StoppableThread):
    def __init__(self, logger: Logger, spammer: Spammer, args):
        super().__init__(args)
        self.logger = logger
        self.spammer = spammer

    def run(self):
        try:
            self.logger.update_program_status("Running")

            print("args: ", self.args)

            # unpack args for main
            count = self.args[0]
            username = self.args[1]
            print("count", count)
            print("username", username)
            # CODE TO RUN HERE
            self.spammer.spam_main(count, username)

        except ThreadKilled:
            return

        except Exception as exc:  # pylint: disable=broad-except
            # catch exceptions and log to not crash the main thread
            self.logger.error(str(exc))


def gui_main():
    # orientate_terminal()

    thread: WorkerThread | None = None
    comm_queue: Queue[dict[str, str | int]] = Queue()
    logger = Logger(comm_queue, timed=False)  # dont time the inital logger

    # window layout
    window = sg.Window("Py-SoundClout", main_layout)

    load_last_settings(window)

    # start timer for autostart
    start_time = time.time()
    auto_start_time = 30  # seconds
    auto_started = False

    # run the gui
    while True:
        # get gui vars
        read = window.read(timeout=100)
        event, values = read or (None, None)

        # check if bot should be autostarted
        if (
            thread is None
            and values is not None
            and values["autostart"]
            and not auto_started
            and time.time() - start_time > auto_start_time
        ):
            auto_started = True
            event = "Start"

        if event in [sg.WIN_CLOSED, "Exit"]:
            # shut down the thread if it is still running
            shutdown_thread(thread)
            break

        if event == "Start":
            save_current_settings(values)

            # start the bot with new queue and logger
            comm_queue = Queue()
            logger = Logger(comm_queue)
            spammer = Spammer(logger)
            thread = start_button_event(logger, spammer, window, values)

        elif event == "Stop":
            stop_button_event(logger, window, thread)

        elif event == "Help":
            show_help_gui()

        elif event == "issues-link":
            webbrowser.open("https://github.com/matthewmiglio/Py-SoundClout/issues")

        elif event == "Donate":
            webbrowser.open(
                "https://www.paypal.com/donate/"
                + "?business=YE72ZEB3KWGVY"
                + "&no_recurring=0"
                + "&item_name=Support+my+projects%21"
                + "&currency_code=USD"
            )

        # handle when thread is finished
        if thread is not None and not thread.is_alive():
            # enable the start button and configuration after the thread is stopped
            for key in disable_keys:
                window[key].update(disabled=False)
            if thread.logger.errored:
                window["Stop"].update(disabled=True)
            else:
                # reset the communication queue and logger
                comm_queue = Queue()
                logger = Logger(comm_queue, timed=False)
                thread = None

        update_layout(window, logger)

    shutdown_thread(thread, kill=True)

    window.close()


def dummy_main():
    pass


# dummy_main()

if __name__ == "__main__":
    gui_main()
