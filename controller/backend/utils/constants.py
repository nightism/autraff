import os

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database/autraffdata.db')

NAMESERVER_ADDRESS = '127.0.0.1:26000'

CONTROLLER_ALIAS = 'controller'

CLIENT_PREFIX = 'client-'
COMMUNICATION_CHANNEL = 'request_addr'
CONNECTION_SUFFIX = '_tcp_channel'

COMMAND_SCHEDULE_TASK = 'schedule_task'
COMMAND_DELETE_TASK = 'delete_task'
COMMAND_GET_USAGE_LOG = 'get_usage_log'
COMMAND_GET_DRIVER_LOG = 'get_driver_log'
