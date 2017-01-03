#!/usr/bin/env python
#coding:utf-8
'''
Varify if these proxies could access to jd.com.
Check the type of these proxies.
'''
import requests
import json
from lxml import etree

HEADER = {
    'User-Agent': r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.11",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
}
test_str = '\nThis request appears NOT to have come via a proxy.\n'

r = requests.get('http://127.0.0.1:8000/?')
ip_ports = json.loads(r.text)
print ip_ports
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
        'https':'http://%s:%s'%(ip,port)
    }
    try:
        jdr = requests.get('https://list.jd.com/list.html?cat=9987,653,655',headers=HEADER, proxies=proxies, timeout=6)
        if jdr.ok:
            https_ips.append(ip_port)
        '''
        r = requests.get(url='http://ipaddress.com/')
        if r.ok:
            root = etree.HTML(r.text)
            proxy = root.xpath('/html/body/div[1]/div[3]/div[2]/table/tr[6]/td/text()')[0]
            if proxy == 'No Proxy Detected':
                https_anony_ips.append(ip_port)
        '''
        r = requests.get(url='http://www.lagado.com/proxy-test',headers=HEADER,timeout=6,proxies=proxies)
        
        if r.ok:
            root = etree.HTML(r.text)
            proxy = root.xpath('//*[@id="summary"]/p[1]/text()')[0]
            print proxy
            if proxy==test_str:
                https_anony_ips.append(ip_port)
    except requests.exceptions.RequestException:
        print 'cant access to JD!'

print len(https_ips)
print https_ips
print https_anony_ips
