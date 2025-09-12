#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Elwin.Gao
# Created Time : Thu Sep 11 16:27:01 2025
# File Name: db.py
# Description:
"""

from peewee import SqliteDatabase
from peewee import Model
from peewee import AutoField
from peewee import CharField
from peewee import DateField

# 模拟存储用户信息
db = SqliteDatabase('test.db')

class User(Model):
    class Meta:
        database = db
        table_name = 'user'
    
    id = AutoField(primary_key=True)
    name = CharField()
    age = DateField()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }
