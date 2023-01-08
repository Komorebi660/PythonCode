# ----------------------------------------------------------
# -*- coding: UTF-8 -*-
# Copyright © 2023 Komorebi660 All rights reserved.
# ----------------------------------------------------------
import MySQLdb


class Database():
    __db = None
    __error = None

    def __init__(self) -> None:
        pass

    def __del__(self):
        self.close()

    def login(self, user, passwd, server_addr, dbname):
        #登录数据库
        try:
            self.__db = MySQLdb.connect(server_addr, user, passwd,
                                        dbname, charset="utf8")
        except MySQLdb.Error as e:
            print(e)
            self.__error = e
            self.__db = None

    def execute(self, sql):
        #执行SQL语句
        try:
            cursor = self.__db.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()

            # 解决"commands out of sync"
            more = True
            while more:
                more = cursor.nextset()
            cursor.close()

            self.__db.commit()
            return res
        except MySQLdb.Error as e:
            print(e)
            self.__error = e
            self.__db.rollback()
            return None

    def callproc(self, proc_name, in_params, out_params):
        #调用存储过程
        try:
            cursor = self.__db.cursor()
            cursor.callproc(proc_name, in_params+out_params)
            # 获取结果
            if len(out_params) > 0:
                sql = "SELECT @_%s_%d" % (proc_name, len(in_params))
                for i in range(1, len(out_params)):
                    sql += ", @_%s_%d" % (proc_name, len(in_params)+i)
            cursor.execute(sql)
            res = cursor.fetchall()
            self.__db.commit()
            return res[0][0]  # 假设存储过程只有一个返回值
        except MySQLdb.Error as e:
            print(e)
            self.__error = e
            self.__db.rollback()
            return None

    def close(self):
        if self.__db is not None:
            self.__db.close()

    def getError(self):
        return self.__error

    def isConnected(self):
        return self.__db is not None


if __name__ == "__main__":
    '''测试该类的基础功能'''
    db = Database()
    #登录
    db.login("root", "passwd", "localhost", "test")
    #建表
    db.execute("CREATE TABLE Book (\
                    ID CHAR(8),\
                    _name VARCHAR(10) NOT NULL,\
                    author VARCHAR(10),\
                    price FLOAT,\
                    _status INT DEFAULT 0,\
                    CONSTRAINT PKb PRIMARY KEY (ID),\
                    CONSTRAINT Cons CHECK (_status IN (0 , 1))\
                );")
    db.execute("insert into Book value('b3', 'C++ Primer', 'Stanley', 78.6, 1);")
    #查询数据库中所有表格信息并输出
    tables = db.execute("SHOW TABLES;")
    if tables is not None:
        for table in tables:
            count = db.execute("SELECT count(*) FROM " + table[0])
            print(table[0], count[0][0])
    #删除所有表格
    db.execute("DROP TABLE IF EXISTS Book;")
