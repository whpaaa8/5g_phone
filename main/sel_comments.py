import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#箱线图法去除异常值
def boxplot(data):
    # 绘制箱线图
    # plt.scatter(data.index.values, data['weight'],linewidths=1)
    # plt.ylabel('emotion')
    # plt.xlabel("index")
    plt.boxplot(data['weight'])
    plt.show()
    # 计算上下限
    Q1 = data['weight'].quantile(0.25)
    Q3 = data['weight'].quantile(0.75)
    IQR = Q3 - Q1
    upper_limit = Q3 + 1.5 * IQR
    lower_limit = Q1 - 1.5 * IQR
    # print(lower_limit,upper_limit)
    # 剔除异常值
    data = data[(data['weight'] >= lower_limit) & (data['weight'] <= upper_limit)]

    # 输出剔除异常值后的数据
    # print('剔除异常值后的数据：\n', data)
    # print(len(data))
    return data

def draw(y):
    a = np.array(y['weight'])
    l = y.shape[0]
    x = [i for i in range(0,l)]
    plt.scatter(x,a)
    plt.show()

#使用API的
def select_comments(id):
    #消极评论
    neg = pd.read_csv("../data/phone/words/neg/{}.csv".format(id))
    neg['weight'] = -1
    #积极评论
    pos = pd.read_csv("../data/phone/words/pos/{}.csv".format(id))
    pos['weight'] = 1
    #合并
    comment = pd.read_csv("../data/phone/comment/comments_{}.csv".format(id))
    df = pd.concat([neg, pos])
    #计算每个评论的情感值
    emotional_value = df.groupby(['text_content'],
                                               as_index=False)['weight'].sum()
    type = []
    for i in emotional_value['text_content']:
        type.append(comment.loc[int(i)]['评论类型'])
    emotional_value['type'] = type
    print(emotional_value)
    emotional_value = boxplot(emotional_value)

    data = emotional_value.groupby(['type'])['weight']
    avg = data.mean()

    type = list(set(emotional_value['type']))

    data = pd.DataFrame(columns=['text_content','weight','type'])
    # print(data)
    for t in type:
        result = emotional_value.loc[(emotional_value['type'] == t) & (abs(emotional_value['weight'] - avg[t]) < 1)].head(10)
        data = pd.concat([data,result])
    # print(data)

    comment = comment.loc[data['text_content']]
    comment.to_csv("../data/phone/comment/sel/{}.csv".format(id),index = False)

#使用情感分析法
def select_comments2(id):
    comment = pd.read_csv("../data/phone/comment/comments_{}.csv".format(id))
    result =[]
    try:
        result = comment.groupby('评论类型',as_index=False).apply(lambda x: x.sample(n=10))
    except:
        comment_good = comment[comment['评论类型'] == '好评']
        comment_media = comment[comment['评论类型'] == '中评']
        comment_bad = comment[comment['评论类型'] == '差评']
        if comment_good.shape[0] > 10:
            comment_good =comment_good.sample(n=10)
        if comment_good.shape[0] > 10:
            comment_good =comment_good.sample(n=10)
        if comment_good.shape[0] > 10:
            comment_good =comment_good.sample(n=10)
        result = pd.concat([comment_good,comment_media,comment_bad])
    result.to_csv("../data/phone/comment/sel/{}.csv".format(id),index=False)
    # print(result)


def test():
    select_comments("test")

