
import pandas as pd
import numpy as np
import random
import stylecloud



def emotion_analyze(word, id):
    # word = pd.read_csv("../data/phone/analysis/word.csv")

    # 读入正面、负面情感评价词
    pos_comment = pd.read_csv("../data/phone/analysis/正面评价词语（中文）.txt", header=None, sep="/n",
                              encoding='gbk', engine='python')
    neg_comment = pd.read_csv("../data/phone/analysis/负面评价词语（中文）.txt", header=None, sep="/n",
                              encoding='gbk', engine='python')
    pos_emotion = pd.read_csv("../data/phone/analysis/正面情感词语（中文）.txt", header=None, sep="/n",
                              encoding='gbk', engine='python')
    neg_emotion = pd.read_csv("../data/phone/analysis/负面情感词语（中文）.txt", header=None, sep="/n",
                              encoding='gbk', engine='python')

    # print(pos_comment.head(20))
    # 合并情感词与评价词
    positive = set(pos_comment.iloc[:, 0]) | set(pos_emotion.iloc[:, 0])
    negative = set(neg_comment.iloc[:, 0]) | set(neg_emotion.iloc[:, 0])
    intersection = positive & negative  # 正负面情感词表中相同的词语
    positive = list(positive - intersection)
    negative = list(negative - intersection)
    positive = pd.DataFrame({"word": positive,
                             "weight": [1] * len(positive)})
    negative = pd.DataFrame({"word": negative,
                             "weight": [-1] * len(negative)})

    posneg = pd.concat([positive, negative])

    #  将分词结果与正负面情感词表合并，定位情感词
    data_posneg = posneg.merge(word, left_on='word', right_on='word',
                               how='right')
    data_posneg = data_posneg.sort_values(by=['index_content', 'index_word'])

    # 根据情感词前时候有否定词或双层否定词对情感值进行修正
    # 载入否定词表
    notdict = pd.read_csv("../data/phone/analysis/not_word.csv")

    # 处理否定修饰词
    data_posneg['amend_weight'] = data_posneg['weight']  # 构造新列，作为经过否定词修正后的情感值
    data_posneg['id'] = np.arange(0, len(data_posneg))
    only_inclination = data_posneg.dropna()  # 只保留有情感值的词语
    only_inclination.index = np.arange(0, len(only_inclination))
    index = only_inclination['id']

    # print(only_inclination)
    # print(notdict)

    for i in np.arange(0, len(only_inclination)):
        review = data_posneg[data_posneg['index_content'] ==
                             only_inclination['index_content'][i]]  # 提取第i个情感词所在的评论
        review.index = np.arange(0, len(review))
        affective = only_inclination['index_word'][i]  # 第i个情感值在该文档的位置
        if affective == 1:
            ne = sum([i in notdict['term'] for i in review['word'][affective - 1]])
            if ne == 1:
                data_posneg['amend_weight'][index[i]] = - \
                    data_posneg['weight'][index[i]]
        elif affective > 1:
            ne = sum([i in notdict['term'] for i in review['word'][[affective - 1,
                                                                    affective - 2]]])
            if ne == 1:
                data_posneg['amend_weight'][index[i]] = - \
                    data_posneg['weight'][index[i]]

    # 更新只保留情感值的数据
    only_inclination = only_inclination.dropna()

    # 计算每条评论的情感值
    emotional_value = only_inclination.groupby(['index_content'],
                                               as_index=False)['amend_weight'].sum()

    #
    # 去除情感值为0的评论
    emotional_value = emotional_value[emotional_value['amend_weight'] != 0]
    # 给情感值大于0的赋予评论类型（content_type）为pos,小于0的为neg
    emotional_value['a_type'] = ''
    emotional_value.loc[emotional_value['amend_weight'] > 0, 'a_type'] = 'pos'
    emotional_value.loc[emotional_value['amend_weight'] < 0, 'a_type'] = 'neg'

    # print(emotional_value)
    # 查看情感分析结果
    result = emotional_value.merge(word,
                                   left_on='index_content',
                                   right_on='index_content',
                                   how='left')

    result = result[['index_content', 'content_type', 'a_type']].drop_duplicates()
    confusion_matrix = pd.crosstab(result['content_type'], result['a_type'],
                                   margins=True)  # 制作交叉表
    (confusion_matrix.iat[0, 0] + confusion_matrix.iat[1, 1]) / confusion_matrix.iat[2, 2]

    # 提取正负面评论信息
    ind_pos = list(emotional_value[emotional_value['a_type'] == 'pos']['index_content'])
    ind_neg = list(emotional_value[emotional_value['a_type'] == 'neg']['index_content'])
    posdata = word[[i in ind_pos for i in word['index_content']]]
    negdata = word[[i in ind_neg for i in word['index_content']]]


    # 词云背景图的形状，随机选取一个
    icon = ['fas fa-cloud', 'fas fa-dog', 'fab fa-qq', 'fas fa-plane', 'fas fa-flag', 'fas fa-grin','fas fa-dove']

    # 读取数据
    element = list(posdata["word"])
    choices = [
        'cartocolors.qualitative.Bold_6', 'cartocolors.qualitative.Pastel_6',
        'cartocolors.qualitative.Prism_6', 'cartocolors.qualitative.Vivid_6']

    stylecloud.gen_stylecloud(
        text=' '.join(element),  # 分词用" "隔开
        size=2048,
        collocations=False,
        palette=random.choice(choices),
        # palette=color,
        font_path=r'msyh.ttc',
        output_name="../data/phone/wordcloud/pos_{}.jpg".format(id),
        icon_name=random.choice(icon),
        background_color="black",
        # palette='colorbrewer.qualitative.Dark2_7',
    )
    # 读取数据
    element = list(negdata["word"])
    stylecloud.gen_stylecloud(
        text=' '.join(element),  # 分词用" "隔开
        size=2048,
        collocations=False,
        palette=random.choice(choices),
        # palette=color,
        font_path=r'msyh.ttc',
        output_name="../data/phone/wordcloud/neg_{}.jpg".format(id),
        icon_name=random.choice(icon),
        background_color="black",
        # palette='colorbrewer.qualitative.Dark2_7',
    )


    return posdata, negdata
    # 将结果写出，每条评论作为一行
    # posdata.to_csv("posdata.csv", index=False, encoding='utf-8')
    # negdata.to_csv("negdata.csv", index=False, encoding='utf-8')


def test():
    word = pd.read_csv("../data/phone/analysis/word_test.csv")
    id = 100037311057
    emotion_analyze(word,id)

