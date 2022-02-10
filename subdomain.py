from tools.oneforall import oneforall
from lib.api import get, put_subdomain, get_ip_info
from tools.oneforall.config import log
from loguru import logger
import time
import datetime


def scan(domain):
    domain_data = {'code': 0, 'reason': '', 'data': []}
    try:
        app = oneforall.OneForAll(domain)
        app.run()
        logger.log('INFOR', f'======= oneforall 扫描完成 =======')
        #app.data = [{'id': 647, 'alive': 1, 'request': 1, 'resolve': 1, 'url': 'http://zhuanxian.huolala.cn', 'subdomain': 'zhuanxian.huolala.cn', 'level': 1, 'cname': 'van.huolala.cn', 'ip': '8.129.135.39', 'public': 1, 'cdn': 1, 'port': 80, 'status': 200, 'reason': 'OK', 'title': '货拉拉专线系统', 'banner': 'Van', 'cidr': '8.129.128.0/17', 'asn': 'AS37963', 'org': 'Hangzhou Alibaba Advertising Co. Ltd.', 'addr': '中国广东省深圳市', 'isp': '阿里云', 'source': 'VirusTotalAPIQuery'}, {'id': 648, 'alive': 1, 'request': 1, 'resolve': 1, 'url': 'https://zhuanxian.huolala.cn', 'subdomain': 'zhuanxian.huolala.cn', 'level': 1, 'cname': 'van.huolala.cn', 'ip': '8.129.135.39', 'public': 1, 'cdn': 1, 'port': 443, 'status': 200, 'reason': 'OK', 'title': '货拉拉专线系统', 'banner': 'Van', 'cidr': '8.129.128.0/17', 'asn': 'AS37963', 'org': 'Hangzhou Alibaba Advertising Co. Ltd.', 'addr': '中国广东省深圳市', 'isp': '阿里云', 'source': 'VirusTotalAPIQuery'}, {'id': 380, 'alive': 0, 'request': 0, 'resolve': 1, 'url': 'https://zhuanxian-stg.huolala.cn', 'subdomain': 'zhuanxian-stg.huolala.cn', 'level': 1, 'cname': 'zhuanxian-stg.huolala.cn', 'ip': '10.129.37.215', 'public': 0, 'cdn': 0, 'port': 443, 'status': None, 'reason': '(MaxRetryError("HTTPSConnectionPool(host=\'zhuanxian-stg.huolala.cn\', port=443): Max retries exceeded with url: / (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x7fe75c0c1f90>, \'Connection to zhuanxian-stg.huolala.cn timed out. (connect timeout=13)\'))"),)', 'title': None, 'banner': None, 'cidr': '10.0.0.0/8', 'asn': 'AS-', 'org': '-', 'addr': '内网IP', 'isp': '内网IP', 'source': 'IP138Query'}]
        logger.log('INFOR',len(app.data))
        for i in app.data:
            logger.log('INFOR',i)
            subdomain = i['subdomain']
            subdomain_ip = i['ip']
            city = None
            is_private = False
            is_cdn = False
            if subdomain and subdomain_ip:
                subdomain_ip = subdomain_ip.split(',')[0]
                ip_info = get_ip_info(subdomain_ip)
                if isinstance(ip_info, dict):
                    city = ip_info['city']
                    is_private = ip_info['is_private']
                    is_cdn = ip_info['is_cdn']
            elif subdomain:
                pass
            else:
                continue
            domain_data['data'].append({
                'subdomain': subdomain,
                'subdomain_ip': subdomain_ip,
                'city': city,
                'is_private': is_private,
                'is_cdn': is_cdn
            })
        domain_data['code'] = 1
    except Exception as e:
        domain_data['code'] = 0
        domain_data['reason'] = str(e)
    finally:
        logger.log('INFOR',len(domain_data['data']))
        return domain_data


def run():
    while True:
        data = get('domain')    
        #data = {"code":1,"msg":"返回成功","time":"1642736657","data":{"domain":"huolala.cn","project_name":"货拉拉"}}
        if data['code'] == 0:
            logger.log('ERROR', data['msg'])
            time.sleep(30)
        else:
            domain = data['data']['domain']     #foxyu.cn
            project_name = data['data']['project_name']     #京东

            start = datetime.datetime.now()     #扫描开始时间
            domain_data = scan(domain)          #扫描
            end = datetime.datetime.now()       #扫描结束时间    

            domain_data['time'] = (end-start).seconds
            domain_data['domain'] = domain
            domain_data['project_name'] = project_name
            domain_data['plugin'] = 'oneforall'

            put_subdomain(domain_data)
            logger.log('INFOR', f'[{domain}] {domain_data} - 扫描完成')
            #$domain_data = {"code": 1, "reason": "", "data": [{"subdomain": "foxyu.cn", "subdomain_ip": "104.21.65.34", "city": "CLOUDFLARE.COMCLOUDFLARE.COMcloudflare.com", "is_private": false, "is_cdn": true}, {"subdomain": "foxyu.cn", "subdomain_ip": "104.21.65.34", "city": "CLOUDFLARE.COMCLOUDFLARE.COMcloudflare.com", "is_private": false, "is_cdn": true}, {"subdomain": "www.foxyu.cn", "subdomain_ip": "172.67.188.191", "city": null, "is_private": false, "is_cdn": false}, {"subdomain": "www.foxyu.cn", "subdomain_ip": "172.67.188.191", "city": null, "is_private": false, "is_cdn": false}], "time": 86, "domain": "foxyu.cn", "project_name": "\u8d27\u62c9\u62c9"}


if __name__ == '__main__':
    run()
