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
    This module will use a specific searching engine to search certain keyword using the driver given.

    :param args: dict of mandantory and optional arguments used.
                 engine: searching engine used, support: Google, Bing
                 keyword: keyword to search
    :return res: the web page content of the searching result.
    """