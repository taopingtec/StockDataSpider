#导入需要使用到的模块
import requests
from bs4 import BeautifulSoup
import traceback
import urllib
import re
import pandas as pd
import pymysql
import os

mysqlHost='127.0.0.1'
mysqlPort=3306
mysqlUser='root'
mysqlPassWord='abc@123'
database='stock_data'

def saveStockList2Mysql(lst):
    conn = pymysql.connect(host=mysqlHost, port=mysqlPort, user=mysqlUser, passwd=mysqlPassWord, db=database, charset='utf8') 
    cursor = conn.cursor()
    insertSql = ('insert into stock(stock_no, stock_name) values(%s, %s)')
    
    for stock in lst:
        try:
            cursor.execute(insertSql, (stock[0], stock[1]))
        except:
            continue
    
    conn.commit()
    cursor.close()
    conn.close()
    
def createTableIfNeeded(code):    
    conn = pymysql.connect(host=mysqlHost, port=mysqlPort, user=mysqlUser, passwd=mysqlPassWord, db=database, charset='utf8')
    cursor = conn.cursor()
    createTableSql = "CREATE TABLE stock_date_%s LIKE stock_date;" % (code[-2:])
    print(createTableSql)
    try:
        cursor.execute(createTableSql)
    except BaseException as e:
        print(e)
    conn.commit()
    cursor.close()
    conn.close()
        
def save2DB(filePath, code):
    createTableIfNeeded(code)
    conn = pymysql.connect(host=mysqlHost, port=mysqlPort, user=mysqlUser, passwd=mysqlPassWord, db=database, charset='utf8') 
    cursor = conn.cursor()
    data = pd.read_csv(filepath+code+'.csv', 'gbk')
    #print(data.columns)
    length = len(data)
    for i in range(2, length):
        record = tuple(data.loc[i])
        info_data = record[0].split(',')
        try:
            #sqlSentence4 = "insert into stock_date(trade_date, stock_no, stock_name, JinShou, ZuiGao, ZuiDi, JinKai,\
            #                   ZuoShou, ShangZhang, ZhangFu, HuanSouLv, ChengJiaoLiang, ChengJiaoE, ZongShiZhi, LiuTongShiZhi)  \
            #                   values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
            sqlSentence4 = "insert into stock_date_%s(trade_date, stock_no, stock_name, JinShou, ZuiGao, ZuiDi, JinKai,\
                               ZuoShou, ShangZhang, ZhangFu, HuanSouLv, ChengJiaoLiang, ChengJiaoE, ZongShiZhi, LiuTongShiZhi)  \
                               values ('%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (code[-2:], info_data[0], code, info_data[2], info_data[3], info_data[4], info_data[5], info_data[6], info_data[7], info_data[8], info_data[9], info_data[10], info_data[11], info_data[12], int(float(info_data[13])/10000), int(float(info_data[14])/10000))
            #print(sqlSentence4)
            #获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
            sqlSentence4 = sqlSentence4.replace('nan','null').replace('None','null').replace('none','null') 
            cursor.execute(sqlSentence4)
        except BaseException as e:#如果以上插入过程出错，跳过这条数据记录，继续往下进行
            #print(info_data)
            #print(e)        
            continue
    conn.commit()
    cursor.close()
    conn.close()            

#爬虫抓取网页函数
def getHtml(url):
    html = urllib.request.urlopen(url).read()
    html = html.decode('utf-8')
    f = open('test.txt', 'w')
    f.write(html)
    f.close()
    return html

#抓取网页股票代码函数
def getStackCode(html):
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    return code
    
def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except BaseException as e:
        print(e)
        return ""    
    
def getStockList(lst, stockURL):
    html = getHTMLText(stockURL)
    if "" == html:
        print("get html error of:%s" %(stockURL))
        return
        
    soup = BeautifulSoup(html, 'html.parser')
    listDiv = soup.find('div', attrs={'class': 'u-postcontent cz'})
    listContent = listDiv.find_all('a')
    
    for stock in listContent:
        stockSplit = stock.text.split('(')
        stockInfo = [stockSplit[1].split(')')[0], stockSplit[0]]
        lst.append(stockInfo)
    
    print(len(lst))
    saveStockList2Mysql(lst)    
    
#Url = 'http://quote.eastmoney.com/stocklist.html'#东方财富网股票数据连接地址
filepath = '.\\data\\'#定义数据文件保存路径
#实施抓取
#code = getStackCode(getHtml(Url)) 
stock_list_url_sz = 'https://www.banban.cn/gupiao/list_sz.html'
stock_info_url_sz = 'https://gupiao.baidu.com/stock/sz'
stock_list_url_sh = 'https://www.banban.cn/gupiao/list_sh.html'
stock_info_url_sh = 'https://gupiao.baidu.com/stock/sh'
stock_list_url_cyb = 'https://www.banban.cn/gupiao/list_cyb.html'
stock_info_url_cyb = 'https://gupiao.baidu.com/stock/sz'
    
slist = []
    
getStockList(slist, stock_list_url_sz)
#print(slist)
        
print('========================================================')
#slist = []
#getStockList(slist, stock_list_url_sh)
   
print('========================================================')
#slist = []
#getStockList(slist, stock_list_url_cyb)

#print(code)
#获取所有股票代码（以6开头的，应该是沪市数据）集合
#CodeList = ['600505']
index = 0
for item in slist:
    code = item[0]
    index = index + 1
    print("Processing " + str(index) + " of " + str(len(slist)) + " :" + str(item))
    preCode = '1'
    if code[0]=='6':
        preCode = '0'
    url = 'http://quotes.money.163.com/service/chddata.html?code='+preCode+code+\
        '&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    #print(url)
    #urllib.request.urlretrieve(url, filepath+code+'.csv')   
    save2DB(filepath, code)    
    #break