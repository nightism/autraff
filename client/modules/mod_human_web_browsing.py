"""

* title
* author Mingyang

"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.util import get_driver
from util.util import close_driver
from util.selenium_operations import extract_page_content


from modules.mod_search_keyword import execute as search_keyword
from modules.mod_visit_any_page import execute as visit_page
from modules.mod_click_searching_result import execute as click_result


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
        driver, is_stand_alone = get_driver(driver)

        # get args from dict
        starting_url = args.get('url')
        keyword = args['keyword']

        # initialize starting page
        current_page = None
        if starting_url is None:
            current_page = search_keyword({
                'keyword': keyword,
                'engine': 'Google',  # TODO default searching engine
                'time': '1',
            }, driver)
            current_page = click_result({'n': 0}, driver=current_page)
        else:
            current_page = visit_page({
                'url': starting_url,
                'time': '1',
            }, driver)

        extract_page_content(current_page)

        # total time of browsing
        total_staying_time = int(args['time'])

        # start browsing the web
        while total_staying_time != 0:
            # Compute interest of current page theme
            # Obtain staying time
            # Computer theme closeness and visibility closeness for every page linking
            # Computer possibility for every linking
            # Go to the link with the highest likelihood

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







