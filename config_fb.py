import socks, os

BASE = [("А_Я=","абвгдеёжзийклмнопрстуфхцчшщъыьэюя"),
        ("A_Z=","abcdefghijklmnopqrstuvwxyz"),
        ("0_9=","0123456789")]

with open(f"{os.getcwd()}\\ignore\\id.txt","r", encoding='utf-8') as file:
    search_data = file.read().split("\n")
super_users = []
for point in search_data:
    if len(point) > 1 :
        super_users.append(point)

with open(f"{os.getcwd()}\\ignore\\name.txt","r", encoding='utf-8') as file:
    search_data = file.read().split("\n")
bad_users = []
for point in search_data:
    if len(point) > 1 :
        bad_users.append(point)

with open(f"{os.getcwd()}\\words.txt","r", encoding='utf-8') as file:
    search_data = file.read().split("\n")
words_base = []
for point in search_data:
    if len(point) > 1 :
        words_base.append(point)

with open(f"{os.getcwd()}\\proxy\\socks5.txt","r", encoding='utf-8') as file:
    socks5_data = file.read().split("\n")
socks5_base = []
for point in socks5_data:
    if ":" in point:
        ip, port, login, password = point.split(":")
        socks5_base.append((socks.SOCKS5, ip, int(port), False, login, password))