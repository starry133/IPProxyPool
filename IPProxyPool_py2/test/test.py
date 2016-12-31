#!/usr/bin/env python
#coding:utf-8
'''
Varify if these proxies could access to jd.com.
Check the type of these proxies.
'''
import requests
import json
from lxml import etree

r = requests.get('http://127.0.0.1:8000/?')
ip_ports = json.loads(r.text)
print ip_ports
i = 0
https_ips = []
https_anony_ips = []
for ip_port in ip_ports:
    print ip_port
    ip = ip_port[0]
    port = ip_port[1]
    '''
    proxies={
        'https':'http://%s:%s'%(ip,port)
    }
    '''
    proxies={
        'http':'http://%s:%s'%(ip,port),
        'https':'https://%s:%s'%(ip,port)
    }
    try:
        requests.get('https://list.jd.com/list.html?cat=9987,653,655',proxies=proxies, timeout=6)
        https_ips.append(ip_port)
        
        r = requests.get(url='http://ipaddress.com/')
        root = etree.HTML(r.text)
        proxy = root.xpath('/html/body/div[1]/div[3]/div[2]/table/tr[6]/td/text()')[0]
        if proxy == 'No Proxy Detected':
            https_anony_ips.append(ip_port)
    except requests.exceptions.RequestException:
        print 'cant access to JD!'

print len(https_ips)
print https_ips
print https_anony_ips
