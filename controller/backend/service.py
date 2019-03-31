from flask import Flask
import os
import datetime


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(basedir, 'database/autraffdata.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_dir


def run_service():

    from db_schema import db, ma
    db.init_app(app)
    ma.init_app(app)

    from db_api import db_api
    from control_api import control_api

    app.register_blueprint(db_api)
    app.register_blueprint(control_api)

    app.run(debug=True)


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
        client = job['client']
        module = job['module']
        interval = str(int(job['interval']))
        start = job.get('start')
        args = str(job['args'])

        if start is None:
            start = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(args)
        c.execute('INSERT INTO Job (name, module, client, interval, start, arguments) VALUES ("' +
                  name + '", "' + module + '", "' + client + '", ' + interval + ', "' + start + '", "' + args + '")')

    conn.commit()
    print('[Service DB] database re-initiated.')
    conn.close()
