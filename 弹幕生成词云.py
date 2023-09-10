import requests
from lxml import etree
import re
import json
import pandas as pd
import urllib3
import jieba.analyse
import wordcloud
import parsel
from matplotlib import pylab as plt
import csv
class BiLiBiLi:
    # 初始化方法
    def __init__(self,av_num):
        # 接收av号
        self.name = "BV1号" + str(av_num)
        # 拼接视频地址
        self.av_url = "https://www.bilibili.com/video/BV1{}".format(av_num)
        # 请求头
        self.headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3870.400 QQBrowser/10.8.4405.400"}
##        urllib3.disable_warnings()
    # 响应html内容，并返回
    def parse_url(self,av_url):
        response = requests.get(url=av_url,headers=self.headers)
##        return response.content.decode()
##          return response.text
        return response

    # 解析html内容
    def get_course(self,response):
##        response = requests.get(url=av_url,headers=self.headers)
        uu = response.content.decode()
        # 使用xpath
        html = etree.HTML(uu)
##        print(uu)
##        # 使用字典保存标题和oid
##        item = {}
        # 这里使用xpath提取标题
        title = html.xpath("//div[@id='app']/div/div/div/h1/span/text()")[0] if len(html.xpath("//div[@id='app']/div/div/div/h1/span/text()")) > 0 else None
####        item["点赞数:"] = html.xpath("/div[@id='app']/div[@class='v-wrap']/div[@class='l-con']/div[@id='arc_toolbar_report']/div[@class='ops']/span[@class='like']/text()")
####        item["投掷硬币数:"] = html.xpath("/div[@id='app']/div[@id='v-wrap']/div[@id='l-con']/div[@id='arc_toolbar_report']/div[@id='ops']/span[@id='coin']/text()")
####        item["收藏人数:"] = html.xpath("/div[@id='app']/div[@id='v-wrap']/div[@id='l-con']/div[@id='arc_toolbar_report']/div[@id='ops']/span[@id='collect']/text()")
####        item["分享:"] = html.xpath("/div[@id='app']/div[@id='v-wrap']/div[@id='l-con']/div[@id='arc_toolbar_report']/div[@id='ops']/span[@id='share']/text()")        
        if title:
            # 这里使用正则提取oid
            cid = re.findall(r"\"pages\"\:\[\{\"cid\":(.*?)\,", uu, re.S)[0]
        else:
            print("请输入正确的网址号")
        # 返回提取到的内容
        return cid

    # 解析弹幕url地址
    def get_danmu(self,cid):
        oid = cid
        # 拼接从html中获取到的oid
        danmu_url = "https://api.bilibili.com/x/v1/dm/list.so?oid={}".format(oid)
        # 发送请求
        response = requests.get(url=danmu_url,headers=self.headers)
        # 解析内容
        danmu_json = response.content.decode("utf-8")
        parse=parsel.Selector(danmu_json)
        # 使用xpath在xml中获取弹幕
        links=parse.xpath("//d/text()").getall()
        #print(links)
        for i in links:
            with open(r'E:/pythoncode/B站弹幕.csv','a',newline='',encoding='utf-8-sig') as f:
                writer=csv.writer(f)
                links=[]
                links.append(i)
                writer.writerow(links)
        # #制作词云图
        f =open(r'E:/pythoncode/B站弹幕.csv',encoding='utf-8')
        text=f.read()
        text_list=jieba.analyse.extract_tags(text,topK=100)
        text_list=" ".join(text_list)
        print(text_list)
        w=wordcloud.WordCloud(
            width=1500,
            height=1000,
            font_path="STXIHEI.TTF",
            background_color="white"
        )
        w.generate_from_text(text_list)
         
        #绘制图片
        fig=plt.figure(1)
        plt.imshow(w)
        plt.axis("off")
        plt.show()     #显示生成的词云文件
        # 返回获取到的弹幕
##        return item

    # 保存数据
##    def save(self,all):
##        # 保存为JSON格式到本地
##        with open("{}.json".format(self.name),"a",encoding="utf8") as fp:
##            fp.write(json.dumps(all,ensure_ascii=False,indent=4))

    def run(self):
        # 获取相应内容
        response = self.parse_url(self.av_url)
        # 提取所需数据
##        ii=self.get_information(response)
        item = self.get_course(response)
        self.get_danmu(item)
        # 保存数据为JSON格式到本地
##        self.save(all)

# 主方法
if __name__ == '__main__':
    # 输入av号，便于之后拼接
    av_num = input("请输入网址号:")
    # 传递参数
    bilibili = BiLiBiLi(av_num)
    # 调用方法
    bilibili.run()
