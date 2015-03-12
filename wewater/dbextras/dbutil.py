# -*- coding: utf-8 -*-

''' 该模块已被替换
    以下内容是早期版本'''

__author__ = 'coocol'

import MySQLdb
import MySQLdb.cursors

def getMysqlConnection():
    HOST = '127.0.0.1'
    PASSWORD = 'wewater2014'
    PORT = 3306
    USER_NAME = 'jack'
    DB_NAME = 'app_whuwater'
    try:
        conn = MySQLdb.connect(host=HOST,user=USER_NAME,passwd=PASSWORD,port=PORT,cursorclass=MySQLdb.cursors.DictCursor,charset="utf8")
        conn.select_db(DB_NAME)
        return conn
    except:
        return None