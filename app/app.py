from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime
import os
from datetime import datetime, timedelta
from flask_marshmallow import Marshmallow
import ipaddress
from ipaddress import IPv4Network, IPv4Address, ip_network, ip_address
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

acceptedrequest = 0
blockedrequest = 0

# Path where the database file is stored
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cidrblockapi.db')
app.config['JWT_SECRET_KEY'] = 'super-secret' # Change this IRL
# Initializing the Database
db = SQLAlchemy(app)
# Instantiate Marshmallow
ma = Marshmallow(app)
# Instantiate JWT manager
jwt = JWTManager(app)

# create database
@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


# Distroy database
@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped!')


# Adding initial data
def unicode(param):
    pass


@app.cli.command('db_seed')
def db_seed():
    cidr1 = Cidr(cidr='127.0.0.0/24',
                 ttl=4567,
                 currentts=datetime.now(),
                 expirets=datetime.now() + timedelta(seconds=4567))
    db.session.add(cidr1)
    user1 = Users(email='kennedy@us.com',
                 password='delta123')
    db.session.add(user1)
    db.session.commit()
    print('Database seeded')


@app.route("/", methods=['GET'])
def home():
    return jsonify({'message': 'You have arrived!'}), 200


@app.route("/healthcheck", methods=['GET'])
def health_check():
    inrange = findrange(request.remote_addr)
    if inrange == 0:
        return jsonify({'message': 'Good Health'}), 200
    else:
        return jsonify({'Message': 'Cannot process request'}), 403


@app.route("/stats", methods=['GET'])
def stats():
    inrange = findrange(request.remote_addr)
    if inrange == 0:
        global acceptedrequest
        acceptedrequest = acceptedrequest + 1
        cidr_list = Cidr.query.all()
        num_cidr = len(cidr_list)
        return jsonify({'accepted_request': acceptedrequest, 'blocked_request': blockedrequest,
                        "cidr": num_cidr}), 200
    else:
        return jsonify({'Message': 'Cannot process request'}), 403


@app.route("/block", methods=['POST'])
@jwt_required()
def index():
    if request.is_json:
        inrange = findrange(request.remote_addr)
        if inrange == 0:
            cidr = request.json['cidr']
            ttl = int(request.json['ttl'])
            expirets = datetime.now() + timedelta(seconds=ttl)
            cidr_block = Cidr(cidr=cidr, ttl=ttl, currentts=datetime.now(), expirets=expirets)
            db.session.add(cidr_block)
            db.session.commit()
            return jsonify(message='Requests will be blocked from an IP in CIDR'), 201
        else:
            return jsonify({'Message': 'Cannot process request'}), 403

    else:
        return jsonify(message='JSON format expected!'), 401


@app.route("/register", methods=['POST'])
def register():
    if request.is_json:
        inrange = findrange(request.remote_addr)
        if inrange == 0:
            email = request.json['email']
            password = request.json['password']
            user = Users(email=email, password=password)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return jsonify(message='Email already exists!'), 201
            return jsonify(message='User created successfully'), 201
        else:
            return jsonify({'Message': 'Cannot process request'}), 403
    else:
        return jsonify(message='JSON format expected! '), 401


@app.route("/login", methods=['POST'])
def login():
    if request.is_json:
        inrange = findrange(request.remote_addr)
        if inrange == 0:
            email = request.json['email']
            password = request.json['password']
            test = Users.query.filter_by(email=email, password=password).first()
            if test:
                access_token = create_access_token(identity=email)
                return jsonify(message='login succeeded!', access_token=access_token)
            else:
                return jsonify(message="Bad email or password"), 401
    else:
        return jsonify(message='JSON format expected!'), 401


def findrange(ipadd):
    cidr_list = Cidr.query.all()
    for cidr_block in cidr_list:
        # if IPv4Address(ip) in IPv4Network(cidr_block.cidr):
        if ipaddress.ip_address(ipadd) in ipaddress.ip_network(cidr_block.cidr):
            if cidr_block.expirets >= datetime.now():
                global blockedrequest
                blockedrequest = blockedrequest + 1
                return 1
    global acceptedrequest
    acceptedrequest = acceptedrequest + 1
    return 0


# database models
class Cidr(db.Model):
    __tablename__ = 'cidrblock'
    id = Column(Integer, primary_key=True)
    cidr = Column(String)
    ttl = Column(Integer)
    currentts = Column(DateTime, default=lambda: datetime.now(), nullable=False)
    expirets = Column(DateTime, default=lambda: datetime.now(), nullable=False)


class Users(db.Model):
    __tablename__ = 'userlogin'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)


class CidrSchema(ma.Schema):
    class Meta:
        fields = ('id', 'cidr', 'ttl', 'currentts', 'expirets')


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password')


cidr_schema = CidrSchema(many=True)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='8080')
