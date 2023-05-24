from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from soundclout.utils.file_cleaning import clean_selenium_files


def make_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=900,900")
    chrome_options.add_argument(
        "--disable-software-rasterizer"
    )  # Disable software rasterizer
    chrome_options.add_argument(
        "--force-device-scale-factor=1"
    )  # Set device scale factor to 1
    chrome_options.add_argument(
        "--disable-background-timer-throttling"
    )  # Disable background timer throttling
    chrome_options.add_argument(
        "--disable-backgrounding-occluded-windows"
    )  # Disable backgrounding of occluded windows
    chrome_options.add_argument(
        "--disable-renderer-backgrounding"
    )  # Disable renderer backgrounding
    # chrome_options.add_argument("--headless")  # make client run in the background
    chrome_options.add_argument("log-level=3")  # don't print useless Selenium stuff
    chrome_options.add_argument("--mute-audio")
    return chrome_options


# method to make a chrome webpage driver object using selenium and chromedriver v1.0.9
def make_chrome_driver():
    clean_selenium_files()

    chrome_options = make_chrome_options()

    return webdriver.Chrome(
        options=chrome_options,
    )
