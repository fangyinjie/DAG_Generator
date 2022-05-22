#!/usr/bin/env python
# -*- coding:utf-8 -*-
# - 需求：爬取搜狗首页的页面数据
# 1.最简单最轻量的  一般是打开默认的浏览器进行下载
# 下载文件保存在本地 运行完全没有问题
import requests
import urllib.request as ur
# import urllib.request
if __name__ == "__main__":
    # step_1:指定url
    # url = 'https://dblp.uni-trier.de/db/conf/sc/index.html'
    url = 'http://www.math.pku.edu.cn/teachers/lidf/docs/textrick/tricks.pdf'
    # step_2:发起请求
    # get方法会返回一个响应对象
    response    = requests.get(url=url)
    file        = ur.urlopen(url=url)
    # step_3:获取响应数据.text返回的是字符串形式的响应数据
    page_text   = response.text
    data        = file.read()           # 读取全部
    dataline    = file.readline()       # 读取一行内容
    # print(page_text)
    # step_4:持久化存储
    with open('sogou.txt', 'w', encoding='utf-8') as fp:
        fp.write(page_text)
    print('爬取数据结束！！！')
    fhandle = open("1.html", "wb")    # 将爬取的网页保存在本地
    fhandle.write(data)
    fhandle.close()

