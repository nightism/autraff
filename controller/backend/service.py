from flask import Flask
import os

app = Flask(__name__)

def run_service():
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/autraffdata.db')

    from db_schema import db, ma
    db.init_app(app)
    ma.init_app(app)

    from db_api import db_api
    from control_api import control_api

    app.register_blueprint(db_api)
    app.register_blueprint(control_api)

    app.run(debug=True)


def init_backend_db(clients, jobs):
    from db_schema import db
    from db_schema import Client, ClientSchema
    from db_schema import Job, JobSchema

    Client.query().delete()
    Job.query().delete()

    for client in clients:
        ip = client['ip']
        system = client['system']
        version = client['version']
        new_client = Client(ip, system, version)
        # db.session.add(new_client)
        # db.session.commit()

    for job in jobs:
        name = job['name']
        client = job['client']
        module = job['module']
        interval = int(job['interval'])
        args = str(job['args'])
        print(args)
