"""

* title
* author Mingyang

"""

import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.page import Page

from util.util import stay
from util.util import get_driver
from util.util import close_driver
from util.selenium_operations import extract_page_content
from util.util_human_web_browsing.next_page import get_all_clickable_links
from util.util_human_web_browsing.next_page import calculate_link_possibility

from modules.mod_search_keyword import execute as search_keyword
from modules.mod_visit_any_page import execute as visit_page
from modules.mod_click_searching_result import execute as click_result

from selenium.common.exceptions import ElementNotInteractableException


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
        # driver.maximize_window()

        # get args from dict
        starting_url = args.get('url')
        keyword = args.get('keyword')
        total_staying_time = int(args['time'])  # total time of browsing

        # initialize starting page
        if starting_url is None:
            # start with a google search by clicking the first result
            driver = search_keyword({
                'keyword': keyword,
                'engine': 'Google',  # TODO default searching engine
                'time': '0',
            }, driver)
            driver = click_result({'n': 0}, driver=driver)
        else:
            # start with a specific page
            driver = visit_page({
                'url': starting_url,
                'time': '0',
            }, driver)

        theme_staying_time = 0
        prev_page = None
        # mark starting time
        time_stamp = time.time()

        # start simulation of human browsing
        while total_staying_time != 0:
            stay(10)

            # record current page information
            title = driver.title
            content = extract_page_content(driver)
            height = driver.execute_script("return document.body.scrollHeight")

            # create page object
            current_page = Page(title, content, theme_staying_time, prev_page, height)

            # retrieve all links on the page
            current_page_links = get_all_clickable_links(driver)
            current_page_links_possibility = calculate_link_possibility(current_page, current_page_links)

            time_stayed = int(time.time() - time_stamp)
            page_staying_time = max(0, current_page.staying_time - time_stayed)

            # record theme staying time
            stay(page_staying_time)
            time_stayed = max(page_staying_time, time_stayed)
            theme_staying_time = theme_staying_time + time_stayed
            total_staying_time = max(0, total_staying_time - time_stayed)

            # click the most likely link to be clicked
            # TODO if the link is not clickable
            while True:
                try:
                    link_to_be_click = current_page_links_possibility[0]['link']
                    link_text = link_to_be_click.text
                    link_to_be_click.click()
                    break
                except ElementNotInteractableException:
                    current_page_links_possibility.pop(0)
                    continue
                finally:
                    break

            time_stamp = time.time()  # TODO may not record here

            # To decide whether we are browsing the same theme
            theme_closeness = current_page.calculate_theme_closeness(link_text)
            if theme_closeness < 0.6:
                theme_staying_time = 0

            # record previous page
            prev_page = current_page

            # start browsing the web
            # Compute interest of current page theme
            # Obtain staying time
            # Computer theme closeness and visibility closeness for every page linking
            # Computer possibility for every linking
            # Go to the link with the highest likelihood

        close_driver(is_stand_alone, driver)

    except Exception as e:
        print("Error occurred: \"" + str(e))
        raise e


if __name__ == '__main__':
    # keyword = input()

    execute({
        # 'keyword': input(),
        'url': 'http://time.com/section/newsfeed/',
        'time': 100000
    })







