# 绘制词云
import random
import warnings

import pandas as pd

import stylecloud


warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore",category=DeprecationWarning)

def drawWordCloud(id):
    # 载入情感分析后的数据
    posdata = pd.read_csv("../data/phone/words/pos/{}.csv".format(id), encoding='utf-8')
    negdata = pd.read_csv("../data/phone/words/neg/{}.csv".format(id), encoding='utf-8')


    # 词云背景图的形状，随机选取一个
    icon = ['fas fa-cloud', 'fas fa-dog', 'fab fa-qq', 'fas fa-plane', 'fas fa-flag', 'fas fa-grin','fas fa-dove']

    # 读取数据
    element = list(posdata["word"])
    choices = [
               'cartocolors.qualitative.Bold_6','cartocolors.qualitative.Pastel_6',
               'cartocolors.qualitative.Prism_6','cartocolors.qualitative.Vivid_6']
    # for color in choices:
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
        font_path=r'msyh.ttc',
        output_name="../data/phone/wordcloud/neg_{}.jpg".format(id),
        icon_name=random.choice(icon),
        palette=random.choice(choices),
        background_color="black",
        # palette='colorbrewer.qualitative.Dark2_7',
    )


def test():
    id = "test"
    drawWordCloud(id)


