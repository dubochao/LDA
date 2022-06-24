import requests as r
import random
class ip():
    def __init__(self,proxies=''):
        self.url='https://ip.jiangxianli.com/api/proxy_ips?page='+str(random.randint(1,3))
        self.header={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                     
                     'Connection': 'keep-alive'}
        self.header['X-Forwarded-For']='{}.{}.{}.{}'.format(str(random.randint(1,200)),str(random.randint(1,200)),str(random.randint(1,200)),str(random.randint(1,200)))
        #self.header['X-Forwarded-For']=self.header['Client-Ip']
        self.check='https://www.baidu.com/'
        
        self.proxies=proxies
    def start(self):
        self.header['Host']='ip.jiangxianli.com'
        result=r.get(url=self.url,headers=self.header,proxies=self.proxies, timeout=5)
        if result.status_code==200: 
            json1=result.json()['data']['data']
            random.shuffle(json1)
            for i in json1:
                proxies={i['protocol']:i['ip']+':'+i['port']}
                print(f'ip获取完毕：ip {proxies}')
                del self.header['Host']
                repons=r.get(url=self.check,headers=self.header,proxies=proxies,timeout=5 )
                if repons.status_code==200: 
                    return proxies
                else:
                    continue

                break
        else:
            proxies=''
            return proxies
if __name__=='__main__':
    ip=ip()
    for i in range(20):
        print(ip.start())
