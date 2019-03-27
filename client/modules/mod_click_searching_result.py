"""

* title Click a searching result
* author Mingyang

"""

from util.util import stay
from util.selenium_operations import SELECT_LINK_OPEN_IN_NEW_TAB


def execute(args, driver=None):
    """
    This module will click a link in the searching result, cannot be used standalone

    :param args: dict of mandantory and optional arguments used.
                 (optional) n: the n-th result will be clicked
                 (optional) time: the time remaining on the page
    :param driver: selenium driver used
    :return res: the web page content of the selected page.
    """
    try:
        if driver is None:
            return driver

        staying_time = args.get('time')
        n = args.get('n')

        if n is None:
            n = '0'

        n = int(n)

        search_results = driver \
            .find_elements_by_xpath("//div[@class='g'] | //li[@class='b_algo'] | //div[@id='links']/child::*")
        most_relevant = search_results[n].find_element_by_xpath(".//a")
        most_relevant.click()
        # most_relevant.send_keys(SELECT_LINK_OPEN_IN_NEW_TAB)  # open page in a new tab

        stay(staying_time)

        return driver

    except Exception as e:
        print("Error occured: \"" + str(e) + "\" Skipping to next command.")
        raise e
