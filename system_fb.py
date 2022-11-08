from telethon import TelegramClient, sync
import random, requests
import os, time, json
from config_fb import *

def test_print(data):
    fl_test = True  ##################           !!!!!!!!!!!! НЕ ЗАБЫВАЙ !!!!!!!!!!!!           #########################
    if fl_test:
        print(data)

async def new_client(ID:str = None):
    sessions = session_base()
    day = time.strftime("%d")
    hour = time.strftime("%H")
    dir = f"{os.getcwd()}\\ignore\\sleep"
    with open(dir + ".json","r", encoding='utf-8') as json_file:
            json_data = json.load(json_file)

    if ID:

        json_data[ID] = {"D":day,"H":hour}
    
    for key_ID in list(json_data):
        if json_data[key_ID]["D"] != day and int(json_data[key_ID]["H"]) < int(hour):
            del json_data[key_ID]

    new_ID = random.choice(sessions)    
    while new_ID in list(json_data):
        sessions.remove(new_ID)
        new_ID = random.choice(sessions)

    with open(dir + ".json","w", encoding='utf-8') as out_file:
        json.dump(json_data,out_file)

    return new_ID

def TGclient(ID):
    try:
        test_print('######################################################')
        session_data = jsone_session(ID)
        test_print(f'##  Cессия {ID}')
        proxy = test_proxy(ID)
        test_print(f'##  Прокси : {proxy}')
        session = f'{os.getcwd()}/data_api/{ID}'
        test_print(f'##  Подключаемся к телеграмм')
        test_print('######################################################')
        return TelegramClient(session=session,
                                api_id=session_data['app_id'],
                                api_hash=session_data['app_hash'],
                                use_ipv6=session_data['ipv6'],
                                proxy=proxy,
                                device_model=session_data['device'],
                                system_version=session_data['sdk'],
                                app_version=session_data['app_version']
                                )
    except:
        test_print(f'##  Не смогли подключиться к телеграмм')
        test_print('######################################################')
        return_proxy(ID)

def proxy_is_alive(proxy_type,proxy_ip,proxy_port,proxy_login,proxy_password):
    try:
        proxy = f'{proxy_type}://{proxy_login}:{proxy_password}@{proxy_ip}:{proxy_port}' 
        req = requests.get('https://api.ipify.org?format=json',proxies=dict(http=proxy,https=proxy))
        # test_print(req.json())
        data = True
    except:
        data = False
    return data

def random_proxy():
    proxy = None
    while proxy == None:
        # test_print("get random proxy")
        proxy = random.choice(socks5_base)
        proxy_type = "socks5"
        proxy_ip = proxy[1]
        proxy_port = proxy[2]
        proxy_login = proxy[-2]
        proxy_password = proxy[-1]
        if not proxy_is_alive(proxy_type,proxy_ip,proxy_port,proxy_login,proxy_password):
            socks5_base.remove(proxy)
            proxy = None
    return proxy

def return_proxy(ID):
    dir = f'{os.getcwd()}\\proxy\\bad_socks5'
    proxy = str(jsone_session(ID)["proxy"])

    with open(dir + ".txt", "w") as text_file:
        text_file.writelines(proxy + "\n")

def test_proxy(ID):
    session_data = jsone_session(ID)
    proxy = session_data["proxy"]
    if proxy:
        type,proxy_ip,proxy_port,rool,proxy_login,proxy_password = proxy
        if not proxy_is_alive("socks5",proxy_ip,proxy_port,proxy_login,proxy_password):
            proxy = random_proxy()
            jsone_session_update_proxy(ID,proxy)
    else:
        proxy = random_proxy()    
    return proxy

def session_base():
    base = []
    for file_name in os.listdir(f'{os.getcwd()}\\data_api'):
        if ".session" in file_name:
            base.append(file_name.split(".session")[0])
    return base

def jsone_session(id):
    with open(f'{os.getcwd()}\\data_api\\{id}.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    json_out = {'session_file':False,
                'app_id':None,
                'app_hash':None,
                'first_name':None,
                'last_name':None,
                'sdk':"Android 7.0 Nougat",
                'app_version':"PS(22)",
                'device':"Huawei P Smart S Midnight Black",
                'lang_pack':"android",
                'proxy':None,
                'ipv6':False,
                'password_str':None}

    for key in list(json_out) + ['my_2fa','twoFA']:
        try:
            json_out[key] = json_data[key]
        except:
            pass

    return json_out

def jsone_session_update_proxy(id,proxy):
    dir = f'{os.getcwd()}\\data_api\\{id}.json'
    with open(dir, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    json_data["proxy"] = proxy
    with open(dir,"w", encoding='utf-8') as out_file:
        json.dump(json_data,out_file)

def data_base_update(data,file_name):
    dir = f"{os.getcwd()}\\pars_data\\{file_name}.json"
    with open(dir,"r", encoding='utf-8') as in_file:
        json_data = json.load(in_file)

    if data not in list(json_data.values()):
        key = str(len(json_data) + 1)
        json_data[key] = data
        test_print(f"{file_name} : {data}")
        with open(dir,"w", encoding='utf-8') as out_file:
            json.dump(json_data,out_file)
    #     return True
    # else:
    #     return False
def check_not_in_base(data,file_name):
    dir = f"{os.getcwd()}\\pars_data\\{file_name}.json"
    with open(dir,"r", encoding='utf-8') as in_file:
        json_data = json.load(in_file)
    if data not in list(json_data.values()):
        return True
    else:
        return False

def data_base_clear():
    name_list = ["Боты","Операторы","Остальное","Каналы"]
    for name in name_list:
        dir = f"{os.getcwd()}\\pars_data\\{name}.json"
        json_data = {}
        with open(dir,"w", encoding='utf-8') as out_file:
                json.dump(json_data,out_file)

def clear_data(data):
    for literal in ["'","\n",")","]","}","(","[","{","/"," ","\\"," "]:
        try:
            data = data.split(literal)[0]
        except:
            pass
    return data

def json_to_txt():
    name_list = ["Боты","Операторы","Остальное","Каналы"]
    for name in name_list:
        dir = f"{os.getcwd()}\\pars_data\\{name}"
        with open(dir + ".json","r", encoding='utf-8') as json_file:
            json_data = json.load(json_file)

        with open(dir + ".txt", "w") as text_file:
            for line in list(json_data.values()):
                text_file.writelines(line + "\n")

def uppend_delete_users(username):
    dir = f"{os.getcwd()}\\ignore\\deleted"
    with open(dir + ".txt", "a", encoding='utf-8') as text_file:
        text_file.write(username + "\n")

def in_delete_users(username):
    dir = f"{os.getcwd()}\\ignore\\deleted"
    with open(dir + ".txt","r", encoding='utf-8') as text_file:
        text = text_file.read()
    if username in text:
        return True
    else:
        return False

if __name__ == '__main__':
    pass