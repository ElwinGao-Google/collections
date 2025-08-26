#!/usr/bin/env python
# -*- coding=utf8 -*-
"""
# Author: Elwin.Gao
# Created Time : Tue Aug 26 17:04:05 2025
# File Name: sqlite3.py
# Description: https://docs.python.org/zh-cn/3.13/library/sqlite3.html
"""

import sqlite3

def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(16) NOT NULL,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rate FLOAT(9, 3),
            desc TEXT
        )
    ''')

def delete_table(cursor):
    cursor.execute('DROP TABLE IF EXISTS demo')

def list_tables(cursor):
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
    return cursor.fetchall()

def insert_data(cursor, name, rate):
    cursor.execute('INSERT INTO demo (name, rate) VALUES (?, ?)', (name, rate))

def delete_data(cursor, id):
    cursor.execute('DELETE FROM demo WHERE id = ?', (id,))

def list_data(cursor):
    cursor.execute('SELECT * FROM demo')
    return cursor.fetchall()

def update_data(cursor, id, name, rate):
    cursor.execute('UPDATE demo SET name = ?, rate = ?, time = CURRENT_TIMESTAMP WHERE id = ?', (name, rate, id))

def select_data(cursor, id):
    cursor.execute('SELECT * FROM demo WHERE id = ?', (id,))
    return cursor.fetchall()


if __name__ == '__main__':
    try: 
        with sqlite3.connect('test.db') as connect:
            print('Database connected successfully.')
            cursor = connect.cursor()   # sqlite3.Cursor不支持CMP（上下文管理协议），即不能使用with

            create_table(cursor)
            print('table:', list_tables(cursor))

            # CRUD
            insert_data(cursor, 'n1', 1.0)
            print('datas:', list_data(cursor))
            print('data1:', select_data(cursor, 1))
            update_data(cursor, 1, 'n2', 2.0)
            print('data1:', select_data(cursor, 1))
            delete_data(cursor, 1)
            print('datas:', list_data(cursor))

            delete_table(cursor)
            print('table:', list_tables(cursor))

            cursor.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
