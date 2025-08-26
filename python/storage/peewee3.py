#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Elwin.Gao
# Created Time : Tue Aug 26 17:04:05 2025
# File Name: peewee.py
# Description: https://peewee.pythonlang.cn/en/latest/index.html
"""

from datetime import datetime
from peewee import Model, SqliteDatabase, AutoField, CharField, IntegerField, DateTimeField, DecimalField, TextField

db = SqliteDatabase(':memory:') # 内存形式，不保存到磁盘

class BaseModel(Model):
    class Meta:
        database = db

class Demo(BaseModel):
    id = AutoField()
    name = CharField(16)
    time = DateTimeField(default=datetime.now)
    rate = DecimalField(max_digits=9, decimal_places=3)
    desc = TextField(null = True)

    def __str__(self):
        return f'Demo(id={self.id}, name={self.name}, time={self.time}, rate={self.rate}, desc={self.desc})'

@db.atomic('IMMEDIATE')
def atomic_usage():
    simple_usage()

def simple_usage():
    db.create_tables([Demo])
    print('tables:', db.get_tables())

    # 创建数据（Upsert形式）
    demo = Demo(name='n1', rate=1.0)
    demo.save() # insert or update

    # 创建数据（Insert形式，单条）
    Demo.insert(name='n2', rate=2.0).execute() # just insert

    # 创建数据（Insert形式，多条）
    Demo.insert_many([
        {'name': 'n3', 'rate': 3.0}
    ]).execute() # just insert

    # 获取原始sql
    print('raw sql:', Demo.select().sql())

    # 查询单条数据（简单形式）
    try:
        demo = Demo.get(Demo.id == 0)   # 省略execute()，和写execute()，是等效的
    except Demo.DoesNotExist:
        print('record not found')
    
    # 查询全部数据（execute形式）
    print(*Demo.select().execute(), sep='\n')

    # 查询全部数据（dicts形式）
    print(*Demo.select().dicts(), sep='\n')

    # 更新数据（upsert形式）
    demo = Demo.get(Demo.id == 1)
    demo.name = 'n9'; demo.rate = 9.0; demo.save() # insert or update
    # 更新数据（update形式）
    demo = Demo.get(Demo.id == 2)
    demo.name = 'n8'; demo.rate = 8.0; demo.update() # just update
    # 更新数据（Where条件形式）
    Demo.update(name='n7', rate=7.0).where(Demo.id == 3).execute() # just update
    print(*Demo.select().execute(), sep='\n')

    # 删除数据
    print('records count:', Demo.select().count())
    demo = Demo.get(Demo.id == 1)
    demo.delete_instance()
    print('records count:', Demo.select().count())
    Demo.delete().where(Demo.id == 3).execute()
    print('records count:', Demo.select().count())

    db.drop_tables([Demo])
    print('tables:', db.get_tables())

if __name__ == '__main__':
    # 隐式连接（默认，不推荐）
    simple_usage() # 简单用法
    print('execute sql:', db.execute_sql("SELECT name FROM sqlite_schema WHERE type = 'table'").fetchall())
    db.close()  # 关闭隐式连接（否则下面的db.connect()会报错）

    # 显示连接
    db.connect()
    with db.atomic('EXCLUSIVE') as transaction:    # 事务用法（with形式）
        simple_usage()
    db.close()

    # 显示连接（with形式）
    with db.connection_context() as connection:
        atomic_usage()  # 事务用法（注解形式）
