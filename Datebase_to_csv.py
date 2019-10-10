import pandas as pd
import pymysql
class toCsv():

    def connect(self):
        config = {
        'host': 'localhost',
        'port': 3306,
        'user': 'muwenlong',
        'password': '12345678',
        'db': 'weibofile',
        'charset': 'utf8mb4',
    }
        db = pymysql.connect(**config)
        sql_4 = "select * FROM `WEIBO` ORDER BY `weibo support` DESC "
        sql_5 = "select * FROM `WEIBO` ORDER BY `weibo transpound` DESC"
        sql_6 = "select * FROM `WEIBO` ORDER BY `weibo comment` DESC"

        data2 = pd.read_sql(sql_4, db)
        data3 = pd.read_sql(sql_5, db)
        data4 = pd.read_sql(sql_6, db)
        return data2, data3, data4


    def write_csv(self):
        data1= self.connect()[0]
        data1.to_csv('max_support.csv', encoding='utf8', header=True)
        '''data = self.connect()[1]
        data.to_csv('max_transpound.csv', encoding='utf8', header=True)
        data = self.connect()[2]
        data.to_csv('max_comment.csv', encoding='utf8', header=True)'''
        print("success!")
if __name__=='__main__':
    d=toCsv()
    d.write_csv()