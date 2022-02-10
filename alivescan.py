from tools.alivescan.alivescan import WebAliveScan
from lib.api import get, put_alive
from tools.oneforall.config import log
from loguru import logger
import time
import datetime


def scan(subdomain):
    alive_data = {'code': 0, 'reason': '', 'data': []}
    try:
        app = WebAliveScan(subdomain)
        app.run()
        for i in app.data:
            alive_data['data'].append(i)
        alive_data['code'] = 1
    except Exception as e:
        alive_data['code'] = 0
        alive_data['reason'] = str(e)
    finally:
        return alive_data


def run():
    while True:
        data = get('subdomain')
        #"data":{"subdomain":"huolala.cn","project_name":"货拉拉"}
        if data['code'] == 0:
            logger.log('ERROR', data['msg'])
            time.sleep(30)
        else:
            subdomain = data['data'].get('subdomain')   #huolala.cn
            project_name = data['data'].get('project_name')   #货拉拉

            start = datetime.datetime.now()     #扫描开始时间
            alive_data = scan(subdomain)        #扫描
            end = datetime.datetime.now()       #扫描结束时间

            alive_data['time'] = (end-start).seconds
            alive_data['domain'] = subdomain
            alive_data['project_name'] = project_name
            put_alive(alive_data)
            logger.log('INFOR', f'[{project_name}] {subdomain} - alive扫描完成')


if __name__ == '__main__':
    run()
