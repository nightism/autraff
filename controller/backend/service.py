from flask import Flask
import os
import datetime


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(basedir, 'database/autraffdata.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_dir


def convert_none_to_empty_str(obj):
    if obj is None:
        return ""
    else:
        return str(obj)


def run_service():

    from database.db_schema import db, ma
    db.init_app(app)
    ma.init_app(app)

    from api import root_api
    root_api.init_app(app)

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

    # print(jobs)

    print('[Service DB] inserting new jobs information.')
    for job in jobs:
        name = job['name']
        module = job['module']
        client = job['client']

        success = convert_none_to_empty_str(job.get('success'))
        failure = convert_none_to_empty_str(job.get('failure'))

        interval = convert_none_to_empty_str(job.get('interval'))
        args = convert_none_to_empty_str(job.get('args'))
        start = convert_none_to_empty_str(job.get('start'))

        if start == 'now':
            start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = 'INSERT INTO Job (name, module, client, interval, start, arguments, success, failure) VALUES ("' +\
                name + '", "' + module + '", "' + client + '", "' + interval + '", "' + start + '", "' + args + '", "' \
                + success + '", "' + failure + '")'
        c.execute(query)
        print(job)

    conn.commit()
    print('[Service DB] database re-initiated.')
    conn.close()
