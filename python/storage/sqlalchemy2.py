#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Elwin.Gao
# Created Time : Tue Aug 26 19:11:33 2025
# File Name: sqlalchemy2.py
# Description: https://docs.sqlalchemy.org/en/20/orm/quickstart.html
#              特别注意：sqlalchemy只有在调用flush()或commit()时，才会将数据写入到数据库中，但读请求会优先从本地缓存中获取数据，如果缓存中没有数据，则会从数据库中获取数据。
#                      因此，本示例中，其实大多数情况下，数据都是从本地缓存中获取的，而不是从数据库中获取的。
"""

from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import String
from sqlalchemy import DECIMAL
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy import inspect
from sqlalchemy import text
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete

engine = create_engine('sqlite:///:memory:', echo=False)    # echo=True会打印调试信息

class Base(DeclarativeBase):
    pass

class Demo(Base):
    __tablename__ = 'demo'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(16))
    time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    rate: Mapped[float] = mapped_column(DECIMAL(9, 3))
    desc: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    def __repr__(self):
        return f'Demo(id={self.id}, name={self.name}, rate={self.rate})'

def simple_usage(session):
    # insert单条数据
    session.add(Demo(name='n1', rate=1.0))
    # insert多条数据
    session.add_all([Demo(name='n2', rate=2.0), Demo(name='n3', rate=3.0)])

    # 查询单条数据
    print(session.get(Demo, 1))
    print(session.scalar(select(Demo).filter(Demo.id == 2)))
    print(session.query(Demo).filter(Demo.id == 3).one())   # scalars也可以通过one()获取单条数据

    # 查询多条数据
    print(session.query(Demo).filter(Demo.id > 0).all())
    print(session.scalars(select(Demo).filter(Demo.id > 0)).all())

    # 更新数据
    session.get(Demo, 1).name = 'n9'
    session.get(Demo, 1).rate = 9.0
    session.query(Demo).filter(Demo.id == 2).update({'name': 'n8', 'rate': 8.0})
    session.execute(update(Demo).where(Demo.id == 3).values(name='n7', rate=7.0))
    print(session.query(Demo).filter(Demo.id > 0).all())
    session.bulk_update_mappings(Demo, [{'id': 1, 'name': 'n1', 'rate': 1.0}, {'id': 2, 'name': 'n2', 'rate': 2.0}, {'id': 3, 'name': 'n3', 'rate': 3.0}])
    print(session.query(Demo).filter(Demo.id > 0).all())

    # 删除数据
    session.delete(session.get(Demo, 1))
    session.query(Demo).filter(Demo.id == 2).delete()
    session.execute(delete(Demo).where(Demo.id == 3))
    print(session.query(Demo).filter(Demo.id > 0).all())

if __name__ == '__main__':
    with engine.connect() as conn:  # 即使不进行显式connect，也会自动connect
        print('execute raw sql:', conn.execute(text('SELECT name FROM sqlite_master WHERE type="table"')).fetchall())    # 获取connect对象后，即可执行raw sql

        Base.metadata.create_all(engine)
        print('tables:', inspect(engine).get_table_names())

        # ！！！特别注意！！！
        # 只有在调用commit()时，数据才会真正写入到数据库中，否则数据只是写入到本地缓存中。
        # 因此，上面的写语句的后面，都需要调用commit()，以确保数据正常入库。
        # 但demo中，为了突出重点，所以没有每次写操作都调用一遍commit()
        # 所以，在demo中，虽然一切结果都正常，但其实数据并没有入库，而都只是在操作本地缓存。
        print('show raw sql:', str(select(Demo).filter(Demo.id > 0).compile(compile_kwargs={"literal_binds": True})).replace('\n', ' ')) # 打印sql语句
        with Session(engine) as session:
            print('show raw sql:', str(session.query(Demo).filter(Demo.id > 0).statement.compile(compile_kwargs={"literal_binds": True})).replace('\n', ' '))  # 打印sql语句
            simple_usage(session)
            # 此处通过with语句，隐式调用了commit()

        Base.metadata.drop_all(engine)
        print('tables:', inspect(engine).get_table_names())

