"""

* tile Visit Any Page Module
* author Mingyang

"""
from selenium import webdriver
import time


def execute(args, driver=None):
    """
    This module will use a specific searching engine to search certain keyword using the driver given.

    :param args: dict of mandantory and optional arguments used.
                 engine: searching engine used, support: Google, Bing
                 keyword: keyword to search
    :return res: the web page content of the searching result.
    """

    if driver is None:
        driver = webdriver.Firefox(executable_path='./geckodriver-v0.23.0-linux64/geckodriver')

    print("checkpoint2")

    for c in range(2):
        try:
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

            # TODO logic need to be refined
            time.sleep(5)

            # TODO to be removed, these code will click a result link
            # # searches for elements with class g (google's search results) or other search result classes or ids
            # search_results = driver\
            #     .find_elements_by_xpath("//div[@class='g'] | //li[@class='b_algo'] | //div[@id='links']/child::*")
            # most_relevant = search_results[index].find_element_by_xpath(".//a")
            # most_relevant.click()
            # return driver.current_url

            res = driver.page_source

            driver.close()
            return res

        except Exception as e:
            if c == 0:
                print("Error occured: \"" + str(e) + "\" Retrying one more time.")
            else:
                print("Error occured: \"" + str(e) + "\" Skipping to next command.")
                return ""
