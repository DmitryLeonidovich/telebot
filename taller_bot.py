"""
How are we going to call it? Please choose a name for your bot.
taller_bot

Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
Tallers_bot

t.me/Tallers_bot
"""
from datetime import datetime
import tb_settings
import tb_dict_currency
import telebot
import requests
import json
from extensions import APIexceptions
import lxml
import lxml.html
from lxml import etree
import urllib3

import currencyapicom
client = currencyapicom.Client(tb_settings.CR_TOKEN)

bot = telebot.TeleBot(tb_settings.TB_TOKEN)


def date_time_stamp(date_message=None):
    if date_message is not None:
        return datetime.fromtimestamp(int(date_message)).strftime('%d-%m-%Y %H:%M:%S')
    else:
        return datetime.now().strftime('%d-%m-%Y %H:%M:%S')


def day_time_sender(_message):
    print(date_time_stamp(), end=" ")
    name = str(_message.chat.first_name)
    if len(name) == 0:
        name = str(_message.chat.username)
        if len(name) == 0:
            name = "путник"
    cmd_ln = _message.text.split()
    _s = 'запрос от =' + name + \
         ' id =' + str(_message.chat.id) + \
         ' команда =' + str(cmd_ln) + \
         ' время отправителя ' + date_time_stamp(_message.date)
    return _s


def get_all_currency():
    try:
        r = requests.get(tb_settings.CR_REQUEST_CR_LATE)  # запрашиваем текущие курсы всех валют
        _curr = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы
    except requests.exceptions.ReadTimeout:
        _curr = None
    except TypeError:
        _curr = None
    print(f'RAW response of {len(r.content)} bytes :\n', r.content)
    print('Status code : ', r.status_code)  # узнаем статус полученного ответа
    print(len(_curr['data']))
    return _curr


def get_all_currency_info():
    try:
        r = requests.get(tb_settings.CR_REQUEST_CR_LIST)  # запрашиваем текущие курсы всех валют
        _curr = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы
    except requests.exceptions.ReadTimeout:
        _curr = None
    except TypeError:
        _curr = None
    print(f'RAW response of {len(r.content)} bytes :\n', r.content)
    print('Status code : ', r.status_code)  # узнаем статус полученного ответа
    print(len(_curr['data']))
    return _curr


def get_currency_pair(val1, val2, amo):
    try:
        r = requests.get(tb_settings.CR_REQUEST_CR_LIST + val1 + "%2C" + val2)  # запрашиваем текущие курсы двух валют
        _curr = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы
    except requests.exceptions.ReadTimeout:
        _curr = None
        amo = 0
    except TypeError:
        _curr = None
        amo = 0
    else:
        pass
    return amo


def all_currency_list_out(_message):
    print(date_time_stamp(), 'передача списка обслуживаемых валют')
    texts = ''
    for keys in curr_list['data'].keys():
        if curr_list['data'][keys] is not None:
            s = ''
            if curr_info['data'][keys] is not None:
                try: # дополнительная информация о валюте есть
                    s = curr_info['data'][keys]['name_plural'] + '\n'
                except TypeError: # ошибка в информационном описании валюты
                    print('For key = [' + keys + ']')  # беду в консоль
                    print(curr_info['data'][keys])
                else:  # дополнительной информации о валюте нет
                    pass
            # ========================== блок форматирования вывода по правилам округления из API
            v_to_round = curr_list['data'][keys]['value']
            #
            # dec_dig = None  # нужна при выводе в консоль
            # if v_to_round < 0.0001:  # для малых значений ставим 10 знаков после запятой
            #     s_rounded = '{0:.10f}'.format(v_to_round)
            # elif len(s) != 0:  # нашли доп инфо по валюте и берем из нее число знаков после запятой
            #     dec_dig = curr_info['data'][keys]['decimal_digits']
            #     s_rounded = '%.' + str(dec_dig) + 'f'
            #     s_rounded = s_rounded % v_to_round
            # else:  # доп инфо по валюте нет - выставляем обычный тип формата
            #     s_rounded = '{0:f}'.format(v_to_round)
            # if float(s_rounded) == 0:  # проверяем на потерю точности и правим ее по обнаружении
            #     s_rounded = '*' + '{0:f}'.format(v_to_round)
            
            s_rounded = fmt_rnd(v_to_round, keys)
            
            # ==========================
            s += curr_list['data'][keys]['code'] + '\t = ' + s_rounded
            # print(f'Formatted [{keys}/{dec_dig}] =', s_rounded, '\t\t\t\t\t', v_to_round)  # в консоль не выводим
            texts += s + '\n'
            if len(texts) > 4000:
                bot.send_message(_message.chat.id, texts)  # вывод в бот первой части списка сообщением
                texts = ''
        # end of "if curr_list['data'][keys] is not None:"
    texts += 'Все значения соответствуют количеству валюты в одном долларе США. ' \
             'Информация по состоянию на ' + curr_list['meta']['last_updated_at']
    if len(texts) > 4096:
        for x in range(0, len(texts), 4096):
            bot.send_message(_message.chat.id, texts[x:x + 4096])
    else:
        bot.send_message(_message.chat.id, texts)
    return


