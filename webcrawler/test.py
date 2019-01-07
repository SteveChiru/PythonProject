"""
用于测试所需各个子功能
"""

from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import re
import xlwt

"""
使用BeautifulSoup将url地址解析为html文档
"""
def creatSoup(url):
    f = requests.get(url)                 #Get该网页从而获取该html内容
    soup = BeautifulSoup(f.content, "lxml")  #用lxml解析器解析该网页的内容, 好像f.text也是返回的html
    return soup

#函数入口
if __name__ == "__main__":
    url = 'http://www.gb688.cn/bzgk/gb/newGbInfo?hcno=AD030DBE101E29611F33B318BC301666'
    soup = creatSoup(url)
    #标准号-中文标准名称-英文标准名称-标准状态-在线预览链接-下载链接
    #带有采字
    standard_text = soup.find('h1').get_text()
    standard_number = standard_text[4:]
    if '采' in standard_text:
        standard_number = standard_text[4:-2]

    print(standard_number)

    """
    standard_chi_name = soup.find('table',class_='tdlist').find('b').string
    standard_eng_name = soup.find('table',class_='tdlist').find_all('td')[2].string[7:]
    standard_status = soup.find('span',class_='text-success').string
    """

    """
    print(standard_chi_name)
    print(standard_eng_name)
    print(standard_status)
    """
