"""

* title
* author Mingyang

"""

import sys
import os
import time
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib.lib_human_web_browsing.page import Page
from lib.lib_human_web_browsing.util import UtilWrapper

from util.util import stay
from util.util import get_driver
from util.util import close_driver
from util.selenium_operations import extract_page_content
from util.util_human_web_browsing.next_page import get_all_clickable_links
from util.util_human_web_browsing.next_page import calculate_link_possibility
from util.util_human_web_browsing.next_page import normalize_link_possibility
from util.util_human_web_browsing.next_page import find_link_in_distribution

from modules.mod_search_keyword import execute as search_keyword
from modules.mod_visit_any_page import execute as visit_page
from modules.mod_click_searching_result import execute as click_result

from selenium.common.exceptions import ElementNotInteractableException


def execute(args, driver=None):
    """
    This module will continue browsing the web within certain amount of time.
    General idea of how the traffic is generated:
        1. start browsing the web with a certain page
        2. Compute interest in the theme of current page
        3. Compute the expected staying time on current page
        4. Compute theme closeness and visibility closeness for every link in the page
        5. Compute and normalize the possibility for clicking each link
        6. Generate a random number and click on a link based on this 'seed'
        7. Repeat from 2 until the total amount of time is reached

    :param args: dict of mandatory and optional arguments used.
                 time: total web browsing time, unit in second (noted that 1h = 3600s)
                 (optional) url: the starting url that we are going to start with
                 (optional) keyword: keyword to be browsed, if the url is not provided, the first searching
                                     result will be the page that we are going to start with, otherwise we will not
                                     make use of this argument
                 (optional) new_theme_interest: initial interest level in a new theme, range from 0 to 1, default: 0.5
                 (optional) interest_peak_time: time point when the theme interest of a particular theme starts to drop
                                                while continuously browsing on this theme, default: 600 s = 10 min
                 (optional) theme_closeness_threshold: threshold to define whether two theme are the same or related,
                                                       range from 0 to 1, default: 0.6
                 (optional) phi_visual_effect: define how significant the visual effect is, range from 0 to 1, noted
                                               that the significance of the theme effect will be defined as
                                               (1 - phi_visual_effect) accordingly
    :param driver: (optional) selenium driver used
    :return res: the web page content of the searching result.
    """

    try:
        driver, is_stand_alone = get_driver(driver)
        # driver.maximize_window()

        # get args from dict
        total_staying_time = int(args['time'])  # total time of browsing

        starting_url = args.get('url')  # for starting page
        keyword = args.get('keyword')   # for starting page

        new_theme_interest = float(args.get('init_interest_level', UtilWrapper.DEFAULT_NEW_THEME_INTEREST))
        interest_peak_time = int(args.get('interest_peak_time', UtilWrapper.DEFAULT_INTEREST_PEAK_TIME))
        theme_closeness_threshold = float(args.get('theme_closeness_threshold',
                                          UtilWrapper.DEFAULT_THEME_CLOSENESS_THRESHOLD))
        phi_visual_effect = float(args.get('phi_visual_effect', UtilWrapper.DEFAULT_PHI_VISUAL_EFFECT))

        util_wrapper = UtilWrapper(total_staying_time,
                                   new_theme_interest=new_theme_interest,
                                   interest_peak_time=interest_peak_time,
                                   theme_closeness_threshold=theme_closeness_threshold,
                                   phi_visual_effect=phi_visual_effect)

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
            # start with a specific page, recommended
            driver = visit_page({
                'url': starting_url,
                'time': '0',
            }, driver)

        time_stamp = time.time()  # mark starting time

        # start simulation of human browsing
        while util_wrapper.remaining_staying_time != 0:
            # TODO buffer
            # Buffer for page loading
            stay(10)

            # record current page information
            title = driver.title
            content = extract_page_content(driver)
            height = driver.execute_script("return document.body.scrollHeight")

            # create page object
            current_page = Page(title, content, height, util_wrapper)

            # calculate remaining staying time on current page
            time_stayed = int(time.time() - time_stamp)
            page_staying_time = max(current_page.staying_time, time_stayed)

            # record theme staying time
            stay(page_staying_time - time_stayed)
            time_stayed = page_staying_time
            util_wrapper.before_proceed_to_next_page(time_stayed)

            # recalibrate the time stamp here
            time_stamp = time.time()

            # retrieve all links on the page
            current_page_links = util_wrapper.get_all_clickable_links_from_driver(driver)
            current_page_links_with_normalized_distribution =\
                util_wrapper.calculate_and_normalize_possibility_for_all_link(current_page, current_page_links)

            # click a link
            while True:
                try:
                    link_to_be_clicked = util_wrapper.get_a_random_link(current_page_links_with_normalized_distribution)

                    link_to_be_clicked['link'].click()
                    break
                except ElementNotInteractableException:
                    # regenerate a random number and try again
                    # TODO may ended up as an infinite loop
                    continue

            # To decide whether we are browsing the same theme
            theme_closeness = link_to_be_clicked['theme_closeness']
            util_wrapper.proceed_to_next_page(theme_closeness, current_page)

        close_driver(is_stand_alone, driver)

    except Exception as e:
        print("Error occurred: \"" + str(e))
        raise e


if __name__ == '__main__':
    # keyword = input()

    execute({
        # 'keyword': input(),
        'url': 'http://www.bbc.com/',
        'time': 100000
    })