def fmt_rnd(_v_to_round, _keys):
    # v_to_round = curr_list[_val1]['value']
    dec_dig = None  # нужна при выводе в консоль при отсутствии доп информации по валюте
    if _v_to_round < 0.0001:  # для малых значений ставим 10 знаков после запятой
        _s_rounded = '{0:.10f}'.format(_v_to_round)
    elif curr_info['data'][_keys] is not None:  # нашли доп инфо по валюте и берем из нее число знаков после запятой
        dec_dig = curr_info['data'][_keys]['decimal_digits']
        _s_rounded = '%.' + str(dec_dig) + 'f'
        _s_rounded = _s_rounded % _v_to_round
    else:  # доп инфо по валюте нет - выставляем обычный тип формата
        _s_rounded = '{0:f}'.format(_v_to_round)
    if float(_s_rounded) == 0:  # проверяем на потерю точности и правим ее по обнаружении
        _s_rounded = '*' + '{0:f}'.format(_v_to_round)
    return _s_rounded

"""
@bot.message_handler(filters)
def function_name(message):
    bot.reply_to(message, "This is a message handler")
"""


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    print(day_time_sender(message))
    name = str(message.chat.first_name)
    bot.send_message(message.chat.id, 'Привет тебе, ' + name + ', забредший сюда.')
    bot.send_message(message.chat.id, tb_settings.H_TEXT)
    
    
# Обрабатывается запрос конвертации валют
@bot.message_handler(commands=['e', 'ex', 'exch', 'exchange', 'elist'])
def handle_exchange(message):
    print(day_time_sender(message))
    cmd_ln = message.text.split()
    if cmd_ln[0] == '/elist':
        return
    
    if len(cmd_ln) == 4:  # обработка команды на конверсию
        try:    # просмотр по словарю наличие информации по запросу
            val1 = curr_info['data'][str(cmd_ln[1].upper())]['code']
            val2 = curr_info['data'][str(cmd_ln[2].upper())]['code']
            
            amount = float(str(cmd_ln[3]))
            if amount < 0:
                amount *= -1
            elif amount == 0:
                raise ValueError
            if val1 == val2:
                raise KeyError
        except KeyError:
            bot.send_message(message.chat.id, str('Код валюты введен с ошибкой!\n\n' + tb_settings.H_TEXT))
            print('Код валюты введен с ошибкой =', cmd_ln)
            return
        except ValueError:
            bot.send_message(message.chat.id, str('Число введено с ошибкой!\n\n' + tb_settings.H_TEXT))
            print('Число введено с ошибкой =', cmd_ln)
            return
        # наличие подтверждено
        ddg1 = curr_info['data'][val1]['decimal_digits']
        rate1 = curr_list['data'][val1]['value']
        
        ddg2 = curr_info['data'][val2]['decimal_digits']
        rate2 = curr_list['data'][val2]['value']
        
        result = amount * rate2 / rate1
        
        print(val1, ddg1, fmt_rnd(rate1, val1), rate1)
        print(val2, ddg2, fmt_rnd(rate2, val2), rate2)
        print(val1, ddg1, fmt_rnd(result, val1), result)
        
        
        
        dec_v1 = '%.' + str(curr_info['data'][val1]['decimal_digits']) + 'f'
        dec_v1 = dec_v1 % amount
        dec_v2 = '%.' + str(curr_info['data'][val2]['decimal_digits']) + 'f'
        dec_v2 = dec_v2 % result
        s = str(val1 + '=' + dec_v1 + ' <=> ' + val2 + '=' + dec_v2)
        print(s)
        bot.send_message(message.chat.id, s)
    else:
        bot.send_message(message.chat.id, str('Что Вы имели ввиду набрав:\n"' +
                                              str(cmd_ln) + '"?\n\n' + tb_settings.H_TEXT))
    

# Обрабатывается загрузка списка валют в словарь из запроса по API к сервису
@bot.message_handler(commands=['vload'])
def handle_load_values(message):
    global curr_list, curr_info
    print(day_time_sender(message))
    print(date_time_stamp(), 'запрос данных через API')
    curr_dummy = get_all_currency()
    if curr_dummy is not None:
        tb_dict_currency.currencies_list = curr_dummy
        curr_list = curr_dummy
        curr_dummy = get_all_currency_info()
        if curr_dummy is not None:
            tb_dict_currency.currencies_info = curr_dummy
            curr_info = curr_dummy
            return # все считалось
    print(date_time_stamp(), 'Нет связи с БД валют через API!')
    return


# Обрабатывается запрос списка валют
@bot.message_handler(commands=['v', 'val', 'value'])
def handle_values(message):
    print(day_time_sender(message))
    all_currency_list_out(message)  # вывод всех обслуживаемых валют и крипты
    return


# не обслуженный входной поток
@bot.message_handler(func=lambda message: True)
def other_messages(message):
    print(day_time_sender(message))
    bot.send_message(message.chat.id, str('Что Вы имели ввиду набрав:\n"' +
                                          message.text +
                                          '"? В помощь:\n' +
                                          tb_settings.H_TEXT))


"""
main +++++++++++++++++++++++++++++++++++++++++++
"""

print(date_time_stamp(), "Телеграмм бот по обмену валют запущен")


curr_list = tb_dict_currency.currencies_list
curr_info = tb_dict_currency.currencies_info
bot.infinity_polling()
# while True:
#     try:
#
#     except urllib3.exceptions.ReadTimeoutError:
#         break
#     except requests.exceptions.ReadTimeout:
#         break
print(date_time_stamp(), 'Что-то пошло не так!')

#
#

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