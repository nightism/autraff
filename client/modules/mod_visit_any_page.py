"""

* title Visit Any Page Module
* author Mingyang

"""

from util.util import get_driver
from util.util import close_driver
from util.util import stay


def execute(args, driver=None):
    """
    This module will visit the specified web page using the driver given.

    :param args: dict of mandantory and optional arguments used.
                 url: the page that is going to be visited
                 (optional) time: the time remaining on this page
                 <example> {
                                url: "http://www.bbc.com",
                                time: '10',
                            }
    :param driver: (optional) selenium driver used
    :return res: the web page content of the searching result.
    """

    try:
        driver, is_stand_alone = get_driver(driver)

        driver.get(args['url'])
        res = driver.page_source

        if 'time' in dict:
            stay(dict['time'])
        else:
            stay()

        return close_driver(is_stand_alone, driver)

    except Exception as e:
        print("Error occured: \"" + str(e))
        raise e
