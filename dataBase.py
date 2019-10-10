#encoding:utf-8--
import pymysql
import pandas as pd
import csv
from collections import OrderedDict
class DataBase():
    def connet_database_1(self):
        db=pymysql.connect(host="127.0.0.1",user="muwenlong",password="12345678",charset="utf8mb4")
        cursor=db.cursor()
        return cursor
    def connet_database_2(self):
        db=pymysql.connect(host="127.0.0.1",user="muwenlong",password="12345678",db="weibofile",charset="utf8mb4")
        return db
    '''写完才知道，要是把连接的参数写成字典形式更简单，就不用写两个函数，二次连接db啦，下一个程序尝试写成字典'''

    def createdatabase(self,cursor):#记住这种字符``,esc下面的，否则会出错
        create_database_sql = """create database `WEIBOFILE` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"""

        cursor.execute(create_database_sql)
    def createtable(self,cursor):
        create_table_sql = """
                        CREATE TABLE IF NOT EXISTS `weibo`(
                        `user id` varchar(64),
                        `weibo keyword` varchar(64),
                        `send date` varchar(64),
                        `user name` varchar(64),
                        `weibo support` int,
                        `weibo transpound` int,
                        `weibo comment` int,
                        `weibo content` varchar(4096),
                        PRIMARY KEY(`user id`)
                        )CHARACTER SET UTF8mb4
                        """
        cursor.execute(create_table_sql)
    def prepare_for_mysql(self):
        cursor=self.connet_database_1()
        try:
            self.createdatabase(cursor)
        except:print("the database have already existed or have a error")
        db = self.connet_database_2()
        cursor=db.cursor()
        self.createtable(cursor)
    def read_csv(self,filename):
        with open(filename,'r',encoding="utf8") as f:
            data = list(tuple(rec) for rec in csv.reader(f, delimiter=','))
        return data
    def insert_value(self,filename):
        data=self.read_csv(filename)
        num=0
        for i in range(1,len(data)):
            db = self.connet_database_2()
            cursor=db.cursor()
            num+=1
            insert_sql="REPLACE INTO weibo VALUES"+str(data[i])
            '''
            "INSERT IGNORE INTO weibo VALUES"+str(data[i])忽略重复部分，但会报错
            "REPLACE INTO weibo VALUES"+str(data[i])代替重复部分，不报错
            INSERT INTO weibo VALUES"+str(data[i])报错，不运行
            '''
            cursor.execute(insert_sql)
            db.commit()
        '''insert_sql = "INSERT INTO weibo VALUES(1,22,2,2,2,2,2,2)"
        cursor.execute(insert_sql)
        db.commit()'''
        print("共插入"+str(num)+"条数据")




d=DataBase()
#d.prepare_for_mysql()#仅在第一次运行时使用，可自动在MYSQL建库建表
d.insert_value("data8.csv")#即将导入数据库的csv文件路径



