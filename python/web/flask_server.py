#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Elwin.Gao
# Created Time : Thu Sep 11 15:26:29 2025
# File Name: flask_server.py
# Description: https://flask.palletsprojects.com/en/stable/quickstart/
# Dependencies:
#   pip install flask
# Run:
#   python flask_server.py
"""

from flask import Flask
from flask import Blueprint
from flask import request
from flask import jsonify

from db import db, User

# 全局应用对象
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, World!'

# 创建蓝图对象
api = Blueprint('api', __name__, url_prefix='/api/v1')

# CRUD 操作
# curl -X POST -H "Content-Type: application/json" -d '{"name": "ZhangSan", "age": "2025-01-01"}' http://localhost:8080/api/v1/user
@api.route('/user', methods=['POST'])
def create_user():
    data = request.json
    user = User(name=data.get('name'), age=data.get('age'))
    user.save()
    return jsonify({'message': 'User created successfully', 'user_id': user.id})

# curl -X GET http://localhost:8080/api/v1/user/1
@api.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    return jsonify(User.get(User.id == user_id).to_dict())

# curl -X PUT -H "Content-Type: application/json" -d '{"name": "LiSi", "age": "2025-02-02"}' http://localhost:8080/api/v1/user/1
@api.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    User.update(name=data.get('name')).where(User.id == user_id).execute()
    return jsonify({'message': 'User updated successfully', 'user_id': user_id})

# curl -X DELETE http://localhost:8080/api/v1/user/1
@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    User.delete().where(User.id == user_id).execute()
    return jsonify({'message': 'User deleted successfully', 'user_id': user_id})

# curl -X GET http://localhost:8080/api/v1/users
@api.route('/users', methods=['GET'])
def get_users():
    return jsonify(*User.select().dicts())

app.register_blueprint(api)

if __name__ == '__main__':
    db.create_tables([User])
    app.run(debug=True, host='localhost', port=8080)
