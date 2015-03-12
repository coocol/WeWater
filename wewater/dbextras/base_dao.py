# -*- coding: utf-8 -*-



''' 该模块已被替换
    以下内容是早期版本'''
__author__ = 'coocol'
import dbutil

class DBDao():
    def getAllByProperty(self, table, where_dict):
        conn = dbutil.getMysqlConnection()
        wheresql = []
        for key, value in where_dict.items():
            if isinstance(value, str):
                wheresql.append(key+"="+"'%s'" % value)
            else:
                wheresql.append(key+"="+str(value))
        wheresql = " and ".join(wheresql)
        sql = "select * from %s where %s" % (table, wheresql)
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                cursor.close()
                conn.close()
                return result
            except:
                return None

    def getMoreByProperty(self, table, where_dict):
        conn = dbutil.getMysqlConnection()
        wheresql = []
        for key, value in where_dict.items():
            if isinstance(value, str):
                wheresql.append(key+">"+"'%s'" % value)
            else:
                wheresql.append(key+">"+str(value))
        wheresql = " and ".join(wheresql)
        sql = "select * from %s where %s" % (table, wheresql)
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                cursor.close()
                conn.close()
                return result
            except:
                return None

    def exeRawQuery(self, table, subsql):
        conn = dbutil.getMysqlConnection()
        sql = "select * from %s where %s" % (table, subsql)
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                cursor.close()
                conn.close()
                return result
            except:
                return None

    def getAll(self, table):
        conn = dbutil.getMysqlConnection()
        sql = "select * from %s " % (table)
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                cursor.close()
                conn.close()
                return result
            except:
                return None

    def getId(self, table, where_dict):
        conn = dbutil.getMysqlConnection()
        wheresql = []
        for key, value in where_dict.items():
            if isinstance(value, str):
                wheresql.append(key+"="+"'%s'" % value)
            else:
                wheresql.append(key+"="+str(value))
        wheresql = " and ".join(wheresql)
        sql = "select id from %s where %s" % (table, wheresql)
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                return result["id"]
            except:
                return None


    def update(self, table, values_dict, where_dict):
        conn = dbutil.getMysqlConnection()
        subsql = []
        wheresql = []
        for key, value in values_dict.items():
            if key != "id":
                if isinstance(value, str):
                    subsql.append(key+"="+"'%s'" % value)
                else:
                    subsql.append(key+"="+str(value))

        for key, value in where_dict.items():
            if isinstance(value, str):
                wheresql.append(key+"="+"'%s'" % value)
            else:
                wheresql.append(key+"="+str(value))
        c = ","
        subsql = c.join(subsql)
        wheresql = " and ".join(wheresql)
        sql = "update %s set %s where %s" % (table, subsql ,wheresql)
        if conn is not None:
            try:
                print sql
                cursor = conn.cursor()
                cursor.execute(sql)
                cursor.close()
                conn.commit()
                conn.close()
                return True
            except Exception, e:
                print e.message
                return False


    def add(self, table, values_dict):
        try:
            conn = dbutil.getMysqlConnection()
            print conn
            columns = []
            values = []
            for key, value in values_dict.items():
                if key != "id":
                    columns.append(key)
                    if isinstance(value, unicode):
                        value = value.encode('utf8')
                    values.append(value)
            c = ","

            sql = "insert into %s (%s) values (%s)" % (table, c.join(columns), str(values).replace("[", "").replace("]", ""))
            if conn is not None:
                try:
                    print sql
                    cursor = conn.cursor()
                    res = cursor.execute(sql)
                    cursor.close()
                    conn.commit()
                    conn.close()
                    print True
                except Exception, e:
                    print e.message
        except Exception, e:
            print e.message

    def exists(self, table, where_dict):
        conn = dbutil.getMysqlConnection()
        where_sql = []
        for key, value in where_dict.items():
            if isinstance(value,str):
                value = "'%s'" % value
                print value
            where_sql.append("%s=%s" % (key, value))

        sql = "select * from %s where %s" % (table, " and ".join(where_sql))
        print sql
        res = False
        if conn is not None:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                print result
                if result:
                    res = True
                cursor.close()
                conn.close()
                return res
            except BaseException, e:
                print e.message
                return False

d = DBDao()
print d.exists("admin", {'password': u'123', 'adminname': u'wewater'})