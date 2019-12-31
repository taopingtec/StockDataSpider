import xlwt
import requests
from bs4 import BeautifulSoup
import traceback
import urllib
import re
import pandas as pd
import pymysql
import os
import datetime
from datetime import date, timedelta

mysqlHost='127.0.0.1'
mysqlPort=3306
mysqlUser='root'
mysqlPassWord='abc@123'
database='stock_data'
dbConn = pymysql.connect(host=mysqlHost, port=mysqlPort, user=mysqlUser, passwd=mysqlPassWord, db=database, charset='utf8')


class stockMinMax:
    stockNo = 'NA'
    stockName = 'NA'
    minValue = 8888888;
    minDate = 16540504;
    maxValue = -8888888;
    maxDate = 16540504;
    incRatio = 0
    
    def __init__(self, values):
        self.stockNo = values.loc[values.shape[0] - 1, 'stock_no']
        self.stockName = values.loc[values.shape[0] - 1, 'stock_name']
        self.minValue = values.loc[values.shape[0] - 1, 'JinShou']
        self.minDate = values.loc[values.shape[0] - 1, 'trade_date']
        self.maxValue = values.loc[0, 'JinShou']
        self.maxDate = values.loc[0, 'trade_date']
        
        if(0 == self.minValue or 0 == self.maxValue):
            self.incRatio = -111
        elif(self.minDate > self.maxDate):
            self.incRatio = (self.minValue - self.maxValue) / self.maxValue * 100;
        else:
            self.incRatio = (self.maxValue - self.minValue) / self.minValue * 100;
            
        
        #print("minDate: " + str(self.minDate) + ", minValue: " + str(self.minValue))
        #print("maxDate: " + str(self.maxDate) + ", maxValue: " + str(self.maxValue))
        #print("incRatio: " + str(self.incRatio) + ",  " + str('%.2f' % self.incRatio))


def getMinMaxByCode(lst, code, start, end):
    #查出相关数据
    tradeSql = "select stock_no,stock_name,trade_date,JinShou from stock_date_" + code[-2:] + " where stock_no=" + code \
               +" and trade_date>" + start + " and trade_date<" + end + " order by JinShou desc;"
    df = pd.read_sql(tradeSql, dbConn)
    
    if(df.empty):
        return
        
    #构造stockMinMax
    minMax = stockMinMax(df)
    
    #放到lst
    lst.append(minMax)
    
def incRatioCmp(element):
    return element.incRatio
    
def save2Excel(stockMinMaxList, excelFilePath):
    writebook = xlwt.Workbook()
    
    #创建表和写表头
    test = writebook.add_sheet('涨幅排序')
    test.write(0,0,'股票代码')
    test.write(0,1,'股票名称')
    test.write(0,2,'涨幅')
    test.write(0,3,'最低')
    test.write(0,4,'最低日期')
    test.write(0,5,'最高')
    test.write(0,6,'最高日期')
    
    rowNo = 1
    #第0行第1列写入字符串'this is a test'
    for stockMinMax in stockMinMaxList:
        test.write(rowNo,0,stockMinMax.stockNo)
        test.write(rowNo,1,stockMinMax.stockName)
        test.write(rowNo,2,str('%.2f' % stockMinMax.incRatio) + '%')
        test.write(rowNo,3,stockMinMax.minValue)
        test.write(rowNo,4,str(stockMinMax.minDate))
        test.write(rowNo,5,stockMinMax.maxValue)
        test.write(rowNo,6,str(stockMinMax.maxDate))
        rowNo += 1
    
    writebook.save(excelFilePath) 
    
            
def getAllStockMinMax(start, end):
    sql = "select stock_no,stock_name from stock;"
    df = pd.read_sql(sql, dbConn)
    stockMinMaxList = []
    for index,row in df.iterrows():
        print("Has processed " + str(index) + " of " + str(df.shape[0]) + ", " + row['stock_no'] + ", " + row['stock_name'])
        #获取每只股票的最高最低，然后按比例高低排序
        stockMinMax = getMinMaxByCode(stockMinMaxList, row['stock_no'], start, end)
        
        
    #按比例高低排序    
    stockMinMaxList.sort(key=incRatioCmp, reverse=True)       
    save2Excel(stockMinMaxList, "incRaio.xlsx")

getAllStockMinMax('20191120', '20191227')
    
dbConn.close()    

