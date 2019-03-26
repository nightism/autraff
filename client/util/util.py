import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .constants import FIREFOX_WEBDRIVER


SELECT_LINK_OPEN_IN_NEW_TAB = Keys.CONTROL + Keys.SHIFT + Keys.RETURN


def stay(staying_time=5):
    """
        stay and sleep for certain amount of time, default value 5 seconds
    """
    if staying_time is None:
        staying_time = 5

    staying_time = int(staying_time)
    time.sleep(staying_time)


def get_driver(driver):
    if driver is None:
        driver = webdriver.Firefox(executable_path=FIREFOX_WEBDRIVER)

    return driver


def close_driver(should_close, driver):
    if should_close:
        res = driver.page_source
        driver.close()
        print("test")
        return res
    else:
        return driver
