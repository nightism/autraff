"""

* title
* author Mingyang

"""

# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.util import get_driver
from util.util import close_driver
from util.util import SELECT_LINK_OPEN_IN_NEW_TAB


from modules.mod_search_keyword import execute as search_keyword
from modules.mod_visit_any_page import execute as visit_page


def execute(args, driver=None):
    """
    This module will continue browsing the web within certain amount of time.

    :param args: dict of mandantory and optional arguments used.
                 time: total web browsing time util we start execution, in second, noted that 1h = 3600s
                 (optional) url: the starting url that we are going to start with
                 (optional) keyword: keyword to be browsed, if the url is not provided, the the searching
                 result will be the first page that we are going to start with
    :param driver: (optional) selenium driver used
    :return res: the web page content of the searching result.
    """

    try:
        is_stand_alone = (driver is None)
        driver = get_driver(driver)

        starting_url = args.get('url')
        keyword = args['keyword']
        starting_page = None
        if starting_url is None:
            starting_page = search_keyword({
                'keyword': keyword,
                'engine': 'Google',
                'time': '1',
            }, driver)
            search_results = driver\
                .find_elements_by_xpath("//div[@class='g'] | //li[@class='b_algo'] | //div[@id='links']/child::*")
            most_relevant = search_results[1].find_element_by_xpath(".//a")
            most_relevant.send_keys(SELECT_LINK_OPEN_IN_NEW_TAB)
        else:
            starting_page = visit_page({
                'url': starting_url,
                'time': '1',
            }, driver)

        staying_time = int(args['time'])

        while staying_time != 0:
            return

        close_driver(is_stand_alone, driver)

    except Exception as e:
        print("Error occured: \"" + str(e))
        raise e


if __name__ == '__main__':
    keyword = input()

    execute({
        'keyword': keyword,
        'time': 10
    })







