#国家标准全文公开术语链接   标准号-标准名称-在线预览链接
from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import re
import xlwt

"""
使用xlwt模块初始化一个workbook
返回值：初始化后的workbook
"""
def initWorkBook():
    workbook = xlwt.Workbook(encoding='utf-8')
    return workbook

"""
在初始化后的workbook中创建worksheet
"""
def createWorkSheet(sheetname, workbook = xlwt.Workbook):
    worksheet = workbook.add_sheet(sheetname)
    worksheet.write(0,0,'标准号'); worksheet.write(0,1,'标准名称');worksheet.write(0,2,'在线预览url')
    return worksheet

"""
把数据保存到excel表中
"""
def saveToExcel(pathStr, workbook = xlwt.Workbook):
    workbook.save(pathStr)

"""
获取一个页面上的数据
"""
def getDataOfOnePage(pagenumber,datas):
    index = 0
    row = 1 + (pagenumber-1)*10
    while index < 20:
        standardnumber = datas[index].string
        standardname = datas[index+1].string;standardID = datas[index+1].get('onclick');filenumber = standardID[10:-3]
        urlonlineread = 'http://c.gb688.cn/bzgk/gb/showGb?type=online&hcno='+filenumber

        #写数据
        worksheet.write(row,0,standardnumber);worksheet.write(row,1,standardname);worksheet.write(row,2,urlonlineread)

        index = index + 2
        row = row + 1

    print("第"+str(pagenumber)+"页数据获取完毕")

"""
获取所需要的所有数据
"""
def getAllData(pagetotal):
    pageindex = 1
    while pageindex <= pagetotal:
        url = "http://www.gb688.cn/bzgk/gb/std_list?page="+str(pageindex)+"&pageSize=10&p.p1=0&p.p2=%E8%88%B9%E8%88%B6&p.p5=PUBLISHED&p.p90=circulation_date&p.p91=desc"
        f = requests.get(url)                 #Get该网页从而获取该html内容
        soup = BeautifulSoup(f.content, "lxml")  #用lxml解析器解析该网页的内容, 好像f.text也是返回的html
        table = soup.find('table',class_='table result_list table-striped table-hover')
        datas = table.find_all('a')

        #   把一个页面上的信息存入excel文件内
        getDataOfOnePage(pageindex,datas)
        pageindex = pageindex + 1

#函数入口
if __name__ == "__main__":

    #   设置要爬取的数据的参数
    category = '船舶'     #设置要爬取的术语的类别
    pagetotal = 2          #设置要爬取的数据总共有多少页
    path = 'D:\databank\爬虫\国标术语\国标术语-'+category+'.xls'  #设置excel文件存储路径

    workbook = initWorkBook()       # 创建一个workbook 设置编码
    worksheet = createWorkSheet(category, workbook) # 创建一个worksheet
    getAllData(pagetotal)   #爬取所有数据
    saveToExcel(path,workbook)  #把数据保存到excel文件内

    print("共"+str(pagetotal)+"页数据爬取完毕") #信息提示
