#!/usr/bin/env python
#coding:utf-8
import requests
import json
r = requests.get('http://127.0.0.1:8000/?')
ip_ports = json.loads(r.text)
print ip_ports
i = 0
https_ips = []
for ip_port in ip_ports:
    print ip_port
    ip = ip_port[0]
    port = ip_port[1]
    proxies={
        'https':'http://%s:%s'%(ip,port)
    }
    try:
        r = requests.get('https://list.jd.com/list.html?cat=9987,653,655',proxies=proxies, timeout=8)
        https_ips.append(ip_port)
    except requests.exceptions.RequestException:
        print 'cant access to JD!'
print len(https_ips)
print https_ips
