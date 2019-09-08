'''
要用到两个网站：
1.获取所有股票的名称的网址（这里指上交所和深交所的股票）
https://www.banban.cn/gupiao/list_sz.html
2.获取单个股票的各类信息
https://gupiao.baidu.com/stock/股票名称.html
'''
 
import requests
from bs4 import BeautifulSoup
import traceback
import re
import pymysql

mysqlHost='127.0.0.1'
mysqlPort=3306
mysqlUser='root'
mysqlPassWord='abc@123'
database='stock_data'
 
#获取网页内容
def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""
        

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
 
#获取所有的股票名称，将其放在一个列表中
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
 
 
def getStockInfo(lst, stockURL, fpath):
    count = 0
    for stock in lst:
        url = stockURL + stock[0] + ".html"#对应的每只股票的网址
        print(url)
        #break
        html = getHTMLText(url)
        #print(html)
        try:
            if html == "":
                print('html is empty')
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})
 
            name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
            infoDict.update({'股票名称': name.text.split()[0]})
            print('股票代码:%s' %(stock))
            print('股票名称:%s' %(name.text.split()[0]))
            
            time = stockInfo.find_all(attrs={'class': 'state f-up'})[0]
            print('时间:%s' %(time.text.split()))
            
            price = stockInfo.find_all(attrs={'class': 'price s-up'})[0]
            print('价格:%s' %(price.text.split()))
 
            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val
                print("%s:%s" %(key,val))
                #print(val)
 
#保存到本地，并加载进度条
            #with open(fpath, 'a', encoding='utf-8') as f:
            #    f.write(str(infoDict) + '\n')
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
            print('')
            break
                
        except BaseException as e:
            print(e)
            count = count + 1
            print("\rexcept 当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
            continue
 
 
def main():
    stock_list_url_sz = 'https://www.banban.cn/gupiao/list_sz.html'
    stock_info_url_sz = 'https://gupiao.baidu.com/stock/sz'
    stock_list_url_sh = 'https://www.banban.cn/gupiao/list_sh.html'
    stock_info_url_sh = 'https://gupiao.baidu.com/stock/sh'
    stock_list_url_cyb = 'https://www.banban.cn/gupiao/list_cyb.html'
    stock_info_url_cyb = 'https://gupiao.baidu.com/stock/sz'
    
    output_file = 'D:/taoping/Project/Stock/Data/BaiduStockInfo.txt'
    slist = []
    
    getStockList(slist, stock_list_url_sz)
    #print(slist)
    getStockInfo(slist, stock_info_url_sz, output_file)
        
    print('========================================================')
    #slist = []
    #getStockList(slist, stock_list_url_sh)
    #getStockInfo(slist, stock_info_url_sh, output_file)
    
    print('========================================================')
    #slist = []
    #getStockList(slist, stock_list_url_cyb)
    #getStockInfo(slist, stock_info_url_cyb, output_file)
 
 
main()
