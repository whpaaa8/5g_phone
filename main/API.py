import csv
import random
import time

import pandas as pd
import requests
import json


API_KEY = "7bCXoMGqYz36rqzQKrSKaQj9"
SECRET_KEY = "PI7Y6KkGMC3Q7TbyjgKBCFbZMj04nw8M"
tt = -1


def write_csv(path, data):
    with open(path, 'a', encoding="utf8", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
def write_head(path, data):
    with open(path, 'w', encoding="utf8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

def get_data(comment):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v2/comment_tag?charset=UTF-8&access_token=24.74ff6fea50632f5c59cafa8ef53463fa.2592000.1686927109.282335-33667414"
    global  tt
    payload = json.dumps({
        "text": comment,
        "type": 13
    })
    headers = {
        ''
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(tt," success")
        return response.json()
    except Exception:
        # print(tt, " error")
        return {"error_code": "SSL error"}


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def analysis(comment,index):
    data = get_data(comment)

    # if (data == "error")
    # 名词
    n_words = []
    # 形容词
    a_words = []
    # 合起来的词
    words = []
    # 情感倾向
    sentiment = []
    # 积极的词
    pos_words = []
    # 消极词
    neg_words = []
    # 中立词
    neu_words = []
    # 所属句子
    i = []
    result = []
    if "error_code" not in data or data["error_code"] == 0:
        for item in data["items"]:
            n_words.append(item["prop"])
            a_words.append(item["adj"])
            s = item["prop"] + item["adj"]
            words.append(s)
            sentiment.append(item["sentiment"] - 1)
            # 积极的评论观点
            if item["sentiment"] == 2:
                pos_words.append(s)
                # print(u"    积极的评论观点: " + item["prop"] + item["adj"])
            # 中性的评论观点
            if item["sentiment"] == 1:
                neu_words.append(s)
                # print(u"    中性的评论观点: " + item["prop"] + item["adj"])
            # 消极的评论观点
            if item["sentiment"] == 0:
                neg_words.append(s)
                # print(u"    消极的评论观点: " + item["prop"] + item["adj"])
            i.append(index)

        for ii in range(len(words)):
            result.append([words[ii],n_words[ii],a_words[ii],sentiment[ii],index])
        # result = pd.DataFrame({"word":words,"n_words":n_words,"a_words":a_words,"sentiment":sentiment,"index_content":i})
        # print(result)
    else:
        # print error response
        print(data)

        # 防止qps超限
    # time.sleep(0.1)
    pos = [ j for j in zip(pos_words,i)]
    neg = [ j for j in zip(neg_words,i)]
    neu = [ j for j in zip(neu_words,i)]
    # print(result)
    return result,pos,neg,neu


def getWordsFromId(id):
    # 读取评论
    d =  pd.read_csv("../data/phone/comment/comments_{}.csv".format(id))
    comments = d['评论内容']
    # print(comments)
    global tt
    write_head("../data/phone/words/words/{}.csv".format(id),
               ['word', 'n_word', 'a_word', 'sentiment', 'index_content'])
    write_head("../data/phone/words/pos/{}.csv".format(id), ['word', 'text_content'])
    write_head("../data/phone/words/neg/{}.csv".format(id), ['word', 'text_content'])
    write_head("../data/phone/words/neu/{}.csv".format(id), ['word', 'text_content'])
    for index,comment in enumerate(comments):
        tt = tt +1
        # if (tt == 5): break
        # print(index,comments.loc[index, '评论内容'])
        # start_time = time.time()
        result, pos_words, neg_words, neu_words = analysis(comment, index)
        # end_time = time.time()
        # print(index, ": API", f" Use time:{end_time - start_time} seconds")

        write_csv("../data/phone/words/words/{}.csv".format(id),result)
        write_csv("../data/phone/words/pos/{}.csv".format(id),pos_words)
        write_csv("../data/phone/words/neg/{}.csv".format(id),neg_words)
        write_csv("../data/phone/words/neu/{}.csv".format(id),neu_words)
        # # print(result)
        # data.append(result)
        # pos.append(pos_words)
        # neg.append(neg_words)
        # neu.append(neu_words)




def test():
    id = "test1"
    getWordsFromId(id)

