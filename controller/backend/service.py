from flask import Flask
import os
import datetime


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(basedir, 'database/autraffdata.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_dir


def convertNoneToEmptyStr(obj):
    if obj is None:
        return ""
    else:
        return str(obj)


def run_service():

    from database.db_schema import db, ma
    db.init_app(app)
    ma.init_app(app)

    from api.db_api import db_client_api, db_job_api
    from api.control_api import control_api

    app.register_blueprint(db_client_api)
    app.register_blueprint(db_job_api)
    app.register_blueprint(control_api)

    app.run(debug=False)


def init_backend_db(clients, jobs):
    from sqlite3 import connect

    conn = connect(os.path.join(basedir, 'database/autraffdata.db'))
    c = conn.cursor()

    print('[Service DB] cleaning database.')
    c.execute('DELETE FROM Client WHERE 1')
    c.execute('DELETE FROM Job WHERE 1')

    print('[Service DB] inserting new clients information.')
    for client in clients:
        ip = client['ip']
        system = client['system']
        version = client['version']
        c.execute('INSERT INTO Client (ip, system, version) VALUES ("' + ip + '", "' + system + '", "' + version + '")')

    print('[Service DB] inserting new jobs information.')
    for job in jobs:
        name = job['name']
        module = job['module']
        client = job['client']

        success = convertNoneToEmptyStr(job.get('success'))
        failure = convertNoneToEmptyStr(job.get('failure'))

        interval = convertNoneToEmptyStr(job.get('interval'))
        args = convertNoneToEmptyStr(job.get('args'))
        start = convertNoneToEmptyStr(job.get('start'))

        if start == 'now':
            start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # print(args)
        c.execute('INSERT INTO Job (name, module, client, interval, start, arguments, success, failure) VALUES ("' +
                  name + '", "' + module + '", "' + client + '", ' + interval + ', "' + start + '", "' + args + '", "'
                  + success + '", "' + failure + '")')

    conn.commit()
    print('[Service DB] database re-initiated.')
    conn.close()
