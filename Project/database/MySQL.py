import random
import pymysql
from datetime import datetime, timedelta
import config


class MySQL:
    def __init__(self, host, user, passwd, dbName, port):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbName = dbName
        self.port = port

    def connet(self):
        try:
            self.db = pymysql.connect(self.host, self.user, self.passwd, self.dbName, self.port)
            self.cursor = self.db.cursor()
            # print("connect successed!")
        except:
            print("connect failed!")

    def close(self):
        self.cursor.close()
        self.db.close()

    def get_one(self, sql):
        res = None
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except:
            print("get_one Failed")
        return res

    def get_all(self, sql):
        res = None
        try:
            # print("get_all succeed!","sql",sql)
            self.connet()
            # print("sql",sql)
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except:
            # print("get_all Failed","sql",sql)
            print("get_all Failed")
        return res

    def get_all_obj(self, sql, tableName, *args):
        resList = []
        fieldsList = []
        if (len(args) > 0):
            # print(type(args))
            for item in args:
                fieldsList.append(item)
        else:
            fieldsSql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s' order by ordinal_position " % (
            tableName, self.dbName)
            fields = self.get_all(fieldsSql)
            for item in fields:
                fieldsList.append(item[0])
        res = self.get_all(sql)
        if res == None:
            return res
        for item in res:
            obj = {}
            count = 0
            for x in item:
                obj[fieldsList[count]] = x
                count += 1
            resList.append(obj)
        return resList

    def insert(self, sql):
        return self.__edit(sql)

    def update(self, sql):
        return self.__edit(sql)

    def delete(self, sql):
        return self.__edit(sql)

    def __edit(self, sql):
        count = 0
        try:
            self.connet()
            count = self.cursor.execute(sql)
            # print("delete: ",sql)
            self.db.commit()
            self.close()
        except:
            print("Commit Failed")
            self.db.rollback()
        return count

# db = MySQL(config.mysql["host"],config.mysql["user"],config.mysql["passwd"],config.mysql["dbName"],config.mysql["port"])
# sql = "select Serect from Person where Person_id = '1'; INSERT INTO test VALUES ('fasgfa'); "
# res = db.get_all_obj(sql,"Person","Serect")
# print("res",res)
