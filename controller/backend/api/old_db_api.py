from api.db_client_api import db_api as db_client_api
from api.db_job_api import db_api as db_job_api


# TODO to be deleted in the future
# # endpoint to add module
# @db_api.route("/module", methods=["POST"])
# def add_module():
#     data = json.loads(request.data)
#
#     name = data['name']
#     description = data['description']
#
#     new_module = db_schema.Module(name, description)
#
#     db_schema.db.session.add(new_module)
#     db_schema.db.session.commit()
#
#     resp = module_schema.jsonify(new_module)
#     resp.headers.add('Access-Control-Allow-Origin', '*')
#     return resp
#
#
# # endpoint to show all modules
# @db_api.route("/module", methods=["GET"])
# def get_module():
#     all_modules = db_schema.Module.query.all()
#     result = modules_schema.dump(all_modules)
#
#     resp = jsonify(result.data)
#     resp.headers.add('Access-Control-Allow-Origin', '*')
#     return resp
#
#
# # endpoint to add persona
# @db_api.route("/persona", methods=["POST"])
# def add_persona():
#     data = json.loads(request.data)
#
#     name = data['name']
#     engine = data['engine']
#     interest = []
#     account = dict()
#
#     new_persona = db_schema.Persona(name, engine, interest, account)
#
#     db_schema.db.session.add(new_persona)
#     db_schema.db.session.commit()
#
#     resp = persona_schema.jsonify(new_persona)
#     resp.headers.add('Access-Control-Allow-Origin', '*')
#     return resp
