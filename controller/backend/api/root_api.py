from api.db_api import *
from api.control_api import control_api


def init_app(app):
    app.register_blueprint(db_client_api.db_api)
    app.register_blueprint(db_job_api.db_api)
    app.register_blueprint(control_api)

    return app
