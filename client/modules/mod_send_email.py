import smtplib

from util.log.module_logger import log_module_execution
from util.log.general_logger import logger

# TODO
# from modules.mod_click_searching_result import execute as mod_click_searching_result
# from modules.mod_human_web_browsing import execute as mod_human_web_browsing
# from modules.mod_search_keyword import execute as mod_search_keyword
# from modules.mod_visit_any_page import execute as mod_visit_any_page


@log_module_execution(__name__)
def execute(args, driver=None):

    try:
        print('test1')

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()

        # Next, log in to the server
        print(server.login("sun.mingyang.shawn@gmail.com", "19961025@Smy"))

        sent_from = "sun.mingyang.shawn@gmail.com"
        to = args.get('to')
        subject = str(args.get('subject'))
        body = str(args.get('body'))

        email_text = """\
        From: %s  
        To: %s  
        Subject: %s
    
        %s
        """ % (sent_from, ", ".join(to), subject, body)

        print(server.sendmail("sun.mingyang.shawn@gmail.com", "shawn961025@gmail.com", body))
        print(args)

        success = args.get('success')
        if success is not None:
            success = args.get('success').get('module')
            success_args = args.get('success').get('arguments')
            # eval("from modules import " + success)
            from util.helper import execute_mod
            execute_mod(success, success_args, driver)
            # success = eval(success)
            # success(success_args, driver=driver)

    except Exception as e:
        print("Error occurred: \"" + str(e))
        logger("Error occurred: \"" + str(e), header="[MODULE:SEND_EMAIL]")
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
