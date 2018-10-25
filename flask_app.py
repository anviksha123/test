# !/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, abort, make_response
from flask_sqlalchemy import SQLAlchemy
# test code
# Postgres Configuration
pg_user = 'pg_user'         #postgres User
pg_pass = 'pg_pass'         #postgres User Password
pg_database = 'database'    #postgres Database Name

# Config ends

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://%s:%s@localhost/%s'%(pg_user, pg_pass, pg_database)
db = SQLAlchemy(app)


class Demo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(120))

    def __init__(self, data):
        self.data = data


@app.route('/')
def index():
    return "Demo Page!"


@app.route('/ping', methods=['GET'])
def get_tasks():
    return jsonify("pong"), 200

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/data/<int:rec_id>', methods=['GET'])
def get_data(rec_id):
    record = Demo.query.filter_by(id=rec_id).first()
    if record:
        return jsonify({ 
                'id': record.id,
                'data': record.data
                }), 200
    return make_response(jsonify({'error': 'Record not found'}), 404)


@app.route('/data', methods=['GET'])
def fetch_data():
    records = Demo.query.all()
    data = []
    for rec in records:
        data.append({
            'id': rec.id,
            'data': rec.data
        })
    return jsonify(data), 201

@app.route('/data', methods=['POST'])
def create_data():
    name = request.json and 'data' in request.json and request.json['data'] or ""
    if name:
        add_data = Demo(name)
        rec = db.session.add(add_data)
        t = db.session.commit()
        return jsonify({
            'id': add_data.id,
            'data':name
        }), 201
    else:
        return make_response(jsonify({'error': 'Expecting key word `data`'}), 406)


if __name__ == '__main__':
    app.run(host='localhost', port=80, debug=True)
