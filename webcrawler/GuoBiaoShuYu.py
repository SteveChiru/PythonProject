"""
需求：
    1.爬取国家标准全文公开系统上公开的现行和即将实施的标准，转换成excel数据
    2.excel文件格式 标准号-中文标准名称-英文标准名称-标准状态-在线预览链接-下载链接
细节设计：
    1.页面中如果没有在线预览按钮，说明无法在线预览，excel表中填入“无法在线预览”
    2.没有下载链接，则在excel表中输入“文档无法下载”
"""
#国家标准全文公开术语链接   标准号-标准名称-在线预览链接
from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import re
import xlwt
import urllib.parse

"""
使用xlwt模块初始化一个workbook
返回值：初始化后的workbook
"""
def initWorkBook(category):
    workbook = xlwt.Workbook(encoding='utf-8')
    return workbook

"""
在初始化后的workbook中创建worksheet
"""
def createWorkSheet(sheetname, workbook = xlwt.Workbook):
    worksheet = workbook.add_sheet(sheetname)
    #标准号-中文标准名称-英文标准名称-标准状态-在线预览链接-下载链接
    worksheet.write(0,0,'标准号'); worksheet.write(0,1,'中文标准名称')
    worksheet.write(0,2,'英文标准名称');worksheet.write(0,3,'标准状态')
    worksheet.write(0,4,'在线预览url');worksheet.write(0,5,'下载url')
    return worksheet

"""
把数据保存到excel表中
"""
def saveToExcel(pathStr, workbook = xlwt.Workbook):
    workbook.save(pathStr)

"""
使用BeautifulSoup将url地址解析为html文档
"""
def creatSoup(url):
    f = requests.get(url)                 #Get该网页从而获取该html内容
    soup = BeautifulSoup(f.content, "lxml")  #用lxml解析器解析该网页的内容, 好像f.text也是返回的html
    return soup

"""
在线阅读链接判断：没有在线阅读按钮，输出“无法在线阅读”；否则，输出在线阅读链接
"""
def getOnlineReadUrl(filenumber,soup):
    urlonlinereadurl = 'http://c.gb688.cn/bzgk/gb/showGb?type=online&hcno=' + filenumber
    zxylbutton = soup.find("button",class_="btn ck_btn btn-sm btn-primary") #获得在线预览button
    if zxylbutton is None: #没有在线预览按钮
        urlonlinereadurl = '无法在线预览'
    return urlonlinereadurl

"""
下载链接判断：没有下载链接，输出“文档无法下载”；否则，输出下载链接
"""
def getDownloadUrl(filenumber,soup):
    downloadurl = 'http://c.gb688.cn/bzgk/gb/showGb?type=download&hcno=' + filenumber
    xzbzbutton = soup.find("button",class_="btn xz_btn btn-sm btn-warning") #获得下载标准按钮
    if xzbzbutton is None:
        downloadurl = '文档无法下载'
    return downloadurl

"""
获取一个页面上的数据
"""


def getStandardStatus(beautifulsoup):
    standard_status_class = beautifulsoup.find('table', class_='tdlist').find_all('tr')[2].find('span').get('class')[0]
    standard_status = '现行'
    if standard_status_class == 'text-warning':
        standard_status = '即将实施'
    if standard_status_class == 'text-danger':
        standard_status = '废止'
    return standard_status

def getDataOfOnePage(pagenumber,datas,worksheet,category):
    datatotal = getDataTotal(category)
    pagetotal = getPageTotal(datatotal)
    data_number_per_page = 10
    row = 1 + (pagenumber-1)*10
    if pagenumber is pagetotal:
        data_number_per_page = int(datatotal)%10

    index = 0
    index_total = 2 * data_number_per_page
    while index < index_total:
        filenumber = datas[index].get('onclick')[10:-3]
        new_gb_info_url = 'http://www.gb688.cn/bzgk/gb/newGbInfo?hcno=' + filenumber   #标准信息页面
        soup = creatSoup(new_gb_info_url)
        standard_status = getStandardStatus(soup)
        if standard_status == '废止': #当标准状态为废止时，就不用保存数据到excel中
            index = index + 2
            continue
        #标准号-中文标准名称-英文标准名称-标准状态-在线预览链接-下载链接
        standard_text = soup.find('h1').get_text()
        standard_number = standard_text[4:]
        if '采' in standard_text:
            standard_number = standard_text[4:-2]
        standard_chi_name = soup.find('table',class_='tdlist').find('b').string
        standard_eng_name = soup.find('table',class_='tdlist').find_all('td')[2].string[7:]
        urlonlinereadurl = getOnlineReadUrl(filenumber,soup)    #处理在线阅读链接
        downloadurl = getDownloadUrl(filenumber,soup)    #处理下载标准链接

        #写数据
        worksheet.write(row,0,standard_number); worksheet.write(row,1,standard_chi_name)
        worksheet.write(row,2,standard_eng_name);worksheet.write(row,3,standard_status)
        worksheet.write(row,4,urlonlinereadurl);worksheet.write(row,5,downloadurl)

        index = index + 2
        row = row + 1

    print("第"+str(pagenumber)+"页数据获取完毕")

"""
获取所需要的所有数据
"""

"""
获取给定类别的数据总共有多少页
"""
def getDataTotal(category):
    category_to_url = urllib.parse.quote(category)
    category_url = 'http://www.gb688.cn/bzgk/gb/std_list?r=0.5129843308028312&page=1&pageSize=10&p.p1=0&p.p2='+category_to_url+'&p.p90=circulation_date&p.p91=desc'
    soup = creatSoup(category_url)
    standard_text = soup.find_all('td',class_='hidden-sm hidden-xs')[0].find('span').get_text()
    datatotal = re.findall(r"[共]\xa0(.+?)\xa0[条]",standard_text)[0]
    return datatotal

"""
获取总数据的总页数
"""
def getPageTotal(datatotal):
    pagetotal = int(datatotal)//10 + 1
    return pagetotal

def getAllData(workbook,category):
    pagetotal = getPageTotal(getDataTotal(category))  #获取指定类别的数据的总页数
    savepath = setSavePath(category)    #设置要文件存储路径
    worksheet = createWorkSheet(category,workbook)
    category_url = urllib.parse.quote(category) #类别从汉字转为url编码
    pageindex = 1
    while pageindex <= pagetotal:
        url = 'http://www.gb688.cn/bzgk/gb/std_list?page='+str(pageindex)+'&pageSize=10&p.p1=0&p.p2=' +category_url+ '&p.p90=circulation_date&p.p91=desc'
        soup = creatSoup(url)
        table = soup.find('table',class_='table result_list table-striped table-hover')
        datas = table.find_all('a')

        #   把一个页面上的信息存入excel文件内

        getDataOfOnePage(pageindex,datas,worksheet,category)
        pageindex = pageindex + 1

    saveToExcel(savepath,workbook)  #把数据保存到excel文件内
    print("共"+str(pagetotal)+"页数据爬取完毕") #信息提示

"""
设置要爬取的数据的类别
"""
def setCategory(category):
    return category

"""
设置数据要存储的路径
"""
def setSavePath(category):
    savepath = 'D:\databank\爬虫\国标术语\国标术语-'+category+'.xls'  #设置excel文件存储路径
    return savepath

#函数入口
if __name__ == "__main__":

    category = setCategory('船舶')    #   设置要爬取的数据类别
    workbook = initWorkBook(category)       # 创建一个workbook 设置编码
    getAllData(workbook,category)   #爬取所有数据


