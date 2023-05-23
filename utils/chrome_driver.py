from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def make_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")  # make client run in background
    chrome_options.add_argument("log-level=3")  # dont print useless selenium stuff
    chrome_options.add_argument("--mute-audio")
    return chrome_options

# method to make a chrome webpage driver object using selenium and chromedriver v1.0.9
def make_chrome_driver():
    chrome_options = make_chrome_options()

    return webdriver.Chrome(
        options=chrome_options,
    )
