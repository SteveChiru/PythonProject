#国家标准全文公开术语链接   标准号-标准名称-在线预览链接
from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import re
import xlwt

#函数入口
if __name__ == "__main__":

    #   1.初始化一个excel文件
    # 创建一个workbook 设置编码
    workbook = xlwt.Workbook(encoding = 'utf-8')
    # 创建一个worksheet
    worksheet = workbook.add_sheet('船舶')
    # 设计列名
    worksheet.write(0,0,'标准号'); worksheet.write(0,1,'标准名称');worksheet.write(0,2,'在线预览url')

    #   2.遍历页面获取数据
    page = 1
    while page <= 27:
        url = "http://www.gb688.cn/bzgk/gb/std_list?page="+str(page)+"&pageSize=10&p.p1=0&p.p2=%E8%88%B9%E8%88%B6&p.p5=PUBLISHED&p.p90=circulation_date&p.p91=desc"
        f = requests.get(url)                 #Get该网页从而获取该html内容
        soup = BeautifulSoup(f.content, "lxml")  #用lxml解析器解析该网页的内容, 好像f.text也是返回的html
        table = soup.find('table',class_='table result_list table-striped table-hover')
        datas = table.find_all('a')

        #   3.把一个页面上的信息存入excel文件内
        index = 0
        row = 1 + (page-1)*10
        while index < 20:
            standardnumber = datas[index].string
            standardname = datas[index+1].string;standardID = datas[index+1].get('onclick');filenumber = standardID[10:-3]
            urlonlineread = 'http://c.gb688.cn/bzgk/gb/showGb?type=online&hcno='+filenumber

            #写数据
            worksheet.write(row,0,standardnumber);worksheet.write(row,1,standardname);worksheet.write(row,2,urlonlineread)

            index = index + 2
            row = row + 1

        print("第"+str(page)+"页数据获取完毕")
        page = page + 1

    #   4.数据写完后保存到excel文件内
    workbook.save('D:\databank\爬虫\国标术语\国标术语-船舶.xls')
    print("共"+str(page-1)+"页数据爬取完毕")
