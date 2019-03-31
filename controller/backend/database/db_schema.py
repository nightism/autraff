from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


class Client(db.Model):
    __tablename__ = 'Client'
    # TODO Primary key should be a sequence id, refactor in future development
    ip = db.Column(db.String(255), primary_key=True)
    system = db.Column(db.String(255), unique=False)
    version = db.Column(db.String(255), unique=False)

    job = db.relationship('Job', lazy=True, passive_deletes=True)

    def __init__(self, ip, system, version):
        self.ip = ip
        self.system = system
        self.version = version


class ClientSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('ip', 'system', 'version')


class Job(db.Model):
    __tablename__ = 'Job'
    __table_args__ = {'sqlite_autoincrement': True}
    # TODO primary key should be named as 'id' by convention. refactor in future development
    seq = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    module = db.Column(db.String(255))
    client = db.Column(db.String, db.ForeignKey('Client.ip', ondelete='CASCADE'), nullable=False)

    interval = db.Column(db.Integer, nullable=False)
    start = db.Column(db.DateTime, nullable=False)

    # TODO find a more elegant way to store arguments
    arguments = db.Column(db.Text, nullable=True)

    schedule_id = db.Column(db.String, default='')

    def __init__(self, name, module, client, interval, start=datetime.now(), arguments=""):
        self.name = name
        self.module = module
        self.client = client
        self.interval = interval
        self.arguments = arguments
        self.start = start


class JobSchema(ma.Schema):
    class Meta:
        fields = ('seq', 'client', 'name', 'module', 'interval', 'start', 'arguments', 'schedule_id')


# TODO may be deleted in the future
# class Module(db.Model):
#     __tablename__ = 'Module'
#     name = db.Column(db.String(255), primary_key=True)
#     description = db.Column(db.Text)
#     job = db.relationship('Job', lazy=True, passive_deletes=True)
#
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description
#
#
# class ModuleSchema(ma.Schema):
#     class Meta:
#         #Fields to expose
#         fields = ['name', 'description']
#
#
# class Persona(db.Model):
#     __tablename__ = 'Persona'
#     name = db.Column(db.String(255), primary_key=True)
#     engine = db.Column(db.String(255))
#     interest = db.Column(db.Text)
#     account = db.Column(db.Text)
#
#     job = db.relationship('Job', lazy=True)
#
#     def __init__(self, name, engine, interest, account):
#         self.name = name
#         self.engine
#         self.interest = interest
#         self.account = account
#
#
# class PersonaSchema(ma.Schema):
#     class Meta:
#         fields = ('name', 'engine', 'interest', 'account')


