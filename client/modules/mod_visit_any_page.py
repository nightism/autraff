"""

* tile Visit Any Page Module
* author Mingyang

"""

from selenium import webdriver
from ..util.constants import FIREFOX_WEBDRIVER
import time


def execute(args, driver=None):
    """
    This module will visit the specified web page using the driver given.

    :param args: dict of mandantory and optional arguments used.
                 url: the page that is going to be visited
    :param driver: (optional) selenium driver used
    :return res: the web page content of the searching result.
    """

    is_stand_alone = (driver is None)

    if is_stand_alone:
        driver = webdriver.Firefox(executable_path=FIREFOX_WEBDRIVER)

    print('test')

    try:
        driver.get(args['url'])
        res = driver.page_source
        time.sleep(1)

        if is_stand_alone:
            driver.close()
            return res
        else:
            return driver

    except Exception as e:
        print("Error occured: \"" + str(e))