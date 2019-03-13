"""

* title
* author Mingyang

"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from ..util.constants import FIREFOX_WEBDRIVER
import time

def execute(args, driver=None):
    """
    This module will continue browsing the web within certain amount of time.

    :param args: dict of mandantory and optional arguments used.
                 time: total web browsing time util we start execution, in second, noted that 1h = 3600s
                 (optional) url: the starting url that we are going to start with
                 (optional) keyword: keyword to be browsed, if the url is not provided, the the searching
                 result will be the first page that we are going to start with
    :return res: the web page content of the searching result.
    """

    try:
        is_stand_alone = (driver is None)

        if is_stand_alone:
            driver = webdriver.Firefox(executable_path=FIREFOX_WEBDRIVER)





