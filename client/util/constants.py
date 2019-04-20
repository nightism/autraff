import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FIREFOX_WEBDRIVER = BASE_DIR + '/geckodriver-v0.23.0-linux64/geckodriver'

LOG_DIR = BASE_DIR + '/logs/'
LOG_FILE = LOG_DIR + '/log.log'

# DRIVER_LOG path is fixed, changing the path here will not make the path change of geckodriver.log
DRIVER_LOG = BASE_DIR + '/geckodriver.log'
