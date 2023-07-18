"""
How are we going to call it? Please choose a name for your bot.
taller_bot

Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
Tallers_bot

t.me/Tallers_bot
"""
import tb_settings
import tb_dict_currency
import telebot
import requests
import json
import lxml
import lxml.html
from lxml import etree
import currencyapicom
client = currencyapicom.Client(tb_settings.CR_TOKEN)


print("Телеграмм бот по обмену валют запущен.")

# result = client.currencies(currencies=['EUR', 'RUB'])
# print(result)

# result = client.currencies()
# print(result)

# print(tb_settings.CR_REQUEST_CR_LATE)
# print(tb_settings.CR_REQUEST_CR_LIST)

# r = requests.get(tb_settings.CR_REQUEST_CR_LATE)  # запрашиваем текущие курсы всех валют
# print(r.content)
# print(r.status_code)  # узнаем статус полученного ответа
# curr = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы

# curr = tb_dict_currency.curr
#
# data = curr['data']
# print()
# dl = 0
# curr_info_request = ''
# sd = ''
# for keys in data.keys():
#     dl += 1
#     print(curr['data'][keys]['code'], curr['data'][keys]['value'])
#     sd = keys
#     if dl < len(data):
#         sd += '%2C'
#     curr_info_request += sd
# print(curr_info_request)

# currencies_list = tb_dict_currency.currencies_list
#
# data = currencies_list['data']
# print('Список обслуживаемых валют.')
# dl = 0
# for keys in data.keys():
#     dl += 1
#     if currencies_list['data'][keys] is not None:
#         print(currencies_list['data'][keys]['code'], '\t-',
#               currencies_list['data'][keys]['name']
#               )
#
#

#
# print(tb_settings.CR_REQUEST_CR_LATE + curr_info_request)
# r = requests.get(tb_settings.CR_REQUEST_CR_LATE + curr_info_request)  # запрашиваем текущие курсы всех валют
# print(r.content)
# print(r.status_code)  # узнаем статус полученного ответа
# val_list = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы
#
# print(val_list)

# quit(0)

bot = telebot.TeleBot(tb_settings.TB_TOKEN)

# @bot.message_handler(filters)
# def function_name(message):
#     bot.reply_to(message, "This is a message handler")




# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    name = str(message.chat.first_name)
    if len(name) == 0:
        name = str(message.chat.username)
        if len(name) == 0:
            name = "путник"
    print('Пришел запрос от:', name, message.text)
    
    bot.send_message(message.chat.id, 'Привет тебе, ' + name + ', забредший сюда.')
    bot.send_message(message.chat.id, tb_settings.H_TEXT)
    
    
# Обрабатывается запрос конвертации валют
@bot.message_handler(commands=['e', 'ex', 'exch', 'exchange'])
def handle_exchange(message):
    name = str(message.chat.first_name)
    if len(name) == 0:
        name = str(message.chat.username)
        if len(name) == 0:
            name = "путник"
    cmd_ln = message.text.split()
    print('Прилетел запрос=', name, cmd_ln)
    if len(cmd_ln) == 4:
        try:
            val1 = currencies_list['data'][str(cmd_ln[1].upper())]  # ['code']
            val2 = currencies_list['data'][str(cmd_ln[2].upper())]  # ['code']
            amount = float(str(cmd_ln[3]))
        except KeyError:
            bot.send_message(message.chat.id, str('Код валюты введен с ошибкой!\n\n' + tb_settings.H_TEXT))
            return
        except ValueError:
            bot.send_message(message.chat.id, str('Число введено с ошибкой!\n\n' + tb_settings.H_TEXT))
            return
        
        dec_v1 = '%.' + str(val1['decimal_digits']) + 'f'
        dec_v1 = dec_v1 % amount
        sl = [val1['code'], val2['code'], dec_v1]
        print(sl)
        print(val1)
        print(val2)
        s = ' '.join(sl)
        print(s)
        
        result = 1.2345
        
        dec_v2 = '%.' + str(val2['decimal_digits']) + 'f'
        dec_v2 = dec_v2 % result
        # str(f'={amount:.2f}')
        bot.send_message(message.chat.id, str(val1['code'] + '=' + dec_v1 + ' -> ' + val2['code'] + '=' + dec_v2))
    else:
        bot.send_message(message.chat.id, str('Что Вы имели ввиду набрав:\n"' +
                                              str(cmd_ln) + '"?\n\n' + tb_settings.H_TEXT))
    
    
    

