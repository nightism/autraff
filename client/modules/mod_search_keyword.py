"""

* title Visit Any Page Module
* author Mingyang

"""

from util.util import get_driver
from util.util import close_driver
from util.util import stay


def execute(args, driver=None):
    """
    This module will use a specific searching engine to search certain keyword using the driver given.

    :param args: dict of mandantory and optional arguments used.
                 engine: searching engine used, support: Google, Bing
                 keyword: keyword to search
                 (optional) time: the time remaining on the searching result
    :param driver: (optional) selenium driver used
    :return res: the web page content of the searching result.
    """

    for counter in range(2):
        try:
            driver, is_stand_alone = get_driver(driver)

            engine = args['engine']
            keyword = args['keyword']
            if engine == 'Google':
                url = 'https://www.google.com'
            elif engine == 'Bing':
                url = 'https://www.bing.com'

            driver.get(url)

            # TODO logic need to be went through again
            # searches for element with class search or gsfi (google's name for sreach field class)
            search_field = driver.find_element_by_xpath("//input[contains(@class, 'search') "
                                                        "or contains(@class, 'gsfi')]")
            search_field.send_keys(keyword)
            # sends Enter key
            search_field.send_keys(u'\ue007')

            stay(args.get('time'))

            return close_driver(is_stand_alone, driver)

        except Exception as e:
            if counter == 0:
                print("Error occured: \"" + str(e) + "\" Retrying one more time.")
            else:
                print("Error occured: \"" + str(e) + "\" Skipping to next command.")
                raise e
