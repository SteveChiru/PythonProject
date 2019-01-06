"""
本文件用于演示beautiful soup4的函数的用法
"""

from bs4 import BeautifulSoup
from lxml import html

soup = BeautifulSoup(open("testbs.html"),"lxml")
print(soup) #输出html文件全部内容

