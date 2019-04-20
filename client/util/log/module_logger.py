from functools import wraps

import datetime

from util.constants import LOG_DIR


def log_module_execution(module_name, logfile=LOG_DIR+'log.txt'):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            current_time = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
            log_string = current_time + "[Modules]" + module_name + " was called"
            print(log_string)
            # Open the logfile and append
            with open(logfile, 'a') as opened_file:
                # Now we log to the specified logfile
                opened_file.write(log_string + '\n')
            return func(*args, **kwargs)
        return wrapped_function
    return logging_decorator
