#encoding:utf-8--
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from matplotlib.font_manager import FontProperties#中文处理
class DEALING():
#采用另一种连接方式：
    def connect(self):
        config={
            'host':'localhost',
            'port':3306,
            'user':'muwenlong',
            'password':'12345678',
            'db':'weibofile',
            'charset':'utf8mb4',
        }
        db=pymysql.connect(**config)
        sql_1="select `user id`,`weibo support`,`weibo transpound`,`weibo comment`,`weibo keyword`,`weibo content` from `weibo` ORDER BY `weibo support` DESC LIMIT 50"
        sql_2="select `user id`,`weibo support`,`weibo transpound`,`weibo comment`,`user name`,`weibo keyword`,`send date`,`weibo content` from `weibo` WHERE `weibo support`>=100000 OR `weibo transpound`>=100000 OR `weibo comment`>=100000"
        sql_3 = "select * from `weibo`"
        sql_7 = "select * from `weibo` WHERE `send date` LIKE '9月2%' OR `send date` LIKE '10月%'"
        sql_4="select * FROM `WEIBO` ORDER BY `weibo support` DESC  LIMIT 1"
        sql_5="select * FROM `WEIBO` ORDER BY `weibo transpound` DESC  LIMIT 1"
        sql_6 = "select * FROM `WEIBO` ORDER BY `weibo comment` DESC  LIMIT 1"
        data=pd.read_sql(sql_2,db)
        data1=pd.read_sql(sql_3,db)
        data2=pd.read_sql(sql_4,db)
        data3 = pd.read_sql(sql_5, db)
        data4 = pd.read_sql(sql_6, db)
        data5=pd.read_sql(sql_7,db)
        return data,data1,data2,data3,data4,data5
    def Chinese(self,lables):#保证表中的文字是中文，不是看不懂的方块
        font=FontProperties(fname=r'c:\windows\fonts\simsun.ttc',size=10)
        for lable in lables:
            lable.set_fontproperties(font)
    def deal_pandas(self):
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('max_colwidth', 100)
    def makemaps(self,title,data,choose):
        self.deal_pandas()
        plt.Figure()
        filename=str(title+'.png')
        if choose==1:#为1画柱状图（昵称），为2画折线图（日期），为3画柱状图（热词）
            data=data.plot(kind='bar',align = 'center',title=title,color=["g", "r"])
        elif choose==2:
            data = data.plot(kind='line', title=title,color='b', style='--')
        elif choose==3:
            data=data.plot(kind='bar',title=title,color=["blue","red","yellow","purple"])
        lables=data.get_xticklabels()+data.legend().texts+[data.title]#中文处理
        self.Chinese(lables)
        plt.tight_layout()#防止横坐标或者标签显示不全
        plt.savefig(filename,dpi=600)#像素
        plt.show()
    def getusername_map_csv(self):
        data=self.connect()[0]
        groupData=data['user id'].groupby(data['user name']).count()
        groupData = groupData.sort_values(ascending=False)
        self.makemaps('热门博主分布柱状图(微博热度超十万)',groupData,1)
        groupData.to_csv('weiboUserName.csv', encoding='utf8', header=True)
    def getsenddate_map_csv(self):
        data=self.connect()[1]
        groupData=data['user id'].groupby(data['send date']).count()
        self.makemaps('国庆热度变化折线图（日期）',groupData,2)
        groupData.to_csv('weiboSendDate.csv', encoding='utf8', header=True)
    def gettopic_map_csv(self):
        data=self.connect()[1]
        print(data)
        groupData = data['user id'].groupby(data['weibo keyword']).count()
        groupData = groupData.sort_values(ascending=False)
        self.makemaps('国庆热词占比柱状图',groupData,3)
        groupData.to_csv('weiboKeyWords.csv', encoding='utf8', header=True)
    def get_general_username_map_csv(self):
        self.deal_pandas()
        data=self.connect()[1]
        groupData = data['user id'].groupby(data['user name']).count()
        groupData=groupData.sort_values(ascending=False)#按降序排序
        groupData=groupData.head(20)
        self.makemaps('微博博主柱状图(按微博发帖数)', groupData, 1)
        groupData.to_csv('weiboUserName_general.csv', encoding='utf8', header=True)
    def max_csv(self):
        for i in range(2,5):
            self.deal_pandas()
            data=self.connect()[i]
            data.to_csv('max.csv', mode='a',encoding='utf8', header=True)
    def start(self):
        self.get_general_username_map_csv()
        self.getusername_map_csv()
        self.getsenddate_map_csv()
        self.gettopic_map_csv()
        self.max_csv()
d=DEALING()
d.start()