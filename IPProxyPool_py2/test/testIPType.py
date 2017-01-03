#!/usr/bin/env python
#coding:utf-8
from lxml import etree
import requests
import json
import config

HEADER = {
    'User-Agent': r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.11",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
}

'''
用来检测代理的类型，突然发现，免费网站写的信息不靠谱，还是要自己检测代理的类型
:param proxies: 代理(0 高匿，1 匿名，2 透明 3 无效代理
:return:
'''
r = requests.get('http://127.0.0.1:8000/?')
ip_ports = json.loads(r.text)
print ip_ports
https_ips = []
test_str = '\nThis request appears NOT to have come via a proxy.\n'

for ip_port in ip_ports:
    print ip_port
    ip = ip_port[0]
    port = ip_port[1]
    
    proxies={
        'http':'http://%s:%s'%(ip,port),
        'https':'http://%s:%s'%(ip,port)
    }

    try:
        r = requests.get(url='http://www.lagado.com/proxy-test',headers=HEADER,timeout=6,proxies=proxies)
        
        if r.ok:
            root = etree.HTML(r.text)
            proxy = root.xpath('//*[@id="summary"]/p[1]/text()')[0]
            print proxy
            if proxy==test_str:
                https_ips.append(ip_port)
            
    except Exception,e:
        print str(e)

print len(https_ips)
print https_ips



