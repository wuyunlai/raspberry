#!/usr/bin/env python  
#<strong style="color:black; background-color:#99ff99">-</strong>*<strong style="color:black; background-color:#99ff99">-</strong> coding:utf<strong style="color:black; background-color:#99ff99">-</strong>8 <strong style="color:black; background-color:#99ff99">-</strong>*<strong style="color:black; background-color:#99ff99">-</strong>  
   
import urllib2,urllib,json  
   
class Dns:  
     #Dnspod账户  
     _dnspod_user = 'wuyunlai@163.com'  
     #Dnspod密码  
     _dnspod_pwd = 'qoiqwe198123'  
     #Dnspod主域名，注意：是你注册的域名  
     _domain = 'wuyl.cn'  
     #子域名，如www，如果要使用根域名，用@  
     _sub_domain = '@'  
   
     def getMyIp(self):  
         try:  
             u = urllib2.urlopen('http://members.3322.org/dyndns/getip')  
             return u.read()  
         except HTTPError as e:  
             print e.read()  
             return None;  
   
     def api_call(self,api,data):  
         try:  
             api = 'https://dnsapi.cn/' + api  
             data['login_email'] = self._dnspod_user  
             data['login_password'] = self._dnspod_pwd  
             data['format'] ='json'  
             data['lang'] =  'cn'  
             data['error_on_empty'] = 'no'  
   
             data = urllib.urlencode(data)  
             req = urllib2.Request(api,data,  
                 headers = {  
                     'UserAgent' : 'LocalDomains/1.0.0(roy@leadnt.com)',  
                     'Content<strong style="color:black; background-color:#99ff99">-</strong>Type':'application/x<strong style="color:black; background-color:#99ff99">-</strong>www<strong style="color:black; background-color:#99ff99">-</strong>form<strong style="color:black; background-color:#99ff99">-</strong>urlencoded;text/html; charset=utf8',  
                     })  
             res = urllib2.urlopen(req)  
             html = res.read()  
             results = json.loads(html)  
             return results  
         except Exception as e:  
             print e  
   
     def main(self):  
         ip = self.getMyIp()  
         dinfo = self.api_call('domain.info',{'domain' : self._domain})  
         domainId = dinfo['domain']['id']  
         rs = self.api_call('record.list',  
             {  
                 'domain_id': domainId,  
                 'offset' :'0',  
                 'length' : '1',  
                 'sub_domain' : self._sub_domain  
             })  
   
         if rs['info']['record_total'] == 0:  
             self.api_call('record.create',  
                 {  
                     'domain_id' : domainId,  
                     'sub_domain' : self._sub_domain,  
                     'record_type' : 'A',  
                     'record_line' : '默认',  
                     'value' : ip,  
                     'ttl' : '3600'  
                 })  
             print 'Success.'  
         else:  
             if rs['records'][0]['value'].strip() != ip.strip():  
                 self.api_call('record.modify',  
                 {  
                     'domain_id' : domainId,  
                     'record_id' : rs['records'][0]['id'],  
                     'sub_domain' : self._sub_domain,  
                     'record_type' : 'A',  
                     'record_line' : '默认',  
                     'value' : ip  
                     })  
             else:  
                 print 'Success.'  
   
 if __name__ == '__main__':  
     d = Dns();  
     d.main()
