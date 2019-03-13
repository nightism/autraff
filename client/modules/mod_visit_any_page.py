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
    :param driver: (optional) selenium driver used
    :return res: the web page content of the searching result.
    """

    try:
        is_stand_alone = (driver is None)
        driver = get_driver(driver)

        driver.get(args['url'])
        res = driver.page_source

        stay(dict.get('time'))

        return close_driver(is_stand_alone, driver)

    except Exception as e:
        print("Error occured: \"" + str(e))
        raise e


if __name__ == '__main__':
    url = input()
    execute({'url': url})
