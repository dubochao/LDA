from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import time
import os
import csv
import json
import cookie
import random
import re
cookies,proxies = cookie.main()
#cookies= 'ALF=1584682452; SCF=Ao1AQDSyNMyR23TDx5xG_IJe2v4XqtrohlDD67o143N_ilDj19QP-Ffy2qe6e9RCYw2cmt-buWEsw2I7h1PUgm8.; SUB=_2A25zSLo0DeRhGeFM4lUZ9yrJwj6IHXVQssZ8rDV6PUJbktANLXfDkW1NQIfd1Q7IIALrtuY8yxDNe-TWrxqGr9QJ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh-dpVkFAo9J5yWOxXdB82b5JpX5K-hUgL.FoME1KMRS0Bf1Kz2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeo.N1hMXSK.E; SUHB=0rr7f9X9Ndnx8q; _T_WM=52236839197; XSRF-TOKEN=9d35ef; WEIBOCN_FROM=1110006030; MLOGIN=1'
import warnings
warnings.filterwarnings("ignore")
#cookies=None
base_url = 'https://m.weibo.cn/api/container/getIndex?'
agent1 = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
agent2 = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)'
agent3 = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)'
agent4='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11 '
agent5='Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)'

list1 = [agent1, agent2, agent3,agent4,agent5]
agent = random.choice(list1)
headers = {
    'Host': 'm.weibo.cn',
    #'Referer': 'https://m.weibo.cn/u/2830678474',
     'X-Requested-With': 'XMLHttpRequest',
    }
headers['User-Agent']=agent
headers['lb']='{}.{}.{}.{}'.format(str(random.randint(1,200)),str(random.randint(1,200)),str(random.randint(1,200)),str(random.randint(1,200)))
def get_page(page,title): #得到页面的请求，params是我们要根据网页填的，就是下图中的Query String里的参数
    #global proxies
    
    params = {
        'containerid': '100103type=1&q='+title,
        'page': page,#page是就是当前处于第几页，是我们要实现翻页必须修改的内容。
        'type':'all',
        'queryVal':title,
        'featurecode':'20000320',
        'luicode':'10000011',
        'lfid':'106003type=1',
        'title':title
    }
    url = base_url + urlencode(params)
    #print(url)
    try:
        response = requests.get(url, headers=headers,cookies=cookies,proxies=proxies,verify=False, allow_redirects=False)
        if response.status_code == 200:
            print("^微博_^ write success")
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

        
def count(title): #得到页面的请求，params是我们要根据网页填的，就是下图中的Query String里的参数
    params = {
        'containerid': '100103type=1&q='+title,
        'q':title,
        't':0
    }
    url = base_url + urlencode(params)
    
    try:
        response = requests.get(url,proxies=proxies,headers=headers,cookies=cookies,verify=False, allow_redirects=False)
        if response.status_code == 200:
            
            json= response.json()
            items = json.get('data').get('cards')
            
            for i in items:
                if i == None:
                    continue
                item = i.get('mblog')
                if item == None:
                    continue
                #t+=1
                weibo = {}
                #weibo['id'] = t
                weibo['support_count']  =item.get('attitudes_count') #赞同
                weibo['follow_count']=item.get('user').get('follow_count') #关注
                weibo['followers_count']=item.get('user').get('followers_count') #粉丝
                weibo['reposts_count']=item.get('reposts_count') #转发
                return weibo
    except requests.ConnectionError as e:
        print('Error', e.args)
def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, "", file)
    return chinese
def get_comments(id):
    """
    :weibo standardlized weibo
    :cur_count  已经下载的评论数
    :max_count 最大允许下载数
    :max_id 微博返回的max_id参数
    :on_downloaded 下载完成时的实例方法回调
    """
    #headers['Cookie']=cookies
    #print(headers)
    #id =  '4670594878808726'
    page=1
    url = "https://m.weibo.cn/api/comments/show?id={id}&page={page}".format(
        id=id,page=page)
    req = requests.get(url,headers=headers,cookies=cookies)
    #print(req.text)
    json = None
    try:
        json = req.json()
    except Exception as e:
        #没有cookie会抓取失败
        #logger.info(u'未能抓取评论 微博id:{id} 内容{text}'.format(id=id, text='text'))
        pass

    data = json.get('data')
    if not data:
        return
    comments = data.get('data')
    #count = len(comments)
    print(comments)
    return comments
    if count == 0:
        #没有了可以直接跳出递归
        return
# 解析接口返回的json字符串
def parse_page(json , label):
    res = []
    #print(json)
    if json:
        items = json.get('data').get('cards')
        
        for i in items:
            if i == None:
                continue
            item = i.get('mblog')
            if item == None:
                continue
            #t+=1
            weibo = {}
            #weibo['id'] = t
            weibo['label'] = label
            #print(items['created_at'])
            weibo['time'] =item.get('created_at')
            weibo['text'] = find_chinese(pq(item.get('text')).text())
            weibo['support_count']  =item.get('attitudes_count') #赞同
            weibo['follow_count']=item.get('user').get('follow_count') #关注
            weibo['followers_count']=item.get('user').get('followers_count') #粉丝
            weibo['id']=item.get('id') #转发
            res.append(weibo) 
    return res 
if __name__ == '__main__':
    #proxies=proxy_ip.ip().start()
    json = get_page(0 , '昆明“3.01”' )
    results = parse_page(json , '昆明“3.01”')
    import pandas as np
    print(count( '昆明“3.01”'))
    print(np.DataFrame( results)) 
    get_comments('4540778116546975')
