"""
How are we going to call it? Please choose a name for your bot.
taller_bot

Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
Tallers_bot

t.me/Tallers_bot
"""
from tb_sec_set import TB_TOKEN
from tb_settings import *
from datetime import datetime
import tb_dict_currency
import telebot
import requests
import json
import pickle
# from extensions import APIexceptions
# import lxml
# import lxml.html
# from lxml import etree
# import urllib3

import currencyapicom
client = currencyapicom.Client(CR_TOKEN)

bot = telebot.TeleBot(TB_TOKEN)


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
    r = None
    try:
        r = requests.get(CR_REQUEST_CR_LATE)  # запрашиваем текущие курсы всех валют
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
    r = None
    try:
        r = requests.get(CR_REQUEST_CR_LIST)  # запрашиваем текущие курсы всех валют
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
        r = requests.get(CR_REQUEST_CR_LIST + val1 + "%2C" + val2)  # запрашиваем текущие курсы двух валют
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
                try:  # дополнительная информация о валюте есть
                    s = curr_info['data'][keys]['name_plural'] + '\n'
                except TypeError:  # ошибка в информационном описании валюты
                    print('For key = [' + keys + ']')  # беду в консоль
                    print(curr_info['data'][keys])
                else:  # дополнительной информации о валюте нет
                    pass
            v_to_round = curr_list['data'][keys]['value']
            s_rounded = fmt_rnd(v_to_round, keys)
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
    bot.send_message(message.chat.id, H_TEXT)
    
    
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
            bot.send_message(message.chat.id, str('Код валюты введен с ошибкой!\n\n' + H_TEXT))
            print('Код валюты введен с ошибкой =', cmd_ln)
            return
        except ValueError:
            bot.send_message(message.chat.id, str('Число введено с ошибкой!\n\n' + H_TEXT))
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
                                              str(cmd_ln) + '"?\n\n' + H_TEXT))
    

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
            curr_info = curr_dummy  # все считалось
            with open('tlbdatacl.pkl', 'wb') as f:  # сохраним в файл
                pickle.dump(tb_dict_currency.currencies_list, f)
            with open('tlbdatain.pkl', 'wb') as f:  # сохраним в файл
                pickle.dump(tb_dict_currency.currencies_info, f)
            return
    print(date_time_stamp(), 'Нет связи с БД валют через API!')
    return


# Обрабатывается записи словаря из запроса по API к сервису на диск
@bot.message_handler(commands=['w'])
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
            return  # все считалось
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
                                          H_TEXT))


def reorder_dt(rs):
    s = rs[8:10] + '-' + rs[5:7] + '-' + rs[0:4] + ' ' + rs[11:19]
    return s


def load_dict(fn, dict_struct):
    try:
        with open(fn, 'rb') as f:
            dict_struct = pickle.load(f)
            print('Загружена база', fn, '\n', dict_struct)
            return True
    except FileNotFoundError:
        print('Файл ', fn, 'загрузить с диска не удалось. Используется старый.')
    except UnicodeDecodeError:
        print('Файл ', fn, 'содержит ошибки. Используется старый.')
    except pickle.UnpicklingError:
        print('Файл ', fn, 'содержит ошибки. Используется старый.')
    return False


def save_dict(fn, dict_struct):
    try:
        with open(fn, 'wb') as f:
            pickle.dump(dict_struct, f)
            print('Записан файл', fn, '\n', dict_struct)
            return True
    except FileNotFoundError:
        print('Файл ', fn, 'записать на диск не удалось.')
    except UnicodeDecodeError:
        print('Файл ', fn, 'содержит ошибки.')
    except pickle.UnpicklingError:
        print('Файл ', fn, 'содержит ошибки.')
    return False


def not_up_to_date():
    last_update = curr_list['meta']['last_updated_at']
    print(reorder_dt(last_update), 'Загруженная версия котировок.')
    ts1 = datetime(int(last_update[0:4]),
                   int(last_update[5:7]),
                   int(last_update[8:10]),
                   int(last_update[11:13]),
                   int(last_update[14:16]),
                   int(last_update[17:19])) \
        .timestamp()
    ts2 = datetime.now().timestamp()
    return (ts2-ts1) > UPD_INTERVAL_SEC


def base_load():
    global curr_list, curr_info
    error_flag = 0
    if not_up_to_date():
        print('Устаревшие данные, загружаем из файлов.')
        if not load_dict('tlbdatacl.pkl', tb_dict_currency.currencies_list):
            error_flag += 1
        if not load_dict('tlbdatain.pkl', tb_dict_currency.currencies_info):
            error_flag += 2
    
    if error_flag & 1 != 1:
        curr_list = tb_dict_currency.currencies_list
        
    if error_flag & 2 != 2:
        curr_info = tb_dict_currency.currencies_info
    
    last_update = reorder_dt(tb_dict_currency.currencies_list['meta']['last_updated_at'])
    print(last_update, 'используемая версия котировок.')
    return error_flag


"""
main +++++++++++++++++++++++++++++++++++++++++++
"""
print(date_time_stamp(), "Телеграмм бот по обмену валют запущен")
# загрузка словарей валюты и правил округления (по умолчанию - старые данные)
curr_list = tb_dict_currency.currencies_list
curr_info = tb_dict_currency.currencies_info
base_load()

#bot.infinity_polling()

#print(date_time_stamp(), '\n\nЧто-то пошло не так!')
