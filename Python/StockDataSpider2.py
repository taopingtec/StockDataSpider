#导入需要使用到的模块
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

def save2DB(filePath, code):
    conn = pymysql.connect(host=mysqlHost, port=mysqlPort, user=mysqlUser, passwd=mysqlPassWord, db=database, charset='utf8') 
    cursor = conn.cursor()
    print(filepath+code+'.csv')
    data = pd.read_csv(filepath+code+'.csv', 'gbk')
    #print('正在存储stock_%s'% fileName[0:6])
    print(data.columns)
    length = len(data)
    for i in range(0, length):
        record = tuple(data.loc[i])
        info_data = record[0].split(',')
        print(int(float(info_data[13])/10000))
        #插入数据语句
        try:
            #sqlSentence4 = "insert into stock_date(trade_date, stock_no, stock_name, JinShou, ZuiGao, ZuiDi, JinKai,\
            #                   ZuoShou, ShangZhang, ZhangFu, HuanSouLv, ChengJiaoLiang, ChengJiaoE, ZongShiZhi, LiuTongShiZhi)  \
            #                   values ('%s',%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
            sqlSentence4 = "insert into stock_date(trade_date, stock_no, stock_name, JinShou, ZuiGao, ZuiDi, JinKai,\
                               ZuoShou, ShangZhang, ZhangFu, HuanSouLv, ChengJiaoLiang, ChengJiaoE, ZongShiZhi, LiuTongShiZhi)  \
                               values ('%s',%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (info_data[0], info_data[1][1:7], info_data[2], info_data[3], info_data[4], info_data[5], info_data[6], info_data[7], info_data[8], info_data[9], info_data[10], info_data[11], info_data[12], int(float(info_data[13])/10000), int(float(info_data[14])/10000))

            print(sqlSentence4)
            #获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
            sqlSentence4 = sqlSentence4.replace('nan','null').replace('None','null').replace('none','null') 
            cursor.execute(sqlSentence4)
        except BaseException as e:#如果以上插入过程出错，跳过这条数据记录，继续往下进行
            print(e)        
            break
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
    
Url = 'http://quote.eastmoney.com/stocklist.html'#东方财富网股票数据连接地址
filepath = '.\\data\\'#定义数据文件保存路径
#实施抓取
code = getStackCode(getHtml(Url)) 
print(code)
#获取所有股票代码（以6开头的，应该是沪市数据）集合
CodeList = ['600505']
#for item in code:
#    if item[0]=='6':
#        CodeList.append(item)
#抓取数据并保存到本地csv文件
for code in CodeList:
    print('正在获取股票%s数据'%code)
    url = 'http://quotes.money.163.com/service/chddata.html?code=0'+code+\
        '&end=20161231&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
    print(url)
    urllib.request.urlretrieve(url, filepath+code+'.csv')   
    save2DB(filepath, code)    