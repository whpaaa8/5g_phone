import os
import random
import sys
import time

import pandas as pd
import LDA
import comment
import preprocessing
import emotion_analysis
import LDA_analysis
from get_info import get
import API
import WordCloud
import yaml
import sel_comments

Ana = pd.read_csv('../data/phone/info/Analyze_phones.csv')
Ana.set_index('id',inplace=True)
def get_id(begin):
    path = '../data/phone/info/phones_info.csv'
    a = pd.read_csv(path)[['品牌','id']]
    a = a.loc[begin:]
    # b = a.groupby('品牌')
    # return list(b)
    return a

def API_mode(id):

    if id not in Ana.index.values:
        Ana.loc[id] = ['no', False]

    # id商品已经分析过则不再分析
    p = Ana.loc[id]['type']
    if p != 'no':
        print(id, ": Already been Analysis!")
        return

    #还没有评论的，获取评论
    print(id, ": Don't have comments!Now Get Comments!")
    # 爬取评论，并保存
    start_time = time.time()
    comment.get_comments(id)
    len = pd.read_csv("../data/phone/comment/comments_{}.csv".format(id)).shape[0]
    if len < 101: Ana.loc[id]['type'] = 'BAN'
    end_time = time.time()
    print("getComments Completed!", f" Use time:{end_time - start_time} seconds")

    if Ana.loc[id]['type'] == 'BAN': return


    # 百度API
    start_time = time.time()
    API.getWordsFromId(id)
    end_time = time.time()
    print("API Get Options Completed!", f" Use time:{end_time - start_time} seconds")

    #精选评论
    sel_comments.select_comments(id)

    #画词云图
    WordCloud.drawWordCloud(id)

    # 对评论进行LDA主题分析,将结果保存至../../data/phone/analysis/topic/.csv中
    start_time = time.time()
    LDA_analysis.lda_analyze(id)
    end_time = time.time()
    print("LDA analysis Completed!", f" Use time:{end_time - start_time} seconds")

def EMO_mode(id):

    # id商品已经分析过则不再分析
    if id not in Ana.index.values:
        Ana.loc[id] = ['no', False]

    p = Ana.loc[id]['type']
    if p != 'no':
        print(id, ": Already been Analysis!")
        return

    # 爬取评论，并保存
    start_time = time.time()
    comment.get_comments(id)
    end_time = time.time()
    len = pd.read_csv("../data/phone/comment/comments_{}.csv".format(id)).shape[0]
    if len < 101: Ana.loc[id]['type'] = 'BAN'
    print("getComments Completed!", f" Use time:{end_time - start_time} seconds")

    if Ana.loc[id]['type'] == 'BAN': return

    # 精选评论
    sel_comments.select_comments2(id)

    # 对评论进行分词，得出分词结果
    start_time = time.time()
    word = preprocessing.get_data(id)
    end_time = time.time()
    print("Word Segmentation Completed!", f" Use time:{end_time - start_time} seconds")

    # 对评论分词进行情感分析，返回好评 与 坏评,并保存好坏的词云图
    start_time = time.time()
    posdata, negdata = emotion_analysis.emotion_analyze(word,id)
    end_time = time.time()
    print("Sentiment analysis Completed!", f" Use time:{end_time - start_time} seconds")



    # 对评论进行LDA主题分析,将结果保存至../../data/phone/analysis/topic/.csv中
    start_time = time.time()
    LDA.lda_analyze(id,posdata,negdata)
    end_time = time.time()
    print("LDA analysis Completed!", f" Use time:{end_time - start_time} seconds")


def test():
    phones = get_id(0)
    for phone in phones:
        type = random.random()
        if type >= 0.3:
            EMO_mode(phone)
        else:
            API_mode(phone)


if __name__ == '__main__':
    # 读取YAML文件并转换为Python对象
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)

    # 读取参数
    # 是否更新
    update = config['info']['update']
    # 开始的索引
    begin = config['info']['begin']
    # 最大索引
    max = config['info']['max']
    num = max - begin
    if num == 0: sys.exit()
    #爬取手机id等信息
    if update :
        get()

    info = get_id(begin)
    phones = get_id(0)
    for phone in info:
        type = random.random()
        if type >= 0.3:
            EMO_mode(phone)
        else:
            API_mode(phone)
    # info = [ i[1] for i in info]
    # for i in info: i.reset_index(drop=True, inplace=True)
    # Api_info = []
    # emo_info = []
    # for i in info:
    #     l = i.shape[0]
    #     if l <= 10:
    #         Api_info.append(i[:l])
    #     else:
    #         Api_info.append(i[:10])
    # for i in info:
    #     l = i.shape[0]
    #     if l > 10:
    #         emo_info.append(i[10:])
    #
    # for info in Api_info:
    #     for id in info['id']:
    #         API_mode(id)
    # for info in emo_info:
    #     for id in info['id']:
    #         EMO_mode(id)

    Ana.to_csv("../data/phone/info/Analyze_phones.csv")
    # 将Python对象写回YAML文件
    config['info']['begin'] = config['info']["max"]
    with open('config.yml', 'w') as f:
        yaml.safe_dump(config, f)

