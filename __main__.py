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


logger = Logger()


def main(driver, thread_index):
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

def main():
    count = 4
    chrome_options = make_chrome_options()
    # use pools to load the pages, and get the durations
    while 1:
        with ThreadPoolExecutor(max_workers=count) as executor:
            durations = list(
                executor.map(
                    main,
                    [webdriver.Chrome(options=chrome_options) for _ in range(count)],
                    range(count),
                )
            )


main()