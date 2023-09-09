import os
import time

import requests
import logging

import yaml
from bs4 import BeautifulSoup
import csv
import pandas as pd
import folder
from scrapy import Selector
# 运行程序时 商品图片要下载到文件夹./image/中并且命名为phone_id.png  csv里面要存放路径./image/phone_id.png

def get():

    if not os.path.exists("../data/phone/info/image"):
        folder.create_folder("../data/phone/info/image")
    f = open('../data/phone/info/phones_info.csv', mode='a', encoding='utf-8', newline='')
    exists_id = []
    try:
        exists_id = pd.read_csv('../data/phone/info/phones_info.csv')['id'].tolist()
    except:
        print("empty info!First time get info!")

    l = len(exists_id)
    csv_writer = csv.DictWriter(f, fieldnames=[
            '品牌',
            'id',
            '手机名称',
            '价格',
            '图片',
            '链接'
    ])
    if l == 0: csv_writer.writeheader()

    addresses = ['https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BA%20vivo&enc=utf-8&wq=5g%E6%89%8B%E6%9C%BA%20vivo&pvid=dd56711be1de47a09d58b941570ffaa4&psort=4',#vivo
             'https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BA%20oppo&enc=utf-8&wq=5g%E6%89%8B%E6%9C%BA%20oppo&pvid=99cd6a17597545cc969a3358d7d64a55&psort=4',  # oppo
             'https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BA%20%E5%8D%8E%E4%B8%BA&enc=utf-8&wq=5g%E6%89%8B%E6%9C%BA%20%E5%8D%8E%E4%B8%BA&pvid=8579760ba7e34ca9be3495619b2ed68e&psort=4',  # 华为
             'https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BA%20Apple&qrst=1&wq=5g%E6%89%8B%E6%9C%BA%20Apple&ev=exbrand_Apple%5E&pvid=1212c6771d38458191bc716e4fb1f388&psort=4&click=0',   #apple
             'https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BA%20%E5%B0%8F%E7%B1%B3&enc=utf-8&wq=5g%E6%89%8B%E6%9C%BA%20%E5%B0%8F%E7%B1%B3&pvid=6275cfb8242b4acab7dbacc335b44b50&psort=4',  # 小米
             'https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BA%20%E8%8D%A3%E8%80%80&enc=utf-8&wq=5g%E6%89%8B%E6%9C%BA%20%E8%8D%A3%E8%80%80&pvid=0abb373971254df28a31820551d0a511&psort=4',  # 荣耀
             'https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BA%20%E7%BA%A2%E7%B1%B3&enc=utf-8&wq=5g%E6%89%8B%E6%9C%BA%20%E7%BA%A2%E7%B1%B3&pvid=f553b76ea26648b690b5bc44f9fe7be9&psort=4',  # 红米
             'https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BA%20iqoo&enc=utf-8&wq=5g%E6%89%8B%E6%9C%BA%20iqoo&pvid=edf61f3c0d174b66b3a1a3c4389e41b7&psort=4',  # iqoo
             'https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BA%E4%B8%80%E5%8A%A0&enc=utf-8&wq=5g%E6%89%8B%E6%9C%BA%E4%B8%80%E5%8A%A0&pvid=b408790066e941958ac782d198fc71d0&psort=4',  # 一加
             'https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BArealme&enc=utf-8&wq=5g%E6%89%8B%E6%9C%BArealme&pvid=c2ee0ed200aa4e55a3c1a4aa817e38bc&psort=4',  # realme
             'https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BA%E4%B8%89%E6%98%9F&enc=utf-8&wq=5g%E6%89%8B%E6%9C%BA%E4%B8%89%E6%98%9F&pvid=7e76fdbf67ce4047a126b19779de5fd6&psort=4',  # 三星
             'https://search.jd.com/Search?keyword=5g%E6%89%8B%E6%9C%BA%E9%AD%85%E6%97%8F&enc=utf-8&wq=5g%E6%89%8B%E6%9C%BA%E9%AD%85%E6%97%8F&pvid=5f82193ca89346788894b21de4b623c2&psort=4']  # 魅族

    brands = ['vivo','oppo','华为','Apple','小米','荣耀','红米','iqoo','一加','realme','三星','魅族']

    idd = []
    def get_img(img_list, id_list):
        # os.makedirs('./image/' + keyword, exist_ok=True)
        header = {  # 模拟浏览器头部信息，向京东服务器发送消息
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42"
        }
        for i in range(len(img_list)):
            img = img_list[i]
            id = id_list[i]
            img_url = 'http:' + img  # 图片下载网址
            # print('http:' + img)
            r = requests.get(img_url, headers=header, stream=True)  # 下载图片
            with open(f'../data/phone/info/image/' + str(id) + '.png', 'wb') as f:  # 打开文件夹存放图片 并且命名为phone_id.png
                for chunk in r.iter_content(chunk_size=32):
                    f.write(chunk)

            # print("download: img" + str(id))

    for order in range(0,12):
        print(order)
        time.sleep(2)
        response = requests.get(addresses[order])
        # print(response.text)
        # 创建beatutifulsoup4解析器对象
        soup = BeautifulSoup(response.text, 'html.parser')
        bs = BeautifulSoup(response.text, "lxml")
        htmls1 = soup.find_all("div", class_="p-img", attrs={})
        htmls2 = soup.find_all("div", class_="p-name p-name-type-2", attrs={})
        htmls3 = soup.find_all("div", class_="p-price", attrs={})
        # htmls4 = soup.find_all("div", class_="p-img", attrs={})
        htmls4 = bs.find_all(class_="gl-item")

        id_list = []        # id
        name_list = []      # 手机名称
        price_list = []    # 价格
        img_list = []   # 图片在文件夹中的路径
        link_list = []  # 链接
        exists_list = []
        for html in htmls1:
            id = html.a.get('href').replace('//item.jd.com/', '').replace('.html?bbtf=1', '')
            # print(type(id))
            if int(id) in exists_id or id in idd:
                exists_list.append(False)
                print(brands[order],id)
                continue
            id_list.append(id)
            link_list.append("https:"+html.a.get('href'))
            exists_list.append(True)
            idd.append(id)
        print(brands[order],len(id_list))
        for i,html in enumerate(htmls2):
            if not exists_list[i]: continue
            s = html.a.em.text
            name_list.append(s.replace('\n', ' '))

        for i,html in enumerate(htmls3):
            if not exists_list[i]: continue
            price_list.append('￥'+html.i.text)  # 也就是 ￥+ 数字

        for i,html in enumerate(htmls4):
            if not exists_list[i]: continue
            li_soup = BeautifulSoup(str(html), 'lxml')
            img_url = li_soup.find("img")['data-lazy-img']
            img_list.append(img_url)
        print(brands[order], len(img_list))
        get_img(img_list, id_list)

        b = brands[order]
        l = len(id_list)
        if b == "realme" : l = 20
        if b == "魅族" : l = 5
        for order1 in range(0,l):
            dit = {
                '品牌': brands[order],
                'id': id_list[order1],
                '手机名称': name_list[order1],
                '价格': price_list[order1],
                '图片': 'image/' + str(id_list[order1]) + '.png',  # img_list[order1],
                '链接': link_list[order1]
            }
            csv_writer.writerow(dit)




        # Data = pd.read_csv('twelve types of phones.csv')
        # Data['id'] = id_list
        # Data['手机名称'] = name_list
        # Data['价格'] = price_list
        # Data.to_csv('twelve types of phones.csv',index=False)
        '''for i in name_list:
            dit = {
                '手机名称':i
            }
            csv_writer.writerow(dit)
         '''
    f.close()
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)
    data = pd.read_csv("../data/phone/info/phones_info.csv")
    config['info']["max"] = data.shape[0]
    # 将Python对象写回YAML文件
    with open('config.yml', 'w') as f:
        yaml.safe_dump(config, f)
    # data = pd.read_csv("../data/phone/info/phones_info.csv")
    # print(data.shape)
    # data.drop_duplicates(subset='id', inplace=True)
    # data.to_csv("../data/phone/info/phones_info.csv",index=False)
    # print(data.shape)

def test():
    get()

