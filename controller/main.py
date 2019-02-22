import os
from osbrain import run_agent
from osbrain import run_nameserver

from service import app, db, ma

import db_api, control_api


def main():

    ################################################
    # input()
    # req_addr = ns.proxy('client').addr('request_addr')
    # server.connect(req_addr, 'send_request')

    # while 1:
    #     c = input()
    #     request = None

    #     if c == '1':
    #         request = {
    #             'command': 'schedule_task',
    #             'interval': 5,
    #             'module': 'mod_visit_any_page',
    #             'para': {
    #                 'url': 'https://www.google.com',
    #             }
    #         }
    #     else:
    #         mod_id = input()
    #         request = {
    #             'command': 'delete_task',
    #             'mod_id': mod_id,
    #         }

    #     server.send('send_request', request)
    #     reply = server.recv('send_request')

    #     print(reply)
    ################################################

    # run database api
    # app.run()
    app.run(debug=True)


if __name__ == '__main__':
    main()
