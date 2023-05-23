import random
import time
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver

from soundclout.client_interaction import (
    find_play_button_elements,
    get_to_webpage,
    scroll_to_bottom,
)
from soundclout.credentials import get_link_from_file
from soundclout.utils.chrome_driver import make_chrome_options
from soundclout.utils.logger import Logger


class Spammer:
    def __init__(self, logger: Logger):
        self.logger: Logger = logger

    def spam_one_play(self, driver, thread_index):
        self.logger.log("in main")

        self.logger.update_driver_state(driver_index=thread_index, new_state="Starting")

        success = False

        # make driver objects
        link = get_link_from_file()

        self.logger.log(f"Driver #{thread_index}: getting to webpages")
        get_to_webpage(driver, link)
        time.sleep(5)

        self.logger.log(f"Driver #{thread_index}: scrolling to bottom")
        for _ in range(5):
            scroll_to_bottom(driver)
            time.sleep(0.5)

        time.sleep(5)

        self.logger.log(f"Driver #{thread_index}: finding elements on pages")
        d1_elements = find_play_button_elements(driver)

        while 1:
            start_time = time.time()
            try:
                time_taken = time.time() - start_time
                if time_taken > 5:
                    self.logger.log(
                        f"Driver #{thread_index}: Took too long to find element"
                    )
                    break

                d1_random_element = random.choice(d1_elements)
                d1_random_element.click()
                self.logger.log(f"Driver #{thread_index}: Clicked play button")

                self.logger.add_play(thread_index)

                success = True
                break
            except:
                pass

        if success:
            self.logger.update_driver_state(
                driver_index=thread_index, new_state="Listening"
            )
            time.sleep(random.randint(35,45))
            self.logger.update_driver_state(
                driver_index=thread_index, new_state="Success"
            )

        else:
            self.logger.update_driver_state(
                driver_index=thread_index, new_state="Failed"
            )

    def spam_main(self, thread_count):
        chrome_options = make_chrome_options()
        # use pools to load the pages, and get the durations
        while 1:
            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                executor.map(
                    self.spam_one_play,
                    [
                        webdriver.Chrome(options=chrome_options)
                        for _ in range(thread_count)
                    ],
                    range(thread_count),
                )
