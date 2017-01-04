#coding:utf-8
import json
from multiprocessing import Process
import re
import gevent

from lxml import etree
import requests
import time
from config import TEST_URL, CHECK_SITES
import config
from db.DataStore import sqlhelper
from util.exception import Test_URL_Fail
#from test.testSites import checkSites


from gevent import monkey
monkey.patch_all()


def detect_from_db(myip,proxy,proxies_set):
    proxy_dict = {'ip':proxy[0],'port':proxy[1]}
    sites = detect_list(myip,proxy_dict)
    if sites:
        if proxy[2]<60000:
            score = proxy[2] + 1
        else:
            score = 60000
        proxy_str ='%s:%s'%(proxy[0],proxy[1])
        proxies_set.add(proxy_str)
        sqlhelper.update({'ip':proxy[0],'port':proxy[1]},{'score':score,'sites':sites})
    else:
        sqlhelper.delete({'ip':proxy[0],'port':proxy[1]})


    pass


def validator(queue1,queue2):
    tasklist=[]
    myip = getMyIP()
    while True:
        try:
            # proxy_dict = {'source':'crawl','data':proxy}
            proxy = queue1.get(timeout=10)
            tasklist.append(proxy)
            if len(tasklist)>500:
                p = Process(target=process_start,args=(tasklist,myip,queue2))
                p.start()
                tasklist=[]
        except Exception,e:
            if len(tasklist)>0:
                p = Process(target=process_start,args=(tasklist,myip,queue2))
                p.start()
                tasklist=[]


def process_start(tasks,myip,queue2):
    spawns = []
    for task in tasks:
        spawns.append(gevent.spawn(detect_list,myip,task,queue2))
    gevent.joinall(spawns)


def detect_list(selfip,proxy,queue2=None):
    '''
    :param proxy: ip字典
    :return:
    '''
    ip = proxy['ip']
    port = proxy['port']
    proxies={"http": "http://%s:%s"%(ip,port),"https": "http://%s:%s"%(ip,port)}
    
    start = time.time()
    sites = None
    try:
        r = requests.get(url=TEST_URL,headers=config.HEADER,timeout=config.TIMEOUT,proxies=proxies)

        if not r.ok or r.text.find(ip)==-1:
            proxy = None
        else:
            speed = round(time.time()-start,2)
            proxy['speed']=speed
            proxyType = checkProxyType(selfip,proxies)
            proxy['types'] = proxyType
            sites = checkSites(proxies, CHECK_SITES)
            proxy['sites'] = sites
            '''
            if proxyType==3:
                logger.info('failed %s:%s'%(ip,port))
                #目前找到的测代理的都是国外网站访问不稳定，应该以国内网站测试作为是否可用的依据
                #proxy = None
                queue2.put(proxy)
                return proxy
            else:
                proxy['types']=proxyType
            '''
            
    except Exception,e:
            proxy = None

    if queue2:
        queue2.put(proxy)
    return sites

def checkProxyType(selfip,proxies):
    '''
    用来检测代理的类型，突然发现，免费网站写的信息不靠谱，还是要自己检测代理的类型
    用的是腾讯服务器很多国外网站无法访问，试了很多找到一个目前能用的网站:'http://www.lagado.com/proxy-test'
    发现在校园网内国际出口ip和国内出口ip是不同的
    还没有细分析是检测网站返回的信息，粗略分为两种
    :param proxies: 代理(0 匿名，1 透明
    :return:
    '''

    try:
        test_str = '\nThis request appears NOT to have come via a proxy.\n'
        r = requests.get(url=config.TEST_PROXY,headers=config.HEADER,timeout=config.TIMEOUT,proxies=proxies)
        if r.ok:
            root = etree.HTML(r.text)
            proxy = root.xpath('//*[@id="summary"]/p[1]/text()')[0]
            #print proxy
            if proxy==test_str:
                return '0'
            else:
                return '1'
        return '3'

    except Exception,e:
        #print 'The proxy test website becomes invalid! or not'
        return '3'


def checkSites(proxies, CHECK_SITES):
    '''
    #检查对特定网站能否访问,若能访问，将CHECK_SITES词典里的键值标记到一个可访问一个数组里
    '''
    sites = []
    for key, value in CHECK_SITES.iteritems():
        print value
        try:
            r = requests.get(url=value,headers=config.HEADER,timeout=config.TIMEOUT,proxies=proxies)
            if r.ok:
                sites.append(key)
        except Exception,e:
            pass
    return sites

def getMyIP():
    try:
        r = requests.get(url=config.TEST_URL,headers=config.HEADER,timeout=config.TIMEOUT)
        pattern = '\d+\.\d+\.\d+\.\d+'
        match =re.search(pattern,r.text)
        if match:
            ip = match.group()
            return ip
        else:

            raise Test_URL_Fail
    except Exception,e:
            raise Test_URL_Fail

if __name__=='__main__':
    getMyIP()
    # str="{ip:'61.150.43.121',address:'陕西省西安市 西安电子科技大学'}"
    # j = json.dumps(str)
    # str = j['ip']
    # print str