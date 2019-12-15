import requests
from bs4 import BeautifulSoup
import traceback
import urllib
import re
import json
import pymysql

mysqlHost='127.0.0.1'
mysqlPort=3306
mysqlUser='root'
mysqlPassWord='abc@123'
database='stock_data'

def save2DB(stockDatas):
    conn = pymysql.connect(host=mysqlHost, port=mysqlPort, user=mysqlUser, passwd=mysqlPassWord, db=database, charset='utf8') 
    cursor = conn.cursor()
    length = len(stockDatas)
    for i in range(0, length):
        record = stockDatas[i]
        try:
            sqlSentence = "update stock set pe_static=" + str(record['f114']) + ", pe_dynamic=" + str(record['f9']) + ", pe_rolling=" + str(record['f115']) \
                          + ", pb=" + str(record['f23']) + " where stock_no=" + record['f12'] + ";"

            #获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值
            sqlSentence = sqlSentence.replace('nan','null').replace('None','null').replace('none','null') 
            cursor.execute(sqlSentence)           
        except BaseException as e:
            print(e)        
            continue
             
    conn.commit()
    cursor.close()
    conn.close()            

def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except BaseException as e:
        print(e)
        return ""         

def getStockSYL(stockURL):
    html = getHTMLText(stockURL)
    if "" == html:
        print("get html error of:%s" %(stockURL))
        return
        
    jsonStartIndex = html.index('(') + 1
    jsonStr = html[jsonStartIndex:-2]
    jsonRes = json.loads(jsonStr)
    print(len(jsonRes['data']['diff']))
    save2DB(jsonRes['data']['diff'])
    
stock_info_url_syl = 'http://57.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112407863401632324523_1569412177635&pn=1&pz=10000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f8,f9,f12,f14,f23,f114,f115&_=1569412177653'
getStockSYL(stock_info_url_syl) 


#http://57.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112407863401632324523_1569412177635&pn=1&pz=10000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f8,f9,f12,f14,f23,f114,f115&_=1569412177653

#全面的
#http://57.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112407863401632324523_1569412177635&pn=1&pz=1&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f14,f15,f16,f17,f18,f19,f20,f21,f22,f23,f24,f25,ff114,f115&_=1569412177653

#f8,f9,f12,f14,f23,f114,f115
#f12:股票代码
#f14:股票名称
#f8:换手率
#f9:动态市盈率
#f23:市净率
#f114:静态市盈率
#f115：滚动市盈率
        
#https://tushare.pro/document/1?doc_id=42

#jQuery112407863401632324523_1569412177635
#(
#  {"rc":0,"rt":6,"svr":181669436,"lt":1,"full":1,"data":
#      {"total":3866,"diff":
#         [
#            {"f8":0.46,"f9":39.93,"f12":"300810","f14":"N中科","f23":2.89,"f114":32.49,"f115":25.39},
#            {"f8":5.87,"f9":-83.15,"f12":"002656","f14":"摩登大道","f23":1.19,"f114":100.02,"f115":-50.07},
#            {"f8":0.38,"f9":363.16,"f12":"600712","f14":"南宁百货","f23":2.84,"f114":-64.83,"f115":-2277.19},
#            {"f8":19.98,"f9":-31.46,"f12":"000835","f14":"长城动漫","f23":-87.46,"f114":-3.66,"f115":-3.5},
#            {"f8":4.43,"f9":-2.84,"f12":"300278","f14":"华昌达","f23":2.46,"f114":104.94,"f115":-3.9},
#            {"f8":4.33,"f9":134.09,"f12":"002288","f14":"超华科技","f23":2.9,"f114":132.8,"f115":235.59},
#            {"f8":4.89,"f9":17.93,"f12":"000417","f14":"合肥百货","f23":0.96,"f114":17.09,"f115":17.98},
#            {"f8":3.54,"f9":34.24,"f12":"002343","f14":"慈文传媒","f23":2.62,"f114":-3.75,"f115":-3.28},
#            {"f8":1.69,"f9":41.37,"f12":"601872","f14":"招商轮船","f23":1.88,"f114":34.15,"f115":27.49},
#            {"f8":2.02,"f9":38.74,"f12":"600576","f14":"祥源文化","f23":1.52,"f114":204.47,"f115":-2759.23}
#         ]
#      }
#   }
#);