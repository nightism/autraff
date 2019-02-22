from flask import Flask, request, Response, jsonify
import os

from service import app, db, ma


class Client(db.Model):
    __tablename__ = 'Client'
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


class Module(db.Model):
    __tablename__ = 'Module'
    name = db.Column(db.String(255), primary_key=True)
    description = db.Column(db.Text)
    job = db.relationship('Job', lazy=True, passive_deletes=True)

    def __init__(self, name, description):
        self.name = name
        self.description = description


class ModuleSchema(ma.Schema):
    class Meta:
        #Fields to expose
        fields = ['name', 'description']


class Persona(db.Model):
    __tablename__ = 'Persona'
    name = db.Column(db.String(255), primary_key=True)
    engine = db.Column(db.String(255))
    interest = db.Column(db.Text)
    account = db.Column(db.Text)

    job = db.relationship('Job', lazy=True)

    def __init__(self, name, engine, interest, account):
        self.name = name
        self.engine
        self.interest = interest
        self.account = account


class PersonaSchema(ma.Schema):
    class Meta:
        fields = ('name', 'engine', 'interest', 'account')


class Job(db.Model):
    __tablename__ = 'Job'
    __table_args__ = {'sqlite_autoincrement': True}
    seq = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    module = db.Column(db.String, db.ForeignKey('Module.name', ondelete='CASCADE'), nullable=False)
    persona = db.Column(db.String, db.ForeignKey('Persona.name'), nullable=True)
    client = db.Column(db.String, db.ForeignKey('Client.ip', ondelete='CASCADE'), nullable=False)

    interval = db.Column(db.Integer, nullable=False)
    start = db.Column(db.DateTime, nullable=False)

    arguments = db.Column(db.Text, nullable=True)

    schedule_id = db.Column(db.String, default='')

    def __init__(self, name, module, client, interval, start, persona=None, arguments=None):
        self.name = name
        self.module = module
        self.persona = persona
        self.client = client
        self.interval = interval
        self.arguments = arguments
        self.start = start


class JobSchema(ma.Schema):
    class Meta:
        fields = ('seq', 'client', 'name', 'module', 'persona', 'interval', 'start', 'arguments', 'schedule_id')


if __name__ == '__main__': 
    # app.run(debug=True)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()
