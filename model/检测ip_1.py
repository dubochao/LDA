# coding:utf-8
# version:python3.7
# author:Ivy
import requests
import re
import json
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
        
        'Accept-Encoding': 'gzip, deflate'}

url='https://2021.ip138.com/'
list1=[{'https': '221.122.91.65:80'}, {'https': '221.122.91.61:80'}, {'https': '221.122.91.60:80'}, {'https': '61.160.210.223:808'}, {'https': '221.122.91.66:80'}, {'https': '218.60.8.99:3129'}, {'https': '218.60.8.83:3129'}, {'https': '221.122.91.59:80'}, {'https': '61.160.210.234:808'}, {'https': '221.122.91.74:9401'}]

ip=[]
for i in list1:
    #print(proxies)
    print('正在监测:',i)
    try:
        repons=requests.get(url=url,headers=headers,timeout=1,proxies=i)
        
        #print(repons.text)
        #repons=requests.get(url=url,headers=headers,proxies=proxies,timeout=1 )
    #with open ('ip.html','w', encoding='utf-8') as fp:
    #    fp.write(repons.text)
        if repons.status_code==200:
            print('success',i)
            ip.append(i)
            #print('2222',ip)
    except:
        pass
print(ip)
