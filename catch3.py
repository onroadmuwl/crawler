#encoding:utf-8--
import requests
from lxml import etree
import re
from collections import OrderedDict
import pandas as pd
import time
from datetime import datetime
import random
from time import sleep
class WEIBO():
    cookie = {
        'Cookie': '_T_WM=52165934645; ALF=1573204852; SCF=ArdMMKY9SBOgWxi4HE1DCrEm8vYkDcTnT_8NIoAFJhr3yiG1ryIrOOKbX6ecfBCNdCFo6T_cvboV37xveAwUh34.; SUB=_2A25wmdaYDeRhGeFP61sV-CvOzTqIHXVQZfrQrDV6PUJbktANLUiikW1NQSI-eIFPm_5zxcxo3ah_9S8cH-4Nf-Iy; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W54z7GLQ_uRCDy3AoKHpPxB5JpX5K-hUgL.FoMpeh.X1h-ESoq2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeK54Shnfeoqc; SUHB=0OMk-etS2Ek-ET; SSOLoginState=1570612936'}
    def __init__(self):#初始化
        self.weibo_num=0
        self.weibo=[]
    def deal_html(self,url):#处理html
        html=requests.get(url,cookies=self.cookie).content
        selector=etree.HTML(html)
        return selector
    def get_id(self,info):#获取id信息
        id=info.xpath('@id')[0][2:]
        return id
    def get_date(self,info):#获取发表日期
        times = info.xpath('div/span[@class="ct"]/text()')#注意xpath的语法，出错一点，则不能读出数据
        times = ''.join(times)
        date = str(times[:times.find(' ')])
        #if u'今' in date:
         #   date=time.strftime("%m月%d日",time.localtime(time.time()))
        if u'今天' in times or u'分钟' in times or u'刚刚' in times:
            month=datetime.now().strftime('%m')
            day=datetime.now().strftime('%d')
            date = month+'月'+day+'日'

        return date
    def get_name(self,info):#获取发表名字
        name=info.xpath('div/a[@class="nk"]/text()')[0]
        return name

    def get_content(self,info):#获取内容
        content=''.join(info.xpath('div//text()'))
        contents = content[content.find(':') + 1:content.find(u'赞')]
        return contents
    def get_fonter(self,info):#获取点赞评论转发
        pattern = r'\d+'
        halfcontent = info.xpath('div/a/text()')
        halfcontent = ''.join(halfcontent)
        foot = halfcontent[halfcontent.find(u'赞'):halfcontent.find(u'收藏')]
        foots = re.findall(pattern, foot)
        return foots
    def printAweibo(self,info,k):#打印获取的信息
        print(self.word_list[k])
        print(self.get_id(info))
        print(self.get_date(info))
        print(self.get_name(info))
        print(self.get_content(info))
        print("点赞数:"+self.get_fonter(info)[0])
        print("转发数:" + self.get_fonter(info)[1])
        print("评论数:" + self.get_fonter(info)[2])
    def get_weibo_tuple(self,info,k):#获取微博信息的元组
        weibo=OrderedDict()
        weibo['user id']=self.get_id(info)
        weibo['weibo keyword']=self.word_list[k]
        weibo['send date']=self.get_date(info)
        weibo['user name']=self.get_name(info)
        weibo['weibo content']=self.get_content(info)
        weibo['weibo support']=self.get_fonter(info)[0]
        weibo['weibo transpound']=self.get_fonter(info)[1]
        weibo['weibo comment']=self.get_fonter(info)[2]
        return weibo
    def get_pagenum(self,k):#获取微博的页数
        try:
            url = 'https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%s&advancedfilter=1&starttime=20190920&endtime=20191008&sort=hot' % (self.word_list[k])
            html = self.deal_html(url)
            pageNum = html.xpath('//div[@class="pa"]/form/div/input[@name="mp"]')[0].attrib['value']
            pageNum = int(pageNum)
            return pageNum
        except:
            pass
    def get_keywordlist(self):
        with open(self.filename, 'r', encoding='utf8') as f:
            self.word_list = f.read()
        self.word_list=eval(self.word_list)#字符串转换为列表
        self.word_num=len(self.word_list)
    def deal_url(self,words,pageNum):  # 以后要修改，网址
        #确定微博发布的时间段20190920到20191008
        urls='https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%s&advancedfilter=1&starttime=20190920&endtime=20191008&sort=hot&page=%d'%(words,pageNum)
        return urls
    def write_weibo(self,info,k):#把元组信息写入列表
        weibo=self.get_weibo_tuple(info,k)
        self.weibo.append(weibo)
    def get_pageweibo(self, url,k):#获取一页的微博
        #容错处理，否则会出现'NoneType' object has no attribute 'xpath'
            self.selector = self.deal_html(url)
            info = self.selector.xpath("//div[@class='c']")
            for i in range(2, len(info) - 2):
                try:
                    self.weibo_num += 1
                    print(self.weibo_num)
                    self.write_weibo(info[i],k)
                    self.printAweibo(info[i],k)
                    print("-----" * 100)
                except:
                    continue
    def write_csv(self,keepfile):#写入csv文件
        filename=keepfile
        DataFrame=pd.DataFrame(self.weibo,columns=['user id','weibo keyword','send date','user name','weibo support','weibo transpound','weibo comment','weibo content'])
        DataFrame.to_csv(filename,index=False,sep=',')

    def start(self, filename, keepfilename):  # 运行爬虫
        self.filename = filename
        self.get_keywordlist()
        for k in range(0, self.word_num - 1):
            try:

                num = self.get_pagenum(k)
                pagenum = 0
                randompage = random.randint(1, 3)
                #randompage=1
                for j in range(1, num):#
                    # 设置爬虫睡眠数据避免被系统限制
                    try:
                        if j < num and j == pagenum + randompage:
                            sleep(random.randint(25, 30))
                        url = self.deal_url(self.word_list[k], j)
                        self.get_pageweibo(url, k)
                        pagenum += 1
                    except:
                        continue

            except:
                continue
        print(self.weibo)
        self.write_csv(keepfilename)
        print(u'共爬取' + str(self.weibo_num) + u'条微博')


d=WEIBO()
d.start('2019-10-04newAge.txt','data4.csv')
#第一个是读取文件的路径
#第二个是存储路径
