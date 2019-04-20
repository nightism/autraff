import datetime

from util.constants import LOG_DIR

LOG_FILE = LOG_DIR + 'log.txt'


def logger(msg, header="[INFO]", logfile=LOG_FILE):
    current_time = "[" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]"
    log_string = current_time + header + msg
    print(log_string)
    with open(logfile, 'a') as opened_file:
        # Now we log to the specified logfile
        opened_file.write(log_string + '\n')


def info_logger(msg, logfile=LOG_FILE):
    logger(msg, header="[INFO]", logfile=logfile)


def warning_logger(msg, logfile=LOG_FILE):
    logger(msg, header="[WARNING]", logfile=logfile)


def error_logger(msg, logfile=LOG_FILE):
    logger(msg, header="[ERROR]", logfile=logfile)
