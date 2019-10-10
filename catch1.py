#encoding:utf-8--
from lxml import etree
import time
import requests
class WEIBO():
    cookie={

        'Cookie': '_T_WM=52165934645; ALF=1573204852; SCF=ArdMMKY9SBOgWxi4HE1DCrEm8vYkDcTnT_8NIoAFJhr3yiG1ryIrOOKbX6ecfBCNdCFo6T_cvboV37xveAwUh34.; SUB=_2A25wmdaYDeRhGeFP61sV-CvOzTqIHXVQZfrQrDV6PUJbktANLUiikW1NQSI-eIFPm_5zxcxo3ah_9S8cH-4Nf-Iy; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W54z7GLQ_uRCDy3AoKHpPxB5JpX5K-hUgL.FoMpeh.X1h-ESoq2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeK54Shnfeoqc; SUHB=0OMk-etS2Ek-ET; SSOLoginState=1570612936'}
    #cookie免验证登录
    def __init__(self,choose):
        self.choose=choose#选择功能，因为本程序爬两个不同的网页
    def getdate(self):#获取时间
        self.time=time.strftime('%Y-%m-%d',time.localtime(time.time()))#字符串转为日期格式
        return self.time

    def get_weibo_newage(self):
        url = 'https://s.weibo.com/top/summary?cate=socialevent'#新时代的网站
        html = requests.get(url, cookies=self.cookie).content#解析网页，获取网页内容
        selector = etree.HTML(html)#得到element对象
        self.weibo=selector.xpath('//td[@class="td-02"]/*/text()')#爬取相关文本内容
        self.weibo_1=[]
        for i in self.weibo:
            i=i[1:-1]#去掉‘#’
            self.weibo_1.append(i)
        self.weibo=self.weibo_1
        sep=','
        self.time=self.getdate()
        self.path=str(self.time)+'newAge.txt'#命名文件
        with open(self.path,'a',encoding='utf-8') as f:
                f.write(str(self.weibo))#用逗号分割文本
        print(self.weibo)
    def get_weibo_hotSearch(self):#同上，只是不用再进行去‘#’
        url = 'https://s.weibo.com/top/summary?cate=realtimehot'
        html = requests.get(url, cookies=self.cookie).content
        selector = etree.HTML(html)
        self.weibo=selector.xpath('//td[@class="td-02"]/a/text()')
        sep=','
        self.time=self.getdate()
        self.path=str(self.time)+'hotSearch.txt'
        with open(self.path,'a',encoding='utf-8') as f:
                f.write(str(self.weibo))
        print(self.weibo)
    def start(self):#如果是0，爬取新时代网页
        if self.choose==0:
            self.get_weibo_newage()
        elif self.choose==1:#如果是1，爬取热搜网页
            self.get_weibo_hotSearch()
if __name__=='__main__':
    k=WEIBO(1)
    k.start()





