import time

from selenium import webdriver

from .constants import FIREFOX_WEBDRIVER


def stay(staying_time=5):
    """
        stay and sleep for certain amount of time, default value 5 seconds
    """
    if staying_time is None:
        staying_time = 5

    staying_time = int(staying_time)
    time.sleep(staying_time)


def get_driver(driver):
    stand_alone = driver is None
    if stand_alone:
        driver = webdriver.Firefox(executable_path=FIREFOX_WEBDRIVER)

    return driver, stand_alone


def close_driver(should_close, driver):
    if should_close:
        res = driver.page_source
        driver.close()
        # print("test close_driver")
        return res
    else:
        return driver
