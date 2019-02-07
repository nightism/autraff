from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'autraffdata.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Client(db.Model):
    __tablename__ = 'Client'
    ip = db.Column(db.String(255), primary_key=True)
    system = db.Column(db.String(255), unique=False)
    version = db.Column(db.String(255), unique=False)

    job = db.relationship('Job', lazy=True)

    def __init__(self, ip, system, version):
        self.ip = ip
        self.system = system
        self.version = version


class ClientSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('ip', 'system', 'version')


class Module(db.Model):
    __tablename__ = 'Module'
    name = db.Column(db.String(255), primary_key=True)

    # TODO what is lazy
    argument = db.relationship('Argument', lazy=True)
    job = db.relationship('Job', lazy=True)

    def __init__(self, name):
        self.name = name


class ModuleSchema(ma.Schema):
    class Meta:
        #Fields to expose
        fields = ['name']


class Argument(db.Model):
    __tablename__ = 'Argument'
    sequence = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    module = db.Column(db.String, db.ForeignKey('Module.name'), nullable=False)

    def __init__(self, sname, description):
        self.name = name
        self.description = description


class ArgumentSchema(ma.Schema):
    class Meta:
        fields = ('name', 'description', 'module')


class Persona(db.Model):
    __tablename__ = 'Persona'
    name = db.Column(db.String(255), primary_key=True)
    interest = db.Column(db.String(255))
    job = db.relationship('Job', lazy=True)

    def __init__(self, name, interest):
        self.name = name
        self.interest = interest


class PersonaSchema(ma.Schema):
    class Meta:
        fields = ('name', 'interest')


class Job(db.Model):
    __tablename__ = 'Job'
    id_ = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    module = db.Column(db.String, db.ForeignKey('Module.name'), nullable=False)
    persona = db.Column(db.String, db.ForeignKey('Persona.name'), nullable=False)
    client = db.Column(db.String, db.ForeignKey('Client.ip'), nullable=False)

    def __init__(self, name, module, persona, client):
        self.name = name
        self.module = module
        self.persona = persona
        self.client = client


class JobSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'module', 'persona', 'client')


if __name__ == '__main__':
    # app.run(debug=True)
    db.create_all()
