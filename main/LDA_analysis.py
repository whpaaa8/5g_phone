import pandas as pd
import numpy as np
import re
import itertools

import pyLDAvis.sklearn
import pyLDAvis
import pyLDAvis.gensim_models
from gensim import corpora, models

import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

def lda_analyze(id):
    # 载入情感分析后的数据
    posdata = pd.read_csv("../data/phone/words/pos/{}.csv".format(id), encoding='utf-8')
    negdata = pd.read_csv("../data/phone/words/neg/{}.csv".format(id), encoding='utf-8')


    # 建立词典
    pos_dict = corpora.Dictionary([[i] for i in posdata['word']])  # 正面
    neg_dict = corpora.Dictionary([[i] for i in negdata['word']])  # 负面

    # 建立语料库
    pos_corpus = [pos_dict.doc2bow(j) for j in [[i] for i in posdata['word']]]  # 正面
    neg_corpus = [neg_dict.doc2bow(j) for j in [[i] for i in negdata['word']]]  # 负面

    #
    # print("pos_dict:",pos_dict)
    # print("neg_dict:",neg_dict)
    # print("pos_corpus",pos_corpus)
    # print("neg_corpus",neg_corpus)

    # 构造主题数寻优函数()
    def cos(vector1, vector2):  # 余弦相似度函数
        dot_product = 0.0;
        normA = 0.0;
        normB = 0.0;
        for a, b in zip(vector1, vector2):
            dot_product += a * b
            normA += a ** 2
            normB += b ** 2
        if normA == 0.0 or normB == 0.0:
            return (None)
        else:
            return (dot_product / ((normA * normB) ** 0.5))

        # 主题数寻优

    def lda_k(x_corpus, x_dict):
        # 初始化平均余弦相似度
        mean_similarity = []
        mean_similarity.append(1)

        # 循环生成主题并计算主题间相似度
        for i in np.arange(2, 11):
            lda = models.LdaModel(x_corpus, num_topics=i, id2word=x_dict)  # LDA模型训练

            term = lda.show_topics(num_words=50)
            # print(term)
            # 提取各主题词
            top_word = []
            for k in np.arange(i):
                # 匹配 主题中的主题词
                top_word.append([''.join(re.findall('"(.*)"', i)) \
                                 for i in term[k][1].split('+')])  # 列出所有词

            # 构造词频向量
            word = sum(top_word, [])  # 列出所有的词 所有主题词
            unique_word = set(word)  # 去除重复的词

            # 构造主题词列表，行表示主题号，列表示各主题词
            mat = []
            for j in np.arange(i):
                top_w = top_word[j]  # 第j个主题的所有词
                mat.append(tuple([top_w.count(k) for k in unique_word]))  # 表示所有主题词中第j个主题中出现的主题词

            # print(len(mat))
            # print(mat)
            p = list(itertools.permutations(list(np.arange(i)), 2))
            l = len(p)
            top_similarity = [0]
            for w in np.arange(l):
                vector1 = mat[p[w][0]]  # 主题一
                vector2 = mat[p[w][1]]  # 主题二
                # print(vector1, vector2)
                # 比较两个主题的相似度
                top_similarity.append(cos(vector1, vector2))

            # 计算平均余弦相似度
            mean_similarity.append(sum(top_similarity) / l)
            best_num = mean_similarity.index(min(mean_similarity)) + 2
        return (mean_similarity), best_num

    # # 计算主题平均余弦相似度
    pos_k, pos_num = lda_k(pos_corpus, pos_dict)
    neg_k, neg_num = lda_k(neg_corpus, neg_dict)
    # # 绘制主题平均余弦相似度图形
    # from matplotlib.font_manager import FontProperties
    #
    # font = FontProperties(size=14)
    # # 解决中文显示问题
    # plt.rcParams['font.sans-serif'] = ['SimHei']
    # plt.rcParams['axes.unicode_minus'] = False
    # fig = plt.figure(figsize=(10, 8))
    # ax1 = fig.add_subplot(211)
    # ax1.plot(pos_k)
    # ax1.set_xlabel('正面评论LDA主题数寻优', fontproperties=font)
    #
    # ax2 = fig.add_subplot(212)
    # ax2.plot(neg_k)
    # ax2.set_xlabel('负面评论LDA主题数寻优', fontproperties=font)
    # plt.show()

    # lda = LdaModel(corpus=corpus, id2word=dictionary, num_topics=4, passes=100)
    # num_topics：主题数目
    # passes：训练伦次
    # num_words：每个主题下输出的term的数目
    # LDA主题分析
    pos_lda = models.LdaModel(corpus=pos_corpus, num_topics=pos_num, id2word=pos_dict, passes=10)
    neg_lda = models.LdaModel(corpus=neg_corpus, num_topics=neg_num, id2word=neg_dict, passes=10)

    pos_data = pyLDAvis.gensim_models.prepare(pos_lda, pos_corpus, pos_dict)
    pyLDAvis.save_html(pos_data, '../data/phone/visualization/pos_lda_visualization_{}.html'.format(id))
    neg_data = pyLDAvis.gensim_models.prepare(neg_lda, neg_corpus, neg_dict)
    pyLDAvis.save_html(neg_data, '../data/phone/visualization/neg_lda_visualization_{}.html'.format(id))


    # 主题词
    pos_word = []
    # 主题词权重
    pos_weight = []
    # num_words=10：权值前10的关键字
    for topic in pos_lda.print_topics(num_words=5):
        termNumber = topic[0]
        # print(topic[0], ':', sep='')
        listOfTerms = topic[1].split('+')
        temp = []
        for term in listOfTerms:
            listItems = term.split('*')
            # print('  ', listItems[1], '(', listItems[0], ')', sep='')
            temp.append(eval(listItems[1]))
        pos_word.append(temp)

    pos_topics = pd.DataFrame(pos_word, index=([f'topic{i}' for i in range(1, pos_num + 1)]))
    pos_topics.to_csv("../data/phone/analysis/topic/pos_topics_{}.csv".format(id))

    neg_word = []
    neg_weight = []
    for topic in neg_lda.print_topics(num_words=10):
        termNumber = topic[0]
        # print(topic[0], ':', sep='')
        listOfTerms = topic[1].split('+')
        temp = []
        for term in listOfTerms:
            listItems = term.split('*')
            # print('  ', listItems[1], '(', listItems[0], ')', sep='')
            temp.append(eval(listItems[1]))
        neg_word.append(temp)

    neg_topics = pd.DataFrame(neg_word, index=([f'topic{i}' for i in range(1, neg_num + 1)]))
    neg_topics.to_csv("../data/phone/analysis/topic/neg_topics_{}.csv".format(id))



    # for k in np.arange(pos_num):
    #     # 匹配 主题中的主题词
    #     print(pos_lda[k][1])
    #     pos_word.append([''.join(re.findall('"(.*)"', i)) \
    #                      for i in pos_lda[k][1].split('+')])  # 列出所有词
    #     pos_weight.append([''.join(re.findall('(.*)\*"', i)) \
    #                        for i in pos_lda[k][1].split('+')])

    # 主题词权重
    # neg_weight = []
    # neg_word = []
    # for k in np.arange(neg_num):
    #     # 匹配 主题中的主题词
    #     neg_word.append([''.join(re.findall('"(.*)"', i)) \
    #                      for i in neg_lda[k][1].split('+')])  # 列出所有词
    #     neg_weight.append([''.join(re.findall('(.*)\*"', i)) \
    #                        for i in neg_lda[k][1].split('+')])





#测试单元
def test():
    # 载入情感分析后的数据
    id = 100037311057
    posdata = pd.read_csv("../data/phone/words/pos/test1.csv", encoding='utf-8')
    negdata = pd.read_csv("../data/phone/words/neg/test1.csv", encoding='utf-8')
    lda_analyze(id, posdata, negdata)




