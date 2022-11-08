import asyncio, threading
from telethon import TelegramClient
from telethon.tl.types import User, InputPeerUser, InputPeerChannel
from telethon.tl.functions.messages import GetHistoryRequest, CheckChatInviteRequest
from telethon.tl.functions.contacts import SearchRequest
from telethon import *
from system_fb import *


def TGclient(ID):
    session_data = jsone_session(ID)
    proxy = test_proxy(ID)
    session = f'{os.getcwd()}/data_api/{ID}'
    return TelegramClient(session=session,
                              api_id=session_data['app_id'],
                              api_hash=session_data['app_hash'],
                              use_ipv6=session_data['ipv6'],
                              proxy=proxy,
                              device_model=session_data['device'],
                              system_version=session_data['sdk'],
                              app_version=session_data['app_version']
                              )

async def distribute_object(client,object):
    if not in_delete_users(object):
        link = f"https://t.me/{object}"
        section = None
        try:
            object_entity = await client.get_input_entity(link)
            if type(object_entity) is InputPeerUser:
                if str(object_entity.user_id) not in super_users:
                    link = f"@{object}"
                    entity = await client.get_entity(object_entity)
                    if entity.bot:
                        section = "Боты"
                    else:
                        section = "Операторы"
            elif str(object_entity.channel_id) not in super_users:
                section = "Каналы"
        except Exception as e:
            if "+" in object or "join" in object:
                section = "Остальное"
            elif "Cannot find" in str(e) or "No user" in str(e) or "Nobody is using" in str(e):  
                test_print(f"Юзер {object} больше не существует")
                uppend_delete_users(object)
            elif "A wait of " in str(e):
                timer = str(e).split("A wait of ")[1].split(" ")[0]
                test_print(f"Больше не можем проверить ссылку. Словили таймер {timer} секунд")
                time.sleep(.5)
            else:
                test_print(f"Ошибка : {str(e)}")
                time.sleep(.5)
        if section:
            data_base_update(link,section)

async def observ_search(text,client):
    flag = "tg://resolve?domain="
    if flag in text:
        work_text = text
        while flag in work_text:
            object = work_text.split(flag)[1]
            try:
                object = object.split("&")[0]
            except:
                pass
            if object not in bad_users:
                work_text = work_text.replace(flag + object, '')
                await asyncio.gather(distribute_object(client,object))


            
    flag_base = ["@","t.me/"] 
    for flag in flag_base:
        if flag in text:
            while flag in text:
                object = clear_data(text.split(flag)[1].split(" ")[0])
                if object not in bad_users:
                    text = text.replace(flag + object, '')
                    await asyncio.gather(distribute_object(client,object))

async def history(chat,client):
    if (str(chat.id) not in super_users) and (chat.username not in bad_users):
        data_base_update(f"https://t.me/{chat.username}","Каналы")
        history = await client(GetHistoryRequest(
                            peer=chat,
                            offset_id=0,
                            offset_date=None, add_offset=0,
                            limit=10, max_id=0, min_id=0,
                            hash=0))

        for message in history.messages:
            try:
                await asyncio.gather(observ_search(str(message.message),client))
            except:
                pass
            try:
                for entitie in message.entities:
                    try:
                        await asyncio.gather(observ_search(str(entitie),client))
                    except:
                        pass
            except:
                pass
            try:
                await asyncio.gather(observ_search(str(message.reply_markup),client))
            except:
                pass
            try:
                await asyncio.gather(observ_search(str(message.media.webpage.description),client))
            except:
                pass

async def search_script(client,search_text):
    test_print(f"Ищем по ключевому слову: {search_text}")
    search_results = await client(SearchRequest(q=search_text,limit=10))
    test_print(search_results.results)
    time.sleep(1000)



    test_print(f"Нашли юзеров в поиске: {len(search_results.users)}")
    for user in search_results.users:
        if (str(user.id) not in super_users) and (user.username not in bad_users):
            if user.bot:
                data_base_update(f"@{user.username}","Боты")
            else:
                data_base_update(f"@{user.username}","Операторы")
    test_print(f"Нашли каналов в поиске: {len(search_results.chats)}")
    for chat in search_results.chats:
        await asyncio.gather(history(chat,client))                 
    test_print("Собрали все данные с каналов из поиска\n######################################\n")

async def work_script(client):
    async with client:
        for word in words_base:
            test_print('\n######################################################\n')
            test_print(f'Ключевое слово {word}')
            await asyncio.gather(search_script(client,word))

async def main():
    test_print('\n######################################################\n')
    test_print(f'Начало работы {time.strftime("%a, %d %b %Y %H:%M:%S ")}')
    data_base_clear()
    for ID in session_base():
        test_print('######################################################')
        test_print(f'Подключаемся к телеграмм сессия {ID}')
        test_print('######################################################')
        await asyncio.gather(work_script(TGclient(ID)))

    test_print('\n######################################################\n')
    test_print(f'Обработали {len(words_base)} ключевых слов')
    json_to_txt()
    test_print('\n######################################################\n')
    test_print(f'Конец работы {time.strftime("%a, %d %b %Y %H:%M:%S ")}')
    input("Нажмите ENTER для выхода из программы.")


if __name__ == '__main__':
    asyncio.run(main())



