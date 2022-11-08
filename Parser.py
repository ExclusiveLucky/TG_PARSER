#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio, threading
from telethon import TelegramClient
from telethon.tl.types import User, InputPeerUser, InputPeerChannel, PeerUser
from telethon.tl.functions.messages import GetHistoryRequest, CheckChatInviteRequest
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon import *
from system_fb import *

# pyinstaller --onefile Parser.py

#####################################################################################
BAD_WORDS = ["wa.me","instagram.com"]
ARABIC = ["؆","؈","؉","؊","؋","،","؍","؎","؏",
          "ؐ","ؑ","ؒ","ؓ","ؔ","ؕ","ؖ","ؗ","ؘ","ؙ","ؚ","؛",
          "؞","؟","ؠ","ء","آ","أ","ؤ","إ","ئ",
          "ا","ب","ة","ت","ث","ج","ح","خ","د",
          "ذ","ر","ز","س","ش","ص","ض","ط","ظ",
          "ع","غ","ػ","ؼ","ؽ","ؾ","ؿ","ـ","ف",
          "ق","ك","ل","م","ن","ه","و","ى","ي",
          "ً","ٌ","ٍ","َ","ُ","ِ","ّ","ْ","ٓ","ٔ","ٕ","ٖ",
          "ٗ","٘","ٙ","ٚ","ٛ","ٜ","ٝ","ٞ","ٟ","٠","١","٢","٣"
          ,"٤","٥","٦","٧","٨","٩","٪""٫","٬","٭",
          "ٮ","ٯ","ٰ","ٱ","ٲ","ٳ","ٴ","ٵ","ٶ","ٷ","ٸ",
          "ٹ","ٺ","ٻ","ټ","ٽ","پ","ٿ","ڀ","ځ","ڂ",
          "ڃ","ڄ","څ","چ","ڇ","ڈ","ډ","ڊ","ڋ","ڌ",
          "ڍ","ڎ","ڏ","ڐ","ڑ","ڒ","ړ","ڔ","ڕ","ږ",
          "ڗ","ژ","ڙ","ښ","ڛ","ڜ","ڝ","ڞ","ڟ","ڠ",
          "ڡ","ڢ","ڣ","ڤ","ڥ","ڦ","ڧ","ڨ","ک","ڪ",
          "ګ","ڬ","ڭ","ڮ","گ","ڰ","ڱ","ڲ","ڳ","ڴ",
          "ڵ","ڶ","ڷ","ڸ","ڹ","ں","ڻ","ڼ","ڽ","ھ",
          "ڿ","ۀ","ہ","ۂ","ۃ","ۄ","ۅ","ۆ","ۇ","ۈ",
          "ۉ","ۊ","ۋ","ی","ۍ","ێ","ۏ","ې","ۑ","ے",
          "ۓ","۔","ە","ۖ","ۗ","ۘ","ۙ","ۚ","ۛ","ۜ","۞","۟",
          "۠","ۡ","ۢ","ۣ","ۤ","ۥ","ۦ","ۧ","ۨ","۩","۪","۫","۬",
          "ۭ","ۮ","ۯ","۰","۱","۲","۳","۴","۵","۶",
          "۷","۸","۹","ۺ","ۻ","ۼ","۽","۾","ۿ"]
#####################################################################################

# pyinstaller --onefile Parser.py

async def distribute_object(client,object,level=1):
    fl_empty_link = True
    client_alive = True
    if not in_delete_users(object):
        link = f"https://t.me/{object}"
        section = None
        try:
            object_entity = await client.get_input_entity(link)
            entity = await client.get_entity(object_entity)
            if type(object_entity) is InputPeerUser:
                if str(object_entity.user_id) not in super_users:
                    link = f"@{object}"
                    if entity.bot:
                        section = "Боты"
                        fl_empty_link = False
                    else:
                        section = "Операторы"
                        fl_empty_link = False
            elif str(object_entity.channel_id) not in super_users:
                section = "Каналы"
                fl_empty_link = False

        except Exception as e:
            if "+" in object or "join" in object:
                section = "Остальное"
                fl_empty_link = False
            elif "Cannot find" in str(e) or "No user" in str(e) or "Nobody is using" in str(e):  
                test_print(f"Юзер {object} больше не существует")
                uppend_delete_users(object)
            elif "A wait of " in str(e):
                timer = str(e).split("A wait of ")[1].split(" ")[0]
                test_print(f"Больше не можем проверить ссылку. Словили таймер {timer} секунд")
                time.sleep(.5)
                client_alive = False
            else:
                test_print(f"Ошибка : {str(e)}")
                time.sleep(.5)

        if section and section != "Каналы":
            fl_empty_link = False
            data_base_update(link,section)
        elif section == "Каналы":
            fl_empty_link = False
            if client_alive and bool(level):
                level-=1
                client_alive = await history(entity,client,level) 

    return client_alive, fl_empty_link
            

async def observ_search(text,client,level=1):
    client_alive = True
    fl_full = False
    flag = "tg://resolve?domain="
    if flag in text:
        work_text = text
        while flag in work_text and client_alive:
            object = work_text.split(flag)[1]
            try:
                object = object.split("&")[0]
            except:
                pass
            if object not in bad_users and client_alive:
                work_text = work_text.replace(flag + object, '')
                client_alive, fl_empty_link = await distribute_object(client,object,level)
                if not fl_empty_link:
                    fl_full = True
     
    flag_base = ["@","t.me/"] 
    for flag in flag_base:
        if flag in text:
            while flag in text and client_alive:
                object = clear_data(text.split(flag)[1].split(" ")[0])
                if object not in bad_users:
                    text = text.replace(flag + object, '')
                    client_alive, fl_empty_link = await distribute_object(client,object,level)
                    if not fl_empty_link:
                        fl_full = True
    
    return client_alive, fl_full

