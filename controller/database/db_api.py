from flask import Flask, request, Response, jsonify
import os


from db_schema import app, Client, ClientSchema


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)


# endpoint to create new client
@app.route("/client", methods=["POST"])
def add_client():
    ip = request.json['ip']
    system = request.json['system']
    version = request.json['version']

    new_client = Client(ip, system, version)

    db.session.add(new_client)
    db.session.commit()

    return ip


# endpoint to show all clients
@app.route("/client", methods=["GET"])
def get_client():
    all_clients = Client.query.all()
    result = clients_schema.dump(all_clients)
    resp = jsonify(result.data)
    resp.headers.add('Access-Control-Allow-Origin', '*')  ## IMPORTANT ##
    return resp


# endpoint to get client detail by ip
@app.route("/client/<ip>", methods=["GET"])
def client_detail(ip):
    client = Client.query.get(ip)
    resp = client_schema.jsonify(client)
    resp.headers.add('Access-Control-Allow-Origin', '*')  ## IMPORTANT ##
    return resp


# # endpoint to update user
# @app.route("/user/<id>", methods=["PUT"])
# def user_update(id):
#     user = User.query.get(id)
#     username = request.json['username']
#     email = request.json['email']

#     user.email = email
#     user.username = username

#     db.session.commit()
#     return user_schema.jsonify(user)


# # endpoint to delete user
# @app.route("/user/<id>", methods=["DELETE"])
# def user_delete(id):
#     user = User.query.get(id)
#     db.session.delete(user)
#     db.session.commit()

#     return user_schema.jsonify(user)


def run():
    app.run(debug=True)


if __name__ == '__main__':
    run()
