"""

* title Visit Any Page Module
* author Mingyang

"""

from util.util import get_driver
from util.util import close_driver
from util.util import stay

from util.log.module_logger import log_module_execution
from util.log.general_logger import logger

# TODO
# from modules.mod_send_email import execute as mod_send_email
# from modules.mod_click_searching_result import execute as mod_click_searching_result
# from modules.mod_human_web_browsing import execute as mod_human_web_browsing
# from modules.mod_search_keyword import execute as mod_search_keyword


@log_module_execution(__name__)
def execute(args, driver=None):
    """
    This module will visit the specified web page using the driver given.

    :param args: dict of mandantory and optional arguments used.
                 url: the page that is going to be visited
                 (optional) time: the time remaining on this page
                 <example> {
                                url: "http://www.bbc.com",
                                time: '10',
                            }
    :param driver: (optional) selenium driver used
    :return res: the web page content of the searching result.
    """

    try:
        driver, is_stand_alone = get_driver(driver)

        driver.get(args['url'])
        res = driver.page_source

        if 'time' in args:
            stay(args['time'])
        else:
            stay()

        print(args)

        success = args.get('success')
        if success is not None:
            success = args.get('success').get('module')
            success_args = args.get('success').get('arguments')
            # from modules import mod_send_email
            # eval("from modules import " + success)
            from util.helper import execute_mod
            execute_mod(success, success_args, driver)
            # success = eval(success)
            # success(success_args, driver=driver)

        return close_driver(is_stand_alone, driver)

    except Exception as e:
        print("Error occurred: \"" + str(e))
        logger("Error occurred: \"" + str(e), header="[MODULE:VISIT_ANY_PAGE]")
        failure = args.get('failure')
        if failure is not None:
            failure = args.get('failure').get('module')
            failure_args = args.get('failure').get('arguments')
            # eval("from modules import " + failure)
            from util.helper import execute_mod
            execute_mod(failure, failure_args, driver)
            # failure = eval(failure)
            # failure(failure_args)
        else:
            raise e
