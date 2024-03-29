export const API_HOME = 'http://localhost:5000'

export const OPEN_NAMESERVER_CONTROLLER_CONNECTION = API_HOME + '/open-connection'

export const CHECK_NAMESERVER_STATUS = API_HOME + '/nameserver/debug'

export const GET_NAMESERVER_CONTROLLER_INFO = API_HOME + '/controller/status'

export const CONNECT_TO_CLIENT = API_HOME + '/connect'
export const CONNECT_TO_ALL_CLIENTS = CONNECT_TO_CLIENT + '/all'
export const CHECK_CLIENT_CONNECTION_STATUS = CONNECT_TO_CLIENT

export const DB_CLIENT_API = API_HOME + '/client'

export const DB_JOB_API = API_HOME + '/job'
export const DB_UPDATE_JOB_SCHEDULE_ID = DB_JOB_API + '/schedule/'

export const LOG_USAGE_LOG = API_HOME + '/log/usage/'
export const LOG_DRIVER_LOG = API_HOME + '/log/driver/'
