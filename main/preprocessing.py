import numpy as np
import pandas as pd
import re
import jieba.posseg as psg
import warnings
import PIL.Image as image


def preprocessing(id):
    warnings.filterwarnings("ignore")
    reviews = pd.read_csv('../data/phone/comment/comments_{}.csv'.format(id))

    # print(reviews.shape)
    # 删除数据记录中所有列值相同的记录
    reviews = reviews[['评论内容', '评论类型']].drop_duplicates()

    content = reviews['评论内容']
    # print(reviews)
    # print(reviews.shape)

    strinfo = re.compile('[0-9a-zA-Z]|京东|手机|')
    content = content.apply(lambda x: strinfo.sub('', x))

    # 分词
    worker = lambda s: [(x.word, x.flag) for x in psg.cut(s)]  # 自定义简单分词函数
    seg_word = content.apply(worker)
    # 将词语转为数据框形式，一列是词，一列是词语所在的句子ID，最后一列是词语在该句子的位置
    n_word = seg_word.apply(lambda x: len(x))  # 每一评论中词的个数

    n_content = [[x + 1] * y for x, y in zip(list(seg_word.index), list(n_word))]

    # 将嵌套的列表展开，作为词所在评论的id
    index_content = sum(n_content, [])
    seg_word = sum(seg_word, [])
    # 词
    word = [x[0] for x in seg_word]
    # 词性
    nature = [x[1] for x in seg_word]
    content_type = [[x] * y for x, y in zip(list(reviews['评论类型']), list(n_word))]
    # 评论类型
    content_type = sum(content_type, [])
    result = pd.DataFrame({"index_content": index_content,
                           "word": word,
                           "nature": nature,
                           "content_type": content_type})

    # 删除标点符号
    result = result[result['nature'] != 'x']  # x表示标点符号

    # 删除停用词
    stop_path = open("../data/other/cn_stopwords.txt", 'r', encoding='UTF-8')
    stop = stop_path.readlines()
    stop = [x.replace('\n', '') for x in stop]
    word = list(set(word) - set(stop))
    result = result[result['word'].isin(word)]

    # 构造各词在对应评论的位置列
    n_word = list(result.groupby(by=['index_content'])['index_content'].count())
    index_word = [list(np.arange(0, y)) for y in n_word]
    index_word = sum(index_word, [])  # 表示词语在改评论的位置

    # 合并评论id，评论中词的id，词，词性，评论类型
    result['index_word'] = index_word
    # print(result)
    return result
    # 将词汇分词表保存在word.csv中作为字典与语料库
    # result.to_csv("../data/phone/analysis/word_{}.csv".format(id),index=False)
    # draw(result, id)


# def draw(result, id):
#     # print(result)
#     # 词云
#     from wordcloud import WordCloud
#     frequencies = result.groupby(by=['word'])['word'].count()
#     frequencies = frequencies.sort_values(ascending=False)
#
#     backgroud_Image = np.array(image.open("../data/other/background.jpg"))
#     wordcloud = WordCloud(font_path="msyh.ttc",
#                           max_words=100,
#                           background_color='white',
#                           mask=backgroud_Image)
#     my_wordcloud = wordcloud.fit_words(frequencies)
#     # 保存图片
#     wordcloud.to_file("./wordcloud/{}.jpg".format(id))
#     # import matplotlib.pyplot as plt
#     # import seaborn as sns
#     # plt.imshow(my_wordcloud)
#     # plt.axis('off')
#     # plt.show()


def get_data(id):
    return preprocessing(id)


def test():
    get_data()
