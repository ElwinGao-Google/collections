#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Elwin.Gao
# Created Time : Thu Sep 11 16:11:01 2025
# File Name: fastapi_server.py
# Description: https://fastapi.tiangolo.com/zh/tutorial/
# Dependencies:
#   pip install fastapi
#   pip install uvicorn
"""

import json
import uvicorn
from fastapi import FastAPI, APIRouter, Request
from db import db, User

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello, World!'}

# CRUD 操作
api_router = APIRouter()

# curl -X POST -H "Content-Type: application/json" -d '{"name": "ZhangSan", "age": "2025-01-01"}' http://localhost:8080/api/v1/user
@api_router.post('/user')
def create_user():
    user = User(name=Request.json.get('name'), age=Request.json.get('age'))
    user.save()
    print(user.to_dict())
    return json.dumps(user.to_dict())

# curl -X GET http://localhost:8080/api/v1/user/1
@api_router.get('/user/{user_id}')
def get_user(user_id: int):
    print("debug:", user_id)
    return json.dumps(User.get(User.id == user_id).to_dict())

# curl -X PUT -H "Content-Type: application/json" -d '{"name": "LiSi", "age": "2025-02-02"}' http://localhost:8080/api/v1/user/1
@api_router.put('/user/{user_id}')
def update_user(user_id: int):
    User.update(name=Request.json.get('name'), age=Request.json.get('age')).where(User.id == user_id).execute()
    return json.dumps(User.get(User.id == user_id).to_dict())

# curl -X DELETE http://localhost:8080/api/v1/user/1
@api_router.delete('/user/{user_id}')
def delete_user(user_id: int):
    User.delete().where(User.id == user_id).execute()
    return json.dumps({'message': 'User deleted successfully', 'user_id': user_id})

# curl -X GET http://localhost:8080/api/v1/users
@api_router.get('/users')
def get_users():
    return list(User.select().dicts())

app.include_router(api_router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8080)
