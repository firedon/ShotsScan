cdn_scan = True  # 不扫描识别为cdn的IP
shodan_api = 't8A6SnEjbpAiJpls7rYWSGBjespSpqeY'  # shodan查询api
fofa_email = '865605431@qq.com'
fofa_key = 'af9980c73feb46a7f0c072eaa2eef122'
async_scan = True  # 是否开启常规端口服务探测
async_scan_timeout = 30  # 异步端口扫描超时时间
async_scan_threads = 500  # 异步协程数
# nmap程序路径地址，可指定具体路径或设置环境变量
nmap_search_path = ('nmap', '/usr/bin/nmap', '/usr/local/bin/nmap', '/sw/bin/nmap', '/opt/local/bin/nmap')
# 超过多少个端口识别为CDN丢弃
port_num = 500
