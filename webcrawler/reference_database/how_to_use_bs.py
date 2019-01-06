"""
本文件用于演示beautiful soup4的函数的用法
"""

from bs4 import BeautifulSoup
from lxml import html
import re

soup = BeautifulSoup(open("testbs.html"),"lxml")
#print(soup) #输出html文件全部内容

"""
搜索文档树
1.find_all(name,attrs,recursive,string,**kwargs)
2.find(name,attrs,recursive,string,**kwargs)
"""

###使用find_all()方法###
#name参数
#print(soup.find_all('title'))   #获取所有的a标签

#keyword参数
#print(soup.find_all(id='link2'))    #获取id是link2的标签
#print(soup.find_all(href=re.compile("elsie")))  #使用正则
#print(soup.find_all(href=re.compile("elsie"),id="link1"))   #使用多个指定名字的参数

#按CSS搜索
print(soup.find_all("a",class_="sister"))   #class 在Python中是保留字,使用 class 做参数会导致语法错误

###使用find()方法###
"""
find_all()方法和find()方法的区别：
1.find_all() 方法的返回结果是值包含一个元素的列表,而 find() 方法直接返回结果.
2.find_all() 方法没有找到目标是返回空列表, find() 方法找不到目标时,返回 None .
"""