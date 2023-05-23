from selenium.webdriver.common.by import By


# method to scroll to the bottom of the page as far as it has loaded
def scroll_to_bottom(driver):
    """method to scroll to the bottom of the page as far as it has loaded

    Args:
        driver (selenium.webdriver.chrome.webdriver.WebDriver): the selenium chrome driver
        logger (logging.Logger): the logger

    Returns:
        None

    """
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def get_to_webpage(driver, url):
    driver.get(url)


def find_play_button_elements(driver):
    element_list = []
    for index in range(0, 100):
        try:
            path = f"/html/body/div[1]/div[2]/div[2]/div/div[4]/div[1]/div/div[2]/div/div[2]/ul/li[{index}]/div/div/div/div[2]/div[1]/div/div/div[1]/a"

            element = driver.find_element(By.XPATH, path)
            element_list.append(element)
        except:
            pass
    return element_list
