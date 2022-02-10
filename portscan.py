from tools.portscan.portscan import PortScan
from lib.api import get, put_port, get_ip_info, update_ip_to_domain
from tools.oneforall.config import log
from loguru import logger
import time
import datetime


def scan(ip, is_scan, subdomain):
    port_data = {'code': 0, 'reason': '', 'data': []}
    ip_info = {'is_cdn': False, 'is_private': False, 'ip': ip}
    try:
        if not ip:
            ip_info = get_ip_info('', subdomain)
            if isinstance(ip_info, dict):
                ip_info['domain'] = subdomain
                update_ip_to_domain(ip_info)
            else:
                raise Exception(str(ip_info))
        if (not is_scan) and (not ip_info['is_cdn']) and (not ip_info['is_private']):
            app = PortScan(ip_info['ip'])
            app.run()
            if app.error:
                raise Exception(app.error)
            for i in app.data:
                ip_port_info = app.data.get(i)
                ip = ip_port_info['ip']
                port = ip_port_info['port']
                name = ip_port_info['name']
                product = ip_port_info['product']
                version = ip_port_info['version']
                port_data['data'].append(
                    {"ip": ip, "port": port, "service": name, "product": product, "version": version}
                )
            port_data['code'] = 1
        elif ip_info['is_cdn']:
            port_data['reason'] = '该IP是CDN节点'
        elif ip_info['is_private']:
            port_data['reason'] = '该IP是内网IP'
        else:
            port_data['reason'] = '该IP端口数据已被录入'
    except Exception as e:
        port_data['code'] = 0
        port_data['reason'] = str(e)
    finally:
        return port_data


def run():
    while True:
        data = get('ip')        #"data":{"subdomain":"www.foxyu.cn","project_name":"京东","ip":"107.155.15.110","is_scan":false}

        if data['code'] == 0:
            logger.log('ERROR', data['msg'])
            time.sleep(30)
        else:
            ip = data['data'].get('ip')     #107.155.15.110
            subdomain = data['data'].get('subdomain')   #www.foxyu.cn
            project_name = data['data'].get('project_name')    #京东
            is_scan = data['data'].get('is_scan')       #false
            if not is_scan:
                logger.log('INFOR', f'[{subdomain}] {ip} {is_scan} - 开始扫描')
                start = datetime.datetime.now()             #扫描开始时间
                port_data = scan(ip, is_scan, subdomain)    #扫描
                end = datetime.datetime.now()               #扫描结束时间

                port_data['time'] = (end-start).seconds
                port_data['domain'] = subdomain
                port_data['project_name'] = project_name

                put_port(port_data)
                logger.log('INFOR', f'[{subdomain}] {ip} - 扫描完成')
                #{'code': 1, 'reason': '', 'data': [{'ip': '119.23.87.38', 'port': 80, 'service': 'http', 'product': 'Tengine httpd', 'version': ''}, {'ip': '119.23.87.38', 'port': 81, 'service': 'http', 'product': 'Tengine httpd', 'version': ''}, {'ip': '119.23.87.38', 'port': 83, 'service': 'http', 'product': 'Tengine httpd', 'version': ''}, {'ip': '119.23.87.38', 'port': 84, 'service': 'http', 'product': 'Tengine httpd', 'version': ''}, {'ip': '119.23.87.38', 'port': 9443, 'service': 'http', 'product': 'Tengine httpd', 'version': ''}, {'ip': '119.23.87.38', 'port': 9663, 'service': 'http', 'product': 'nginx', 'version': ''}, {'ip': '119.23.87.38', 'port': 10000, 'service': 'http', 'product': 'Tengine httpd', 'version': ''}, {'ip': '119.23.87.38', 'port': 10001, 'service': 'http', 'product': 'Tengine httpd', 'version': ''}, {'ip': '119.23.87.38', 'port': 28080, 'service': 'http', 'product': 'Tengine httpd', 'version': ''}], 'time': 35, 'domain': 'hestia.huolala.cn'}
            else:
                logger.log('INFOR', f'[{subdomain}] {ip} {is_scan} - 该IP端口数据已被录入')

if __name__ == '__main__':
    run()
