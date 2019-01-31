"""

* tile Visit Any Page Module
* author Mingyang

"""

from selenium import webdriver


def execute(args, driver=None):
    """
    This module will visit the specified web page using the driver given.

    :param args: dict of mandantory and optional arguments used.
                 url: the page that is going to be visited
    :param driver: (optional) selenium driver used
    :return res: the web page content of the searching result.
    """

    # TODO logic need to be redefined
    if driver is None:
        driver = webdriver.Firefox(executable_path='./geckodriver-v0.23.0-linux64/geckodriver')

    try:
        driver.get(args['url'])
        res = driver.page_source
        return res

    except Exception as e:
        print("Error occured: \"" + str(e))