# Обрабатывается запрос списка валют
@bot.message_handler(commands=['v', 'val', 'value'])
def handle_values(message):
    texts = 'Список обслуживаемых валют.\n'
    data = currencies_list['data']
    print(texts)
    dl = 0
    s = ''
    for keys in data.keys():
        dl += 1
        if currencies_list['data'][keys] is not None:
            s = currencies_list['data'][keys]['code'] + '\t-' + currencies_list['data'][keys]['name']
            print(s)
            texts += s + '\n'
    bot.send_message(message.chat.id, texts)

@bot.message_handler(content_types=['photo', ])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme XDD')


# не обслуженный входной поток
@bot.message_handler(func=lambda message: True)
def other_messages(message):
    bot.send_message(message.chat.id, str('Что Вы имели ввиду набрав:\n"' + message.text + '"?'))



currencies_list = tb_dict_currency.currencies_list

bot.polling(none_stop=True)



"""
'id': 864491376, 'first_name': 'Natasha'
'id': 463882236, 'first_name': '.V.aSko.V.'
'id': 275588773, 'first_name': 'Dmitry'
'id': 224489387, 'first_name': 'Gidro', 'username': 'Gidro_Gidro', 'last_name': 'Gidro'

{
'content_type': 'text',
'id': 48,
'message_id': 48,
'from_user': {
                'id': 463882236,
                'is_bot': False,
                'first_name': '.V.aSko.V.',
                'username': 'kitty1ket',
                'last_name': None,
                'language_code': 'ru',
                'can_join_groups': None,
                'can_read_all_group_messages': None,
                'supports_inline_queries': None,
                'is_premium': None,
                'added_to_attachment_menu': None
             },
'date': 1689316154,
'chat': {
            'id': 463882236,
            'type': 'private',
            'title': None,
            'username': 'kitty1ket',
            'first_name': '.V.aSko.V.',
            'last_name': None,
            'is_forum': None,
            'photo': None,
            'bio': None,
            'join_to_send_messages': None,
            'join_by_request': None,
            'has_private_forwards': None,
            'has_restricted_voice_and_video_messages': None,
            'description': None,
            'invite_link': None,
            'pinned_message': None,
            'permissions': None,
            'slow_mode_delay': None,
            'message_auto_delete_time': None,
            'has_protected_content': None,
            'sticker_set_name': None,
            'can_set_sticker_set': None,
            'linked_chat_id': None,
            'location': None,
            'active_usernames': None,
            'emoji_status_custom_emoji_id': None,
            'has_hidden_members': None,
            'has_aggressive_anti_spam_enabled': None
        },
'sender_chat': None,
'forward_from': None,
'forward_from_chat': None,
'forward_from_message_id': None,
'forward_signature': None,
'forward_sender_name': None,
'forward_date': None,
'is_automatic_forward': None,
'reply_to_message': None,
'via_bot': None,
'edit_date': None,
'has_protected_content': None,
'media_group_id': None,
'author_signature': None,
'text': '/start',
'entities': [<telebot.types.MessageEntity object at 0x0338CE38>],
'caption_entities': None,
'audio': None,
'document': None,
'photo': None,
'sticker': None,
'video': None,
'video_note': None,
'voice': None,
'caption': None,
'contact': None,
'location': None,
'venue': None,
'animation': None,
'dice': None,
'new_chat_member': None,
'new_chat_members': None,
'left_chat_member': None,
'new_chat_title': None,
'new_chat_photo': None,
'delete_chat_photo': None,
'group_chat_created': None,
'supergroup_chat_created': None,
'channel_chat_created': None,
'migrate_to_chat_id': None,
'migrate_from_chat_id': None,
'pinned_message': None,
'invoice': None,
'successful_payment': None,
'connected_website': None,
'reply_markup': None,
'message_thread_id': None,
'is_topic_message': None,
'forum_topic_created': None,
'forum_topic_closed': None,
'forum_topic_reopened': None,
'has_media_spoiler': None,
'forum_topic_edited': None,
'general_forum_topic_hidden': None,
'general_forum_topic_unhidden': None,
'write_access_allowed': None,
'user_shared': None,
'chat_shared': None,
'json':
        {
            'message_id': 48,
            'from':
                    {
                        'id': 463882236,
                        'is_bot': False,
                        'first_name': '.V.aSko.V.',
                        'username': 'kitty1ket',
                        'language_code': 'ru'
                    },
            'chat': {
                        'id': 463882236,
                        'first_name': '.V.aSko.V.',
                        'username': 'kitty1ket',
                        'type': 'private'},
            'date': 1689316154,
            'text': '/start',
            'entities': [{
                            'offset': 0,
                            'length': 6,
                            'type': 'bot_command'
                         }
                        ]
            }
        }
"""