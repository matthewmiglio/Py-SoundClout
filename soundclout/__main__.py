from selenium import webdriver
from concurrent.futures import ThreadPoolExecutor
import random
import credentials
from client_interaction import (
    find_play_button_elements,
    get_to_webpage,
    scroll_to_bottom,
)
from utils.chrome_driver import make_chrome_driver, make_chrome_options
import time
import utils.admin_check
from utils.logger import Logger

import time
import webbrowser
from queue import Queue

import PySimpleGUI as sg
from utils.caching import read_user_settings
from utils.caching import check_user_settings
from utils.caching import cache_user_settings
from interface import user_config_keys, disable_keys, main_layout, show_help_gui
from utils.thread import StoppableThread, ThreadKilled
from utils.logger import Logger

logger = Logger()


def save_current_settings(values):
    # read the currently selected values for each key in user_config_keys
    user_settings = {key: values[key] for key in user_config_keys if key in values}
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
            window[stat].update(val)  # type: ignore


def no_jobs_popup():
    sg.popup("Please enter your message:", "Message Box")


def start_button_event(logger: Logger, window, values):
    # check for invalid inputs

    logger.log("Starting")

    for key in disable_keys:
        window[key].update(disabled=True)

    # unpack job list
    count = values['driver_count']
    # if values["bitcoin_checkbox"]:
    #     jobs.append("Bitcoin")

    thread = WorkerThread(logger, count)
    thread.start()

    # enable the stop button after the thread is started
    window["Stop"].update(disabled=False)

    return thread


def stop_button_event(logger: Logger, window, thread):
    logger.log("Stopping")
    window["Stop"].update(disabled=True)
    shutdown_thread(thread, kill=True)  # send the shutdown flag to the thread


class WorkerThread(StoppableThread):
    def __init__(self, logger: Logger, args):
        super().__init__(args)
        self.logger = logger

    def run(self):
        try:
            print(self.args)

            # unpack args for main
            count = self.args
            print(count)
            # CODE TO RUN HERE
            main(count)

        except ThreadKilled:
            return

        except Exception as exc:  # pylint: disable=broad-except
            # catch exceptions and log to not crash the main thread
            self.logger.error(str(exc))


def spam_one_play(driver, thread_index):
    logger.log("in main")

    logger.update_driver_state(driver_index=thread_index, new_state="Starting")

    success = False

    # make driver objects
    link = credentials.get_link_from_file()

    logger.log(f"Driver #{thread_index}: getting to webpages")
    get_to_webpage(driver, link)
    time.sleep(5)

    logger.log(f"Driver #{thread_index}: scrolling to bottom")
    for _ in range(5):
        scroll_to_bottom(driver)
        time.sleep(0.5)

    time.sleep(5)

    logger.log(f"Driver #{thread_index}: finding elements on pages")
    d1_elements = find_play_button_elements(driver)

    while 1:
        start_time = time.time()
        try:
            time_taken = time.time() - start_time
            if time_taken > 5:
                logger.log(f"Driver #{thread_index}: Took too long to find element")
                break

            d1_random_element = random.choice(d1_elements)
            d1_random_element.click()
            logger.log(f"Driver #{thread_index}: Clicked play button")

            logger.add_play(thread_index)

            success = True
            break
        except:
            pass

    if success:
        logger.update_driver_state(driver_index=thread_index, new_state="Listening")
        time.sleep(34)
        logger.update_driver_state(driver_index=thread_index, new_state="Success")

    else:
        logger.update_driver_state(driver_index=thread_index, new_state="Failed")


def main(thread_count):
    chrome_options = make_chrome_options()
    # use pools to load the pages, and get the durations
    while 1:
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            durations = list(
                executor.map(
                    spam_one_play,
                    [webdriver.Chrome(options=chrome_options) for _ in range(thread_count)],
                    range(thread_count),
                )
            )


def gui_main():
    # orientate_terminal()

    thread: WorkerThread | None = None
    comm_queue: Queue[dict[str, str | int]] = Queue()
    logger = Logger(comm_queue, timed=False)  # dont time the inital logger

    # window layout
    window = sg.Window("Py-TarkBot", main_layout)

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
            thread = start_button_event(logger, window, values)

        elif event == "Stop":
            stop_button_event(logger, window, thread)

        elif event == "Help":
            show_help_gui()

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
