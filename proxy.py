
import random, requests
from config_fb import *
from system_fb import *


def proxy_is_alive(proxy_type,proxy_ip,proxy_port,proxy_login,proxy_password):
    try:
        proxy = f'{proxy_type}://{proxy_login}:{proxy_password}@{proxy_ip}:{proxy_port}' 
        test_print(proxy)
        req = requests.get('https://api.ipify.org?format=json',proxies=dict(http=proxy,https=proxy))
        test_print(req.json())
        test_print("proxy is alive")
        data = True
    except:
        test_print("proxy not alive")
        data = False
    return data

def random_proxy():
    proxy = None
    while not proxy:
        test_print("get random proxy")
        proxy = random.choice(socks5_base)
        proxy_type = "socks5"
        proxy_ip = proxy[1]
        proxy_port = proxy[2]
        proxy_login = proxy[-2]
        proxy_password = proxy[-1]
        if not proxy_is_alive(proxy_type,proxy_ip,proxy_port,proxy_login,proxy_password):
            socks5_base.remove(proxy)
            proxy = None
    socks5_base.remove(proxy)
    return proxy

def test_proxy_old(proxy=None):
    if proxy:
        type,proxy_ip,proxy_port,rool,proxy_login,proxy_password = proxy
        if not proxy_is_alive("socks5",proxy_ip,proxy_port,proxy_login,proxy_password):
            return random_proxy()
        else:
            return proxy
    else:
        return random_proxy()



def test_proxy(ID):
    session_data = jsone_session(ID)
    if proxy := session_data["proxy"]:
        type,proxy_ip,proxy_port,rool,proxy_login,proxy_password = proxy
        if not proxy_is_alive("socks5",proxy_ip,proxy_port,proxy_login,proxy_password):
            proxy = random_proxy()
            jsone_session_update_proxy(ID,proxy)
            
    return proxy