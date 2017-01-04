#!/usr/bin/env python
#coding:utf-8
'''
Varify if these proxies could access to jd.com.
Check the type of these proxies.
'''
import requests
import json
from lxml import etree
import config



def checkSites(proxies)
    
    sites = []
    try:
        jdr = requests.get('https://list.jd.com/list.html?cat=9987,653,655',headers=config.HEADER, proxies=proxies, timeout=6)
        if jdr.ok:
            sites.append("JD")
            print "jdr.ok"
        '''
        r = requests.get(url='http://www.lagado.com/proxy-test',headers=HEADER,timeout=6,proxies=proxies)
        
        if r.ok:
            root = etree.HTML(r.text)
            proxy = root.xpath('//*[@id="summary"]/p[1]/text()')[0]
            print proxy
            if proxy==test_str:
                https_anony_ips.append(ip_port)
        '''
    except requests.exceptions.RequestException:
        print 'cant access to JD!'

    return sites
