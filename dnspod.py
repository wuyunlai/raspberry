#!/usr/bin/env python
#-*- coding:utf-8 -*-
 
import httplib, urllib
import socket
import time
 
params = dict(
    login_email="wuyunlai@163.com", # replace with your email
    login_password="qoiqwe198123", # replace with your password
    format="json",
    #curl curl -k https://dnsapi.cn/Domain.List -d "login_email=wuyunlai@163.com&login_password=qoiqwe198123"
    domain_id=39960861, # replace with your domain_od, can get it by API Domain.List
    #curl -k https://dnsapi.cn/Record.List -d "login_email=wuyunlai@163.com&login_password=qoiqwe198123&domain_id=39960861"
    record_id=201279720, # replace with your record_id, can get it by API Record.List
    sub_domain="@", # replace with your sub_domain
    #record_id=201562621
    #sub_domain="*"
    record_line="Ĭ��",
)
current_ip = None
 
def ddns(ip):
    params.update(dict(value=ip))
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request("POST", "/Record.Ddns", urllib.urlencode(params), headers)
     
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    conn.close()
    return response.status == 200
 
def getip():
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
    return ip
 
if __name__ == '__main__':
    while True:
        try:
            ip = getip()
            print ip
            if current_ip != ip:
                if ddns(ip):
                    current_ip = ip
        except Exception, e:
            print e
            pass
        time.sleep(30)