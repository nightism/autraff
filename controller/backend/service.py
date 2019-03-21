from flask import Flask
import os


def run_service():
    app = Flask(__name__)

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
