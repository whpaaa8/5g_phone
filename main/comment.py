import csv
import time
import random
import pandas as pd
import requests


com_type = ['全部评论', '差评', '中评', '好评', '晒图评价', '追评']
path = "../data/phone/comment/"
user_agents = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
        'Opera/8.0 (Windows NT 5.1; U; en)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
    ]
# 将不同页面的url处理
def params_data(id_url, num1, num2):
    params_list = []
    list_data = [i for i in range(num1, num2 + 1)]
    random.shuffle(list_data)
    for score in range(1, 6):
        for page in list_data:
            par = '?productId={}&score={}&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(id_url,
                                                                                                            score,
                                                                                                            page)
            params_list.append(par)

    return params_list


# 合并为url
def join_ulr(url, params_list):
    data_url = []
    for i in params_list:
        new_url = url + i
        data_url.append(new_url)
    return data_url


def get_url_save(id, url_list, fu_ip=None):
    headers = {
        'User-Agent': str(random.choice(user_agents))
    }
    make_file(id)
    for k in url_list:
        data = []
        time.sleep(1)
        try:
            response = requests.get(url=k, headers=headers, proxies=fu_ip)
            response_data = response.json()
        except:
            print('遭到反爬了', k)
            time.sleep(3)
            # fu_ip = ip
        # 有时候返回数据，但是没有 comments，会导致报错，所以这里捕获一下错误
        try:
            if response_data['comments'] == [] : raise Exception()
            if response_data['comments']:
                a = com_type[response_data['score']]
                for i in response_data['comments']:
                    comment_data = [a, i['id'], i['nickname'], i['content'].replace("\n", " "), i['creationTime']]
                    data.append(comment_data)
                # print(data)

            write_csv(id, data)
        except:
            # print('无评论:'+k)
            continue


def make_file(goods_id):
    with open(path+"comments_{}.csv".format(goods_id), 'w', encoding="utf8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['评论类型', '用户id', '用户名', '评论内容', '时间'])


def write_csv(goods_id, data):
    with open(path+"comments_{}.csv".format(goods_id), 'a', encoding="utf8", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def get_comments(id):
    u = 'https://club.jd.com/comment/productPageComments.action'

    # 获取0-100页的评论
    url_list = params_data(id, 0, 100)
    # 获取准确的url
    url_list = join_ulr(u, url_list)

    # 爬取评论并存
    get_url_save(id, url_list)
    data = pd.read_csv(path+"comments_{}.csv".format(id))
    data.drop_duplicates(subset='评论内容',inplace=True)
    data.to_csv(path+"comments_{}.csv".format(id))

#测试单元
def test():
    get_comments()

# start_time = time.time()
# test()
# print("UseTime:",time.time()-start_time)