async def check_chanal(chat,client):
    if all(x is True for x in [
                                await member_count(chat,client) >= MEMBERS,
                                not check_arabic(chat.username),
                                not check_arabic(chat.title),
                                str(chat.id) not in super_users,
                                str(chat.username) not in bad_users
                                ]
                                ):
        return True
    else:
        return False


async def history(chat,client,level=1):
        print(f"Проверяем историю : t.me/{chat.username} Глубина {LEVEL - level}")
        links_count = 0
        client_alive = True
        fl_good = True
        if check_not_in_base(f"https://t.me/{chat.username}","Каналы"):
            if await check_chanal(chat,client):
                history = await client.get_messages(chat, limit=10)            
                for message in history:
                    text_base = []
                    if fl_good:
                        for point in message.__dict__:
                            text_data = str(getattr(message, point))
                            if all(word not in text_data for word in BAD_WORDS):
                                text_base.append(text_data)
                            else:
                                fl_good = False
                                test_print("Канал не интересен нам.")
                                test_print('----------------------------------')
                                break
                        if "The admins of this channel have restricted saving content" in str(text_base):
                            links_count += 1
                        elif client_alive and fl_good:
                            try:
                                client_alive, fl_full = await observ_search(str(text_base),client,level)
                                links_count += int(fl_full)
                            except:
                                pass
                if links_count > 0:  
                    data_base_update(f"https://t.me/{chat.username}","Каналы")
                    test_print("Канал добавлен в базу.")
                    test_print('----------------------------------')
                elif not fl_good:
                    test_print("Канал не интересен нам.")
                    test_print('----------------------------------')
                else:
                    test_print("Канал пустышка.")
                    test_print('----------------------------------')

            else:
                test_print("Канал не интересен нам.")
                test_print('----------------------------------')
        else:
            test_print("Канал уже есть в базе")
            test_print('----------------------------------')

        return client_alive

async def member_count(chat,client):
    users = None
    try:
        channel_full_info = await client(GetFullChannelRequest(channel=chat))
        users = channel_full_info.full_chat.participants_count
        return int(users)
    except:
        return 9999999999

def check_arabic(data):
    arabic_count = 0
    for simbl in data:
        if simbl in ARABIC:
            arabic_count+=1
    if ((100 / len(data)) * arabic_count) >= 80:
        return True
    else:
        return False

async def search_script(client,search_text):
    client_alive = True
    chanal_count = 0
    test_print('######################################################')
    test_print(f"Ищем по ключевому слову: {search_text}")
    search_results = await client(SearchRequest(q=search_text,limit=20))
    if search_results.results == [] :
        time.sleep(2)
        search_results = await client(SearchRequest(q=search_text,limit=20))

    for result in search_results.results[:LIMIT]:
        entity = await client.get_entity(result)
        if type(result) is PeerUser:
            if (str(entity.id) not in super_users) and (entity.username not in bad_users) and not check_arabic(entity.username):
                if entity.bot:
                    data_base_update(f"@{entity.username}","Боты")
                else:
                    data_base_update(f"@{entity.username}","Операторы")
        else:
            if client_alive:
                if bool(LEVEL):
                    client_alive = await history(entity,client,LEVEL)
                elif await check_chanal(entity,client):
                    data_base_update(f"https://t.me/{entity.username}","Каналы")
                
                chanal_count += 1
    test_print(f'''
######################################################
# Нашли юзеров в поиске: {LIMIT - chanal_count if len(search_results.results) > LIMIT else len(search_results.results) - chanal_count}
######################################################
# Нашли каналов в поиске: {chanal_count}
######################################################
----------------------------------''')
    if client_alive:                 
        test_print("Собрали все данные с каналов из поиска\n######################################\n")
    return client_alive

async def control_work(client,word,ID):
    client_alive = await search_script(client,word)
    while not client_alive:
        await client.disconnect()
        time.sleep(1)
        ID = await new_client(ID)
        client = TGclient(ID)
        await client.connect()
        client_alive = await search_script(client,word)
    return client

async def work_script():
    ID = await new_client()
    client = TGclient(ID)
    await client.connect()
    for word in words_base:
            fl_complete = False
            for flag, base in BASE:
                if flag in word:
                    for point in base:
                        work_word = f"{point}_{word.split(flag)[1]}"
                        client = await control_work(client,work_word,ID)
                    fl_complete = True
                    break
            if not fl_complete:
                client = await control_work(client,word,ID)
    await client.disconnect()

async def main():
    test_print('\n######################################################\n')
    test_print(f'Начало работы {time.strftime("%a, %d %b %Y %H:%M:%S ")}')
    data_base_clear()

    await asyncio.gather(work_script())

    test_print('\n######################################################\n')
    test_print(f'Обработали {len(words_base)} ключевых слов')
    json_to_txt()
    test_print('\n######################################################\n')
    test_print(f'Конец работы {time.strftime("%a, %d %b %Y %H:%M:%S ")}')
    input("Нажмите ENTER для выхода из программы.")



if __name__ == '__main__':
    while True:
        try:
            MEMBERS = int(input("Введите минимальное количество подписчиков, для канала:\n"))
            LEVEL = int(input("Введите глубину поиска для канала:\n"))
            LIMIT = int(input("Введите лимит на выдачу поиска:\n"))
            break
        except:
            time.sleep(.5)
            pass
    asyncio.run(main())