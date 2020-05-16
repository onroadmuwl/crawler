本程序以使用etree，request，pymysql为主，构建爬虫程序，数据程序，数据处理程序三部分。<br>
简单分析与国庆70周年阅兵相关的微博热点事件与热点人物。 <br> 
整个程序包括两个爬虫程序，catch1，catch3，一个连接数据库程序dataBase，一个数据处理程序deal_data，一个输出csv程序Database_to_csv<br>
运行次序：catch1-----catch3------dataBase-----data_data------Data_to_csv<br>

catch1:
======
通过cookie访问微博网站： <br> 
https://s.weibo.com/top/summary?cate=socialevent   <br> 
该网站国庆期间报告国庆70周年专属内容（新时代）， <br> 
https://s.weibo.com/top/summary?cate=realtimehot <br> 
也可以爬取微博热搜内容，但在这个程序没有用到 <br> 
在程序最后的k=WEIBO()，括号里面是1的话，爬取微博热搜的关键词列表，是0的话爬取微博新时代的关键词列表 <br> 
自动命名为 "当天日期"+newSearch.txt 或者 "当天日期"+newAge.txt，要是cookie没过期的话，直接运行即可 <br> 
cookie如果过期，可以重新添加，具体步骤如下 <br> 

1.用Chrome打开<https://passport.weibo.cn/signin/login> <br> 
2.输入微博的用户名、密码，登录 <br> 
登录成功后会跳转到<https://m.weibo.cn>; <br> 
3.按F12键打开Chrome开发者工具，在地址栏输入并跳转到<https://weibo.cn> <br> 
4.依此点击Chrome开发者工具中的Network->Name中的weibo.cn->Headers->Request Headers，"Cookie:"后的值即为我们要找的cookie值，复制即可 <br> 



catch3：
========
爬取某一关键词列表下面的全部网页内容，包括微博的用户id，发布日期（精确到日），微博内容，点赞数，评论数，转发数，写到指定的csv文件 <br> 
<https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%s&advancedfilter=1&starttime=20190920&endtime=20191008&sort=hot' % (self.word_list[k]> <br> 
<https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%s&advancedfilter=1&starttime=20190920&endtime=20191008&sort=hot&page=%d'%(words,pageNum) ><br> 
第一个网址只用于爬取微博页数，不要其他的，爬取的内容是从9月20日到10月8日，按热度排序 <br> 
第二个网址加上第一个网址提供的翻页功能，进行内容爬取 <br> 
如果catch1只是涉及到xpath模块的皮毛，catch3对于xpath模块来说至关重要，要注意每一个细节，充分利用chrome的对照功能。 <br> 
重点！！！设置睡眠时间，如果爬虫过快会被限制住，直接停止运行，如果爬一两百条数据还好，爬上千条数据及以上一定要设置睡眠时间，慢慢爬
还有是要保证网络的质量，要不然直接停掉。 <br> 
d.start('.csv','.csv')，运行时前一个文件名是从catch1爬取的微博热词列表，后一文件名是自定义的csv文件名，我定义为data4，data5···data8
运行本程序需要catch1处理的微博热词列表，与有效的cookie <br> 

dataBase:
================
连接数据库服务器，创建一个新的数据库，然后命名为weibofile，重新连接数据库服务器，加上数据库weibofile，创建表weibo <br> 
（可以把连接参数写成元组，就不需要二次连接，直接把weibofile加入元组）把csv文件读出来，做出元组，插入到weibo表中。 <br> 
把catch3处理的数据都插入到数据库中，好处是重复数据可以替换，不会报错（REPLACE INTO） <br> 
运行本程序需要MYSQL workbench，还有catch3处理的data数据 <br> 

deal_data
========
本程序在pandas的运用上均属于基本操作，先通过sql语句从数据库中获取我们需要的数据（被sql加工过），然后通过pandas的分组操作，得到一些csv数据 <br> 
再通过matplotlib得出图表。本程序虽然简单，但涉及到许多关于细节内容需要注意，如dataframe如何显示全文，得到的图表如何避免中文乱码等等 <br> 

Database_to_csv
===============
基本上是上一个程序的子程序，把数据库中的weibo表分别按评论数，点赞数，转发数排序提取出来，作为csv文件 <br> 
