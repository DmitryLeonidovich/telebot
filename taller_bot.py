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
from extensions import NoLinkToDB
import tb_dict_currency
import telebot
import requests
import json
import pickle
import currencyapicom

client = currencyapicom.Client(CR_TOKEN)

bot = telebot.TeleBot(TB_TOKEN)

last_update = None
ut_last_checked = 0
curr_list = {}          # объявление рабочего списка валют
curr_info = {}          # объявление рабочего списка правил округления и обозначения валют


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


def get_all_currency(mode='list'):
    mode_type = 'котировки валюты'
    r = None
    _curr = None
    se = ''
    if mode == 'list':
        mode = CR_REQUEST_CR_LATE
    elif mode == 'info':
        mode_type = 'инфо по валюте'
        mode = CR_REQUEST_CR_LIST
    try:
        r = requests.get(mode)  # запрашиваем данные всех валют
        _curr = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы
        if r.status_code != 200:
            _curr = None
            raise NoLinkToDB(r.status_code)
    except requests.exceptions.ConnectionError as e:
        se = e
    except requests.exceptions.ReadTimeout as e:
        se = e
    except TypeError as e:
        se = e
    except NoLinkToDB as e:
        se = 'Обращение к API ['+ mode_type + '] ' + e.e_code
    else:
        print(f'RAW response of {len(r.content)} bytes :\n', r.content)
        print('Number of currencies', len(_curr['data']))
    finally:
        if se != '':
            print(date_time_stamp(), '! ', se)
    return _curr


def get_currency_pair_rate(val1, val2):  # запрашиваем текущие курсы двух валют
    return get_all_currency(CR_REQUEST_CR_LATE + '&currencies=' + val1 + "%2C" + val2)


def get_currency_pair_info(val1, val2):  # запрашиваем текущие курсы двух валют
    return get_all_currency(CR_REQUEST_CR_LIST + '&currencies=' + val1 + "%2C" + val2)


def all_currency_list_out(_message):
    print(date_time_stamp(), 'передача списка обслуживаемых валют')
    texts = ''
    for keys in curr_list['data'].keys():
        if curr_list['data'][keys] is not None:
            s = ''
            if curr_info['data'][keys] is not None:
                try:    # дополнительная информация о валюте есть
                    s = curr_info['data'][keys]['name_plural'] + '\n'
                except TypeError:  # ошибка в информационном описании валюты
                    print('For key = [' + keys + ']')  # беду в консоль
                    print(curr_info['data'][keys])
                else:   # дополнительной информации о валюте нет
                    pass
            v_to_round = curr_list['data'][keys]['value']
            s_rounded = fmt_rnd(v_to_round, keys)
            s += curr_list['data'][keys]['code'] + '\t = ' + s_rounded
            texts += s + '\n'
            if len(texts) > 4000:
                bot.send_message(_message.chat.id, texts)  # вывод в бот первой части списка сообщением
                texts = ''
        # end of "if curr_list['data'][keys] is not None:"
    texts += 'Все значения соответствуют количеству валюты в одном долларе США. ' \
             'Информация по состоянию на ' + reorder_dt(curr_list['meta']['last_updated_at'])
    if len(texts) > 4096:
        for x in range(0, len(texts), 4096):
            bot.send_message(_message.chat.id, texts[x:x + 4096])
    else:
        bot.send_message(_message.chat.id, texts)
    return


def fmt_rnd(_v_to_round, _keys):
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


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    print(day_time_sender(message))
    name = str(message.chat.first_name)
    bot.send_message(message.chat.id, 'Привет тебе, ' + name + ', забредший сюда.')
    bot.send_message(message.chat.id, H_TEXT)
    
    
# Обрабатывается запрос конвертации валют
@bot.message_handler(commands=['e', 'ex', 'exch', 'exchange', 'elive'])
def handle_exchange(message):
    print(day_time_sender(message))
    cmd_ln = message.text.split()
    if len(cmd_ln) == 4:  # обработка команды на конверсию
        try:    # просмотр по словарю наличие информации по запросу
            pair_rate = None
            pair_info = None
            if cmd_ln[0] == '/elive':               # принудительный запрос двух валют через API  ++++++++++++++++++++
                pair_rate = get_currency_pair_rate(str(cmd_ln[1].upper()), str(cmd_ln[2].upper()))
                pair_info = get_currency_pair_info(str(cmd_ln[1].upper()), str(cmd_ln[2].upper()))
            if pair_rate is not None:
                val1 = pair_rate['data'][str(cmd_ln[1].upper())]['code']
                val2 = pair_rate['data'][str(cmd_ln[2].upper())]['code']
            else:
                val1 = curr_info['data'][str(cmd_ln[1].upper())]['code']
                val2 = curr_info['data'][str(cmd_ln[2].upper())]['code']
                
            s_a = str(cmd_ln[3])    # исправление десятичного разделителя на "автомате" с продолжением работы
            s_a = s_a.replace(',', '.')
            amount = float(s_a)
            if amount < 0:
                amount *= -1        # исправление отрицательных чисел на "автомате" с продолжением работы
            elif amount == 0:
                raise ValueError    # исключение обмена нулевых сумм
        except KeyError as e:
            bot.send_message(message.chat.id, str('Код валюты введен с ошибкой!\n' + str(e.args[0]) + '\n' + H_TEXT))
            print('Код валюты введен с ошибкой =', e.args[0])
            return
        except ValueError as e:
            err_str = 'Число введено с ошибкой!\n' + str(e) + '\n'
            bot.send_message(message.chat.id, err_str + '\n' + H_TEXT)
            print(err_str)
            return
        # наличие подтверждено
        if pair_rate is not None:
            rate1 = pair_rate['data'][val1]['value']
            rate2 = pair_rate['data'][val2]['value']
            if pair_info is not None:
                form_str1 = str(pair_info['data'][val1]['decimal_digits'])
                form_str2 = str(pair_info['data'][val2]['decimal_digits'])
            else:
                form_str1 = str(curr_info['data'][val1]['decimal_digits'])
                form_str2 = str(curr_info['data'][val2]['decimal_digits'])
        else:
            rate1 = curr_list['data'][val1]['value']
            rate2 = curr_list['data'][val2]['value']
            form_str1 = str(curr_info['data'][val1]['decimal_digits'])
            form_str2 = str(curr_info['data'][val2]['decimal_digits'])
        result = amount * rate2 / rate1
        
        dec_v1 = '%.' + form_str1 + 'f'
        dec_v1 = dec_v1 % amount
        dec_v2 = '%.' + form_str2 + 'f'
        dec_v2 = dec_v2 % result
        s = str(val1 + '=' + dec_v1 + ' <=> ' + val2 + '=' + dec_v2)
        print(date_time_stamp(), s)
        bot.send_message(message.chat.id, s)
    else:
        bot.send_message(message.chat.id, str('Что Вы имели ввиду набрав:\n"' +
                                              str(cmd_ln) + '"?\n\n' + H_TEXT))
    

# Обрабатывается загрузка списка валют из запроса по API к сервису в словарь с его сохранением +++++++++++++++++++++++
@bot.message_handler(commands=['vload'])
def handle_load_values(message):
    print(day_time_sender(message))
    print(date_time_stamp(), 'Запрос данных через API')
    ask_server()
    return


# Отрабатывается запись текущего словаря на диск
@bot.message_handler(commands=['vsave'])
def handle_load_values_and_wright(message):
    print(day_time_sender(message))
    print(date_time_stamp(), 'Запись базы на диск.')
    ss2 = 'tlbdata_cl.pkl '
    if not save_dict('tlbdata_cl.pkl'):
        ss2 += 'не '
    ss2 += 'сохранен, tlbdata_in.pkl '
    if not save_dict('tlbdata_in.pkl'):
        ss2 += 'не '
    ss2 += 'сохранен'
    bot.send_message(message.chat.id, ss2)
    return


# Отрабатывается информация об используемой версии базы валют
@bot.message_handler(commands=['vinfo'])
def handle_load_values_and_wright(message):
    print(day_time_sender(message))
    print(date_time_stamp(), 'Время "свежего" запроса к базе ',
          datetime.fromtimestamp(ut_last_checked).strftime('%d-%m-%Y %H:%M:%S'))
    bot.send_message(message.chat.id, curr_version())
    return


# Обрабатывается запрос списка валют
@bot.message_handler(commands=['v', 'val', 'values'])
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
    return rs[8:10] + '-' + rs[5:7] + '-' + rs[0:4] + ' ' + rs[11:19]


def load_dict(fn):
    print(date_time_stamp(), end=' <- ')
    dict_struct = None
    try:
        with open(fn, 'rb') as f:
            dict_struct = pickle.load(f)
            print('Загружена база из файла', fn)
    except FileNotFoundError:
        print('Файл ', fn, 'загрузить с диска не удалось. Используется старый.')
    except UnicodeDecodeError:
        print('Файл ', fn, 'содержит ошибки. Используется старый.')
    except pickle.UnpicklingError:
        print('Файл ', fn, 'содержит ошибки. Используется старый.')
    return dict_struct


def save_dict(fn):
    print(date_time_stamp(), end=' -> ')
    try:
        with open(fn, 'wb') as f:
            if fn == 'tlbdata_cl.pkl':
                pickle.dump(curr_list, f)
            elif fn == 'tlbdata_in.pkl':
                pickle.dump(curr_info, f)
            else:
                raise FileNotFoundError
            print('Записан файл', fn)
            return True
    except PermissionError:
        print('Файл ', fn, 'записать на диск не удалось.')
    except UnicodeDecodeError:
        print('Файл ', fn, 'содержит ошибки.')
    except pickle.UnpicklingError:
        print('Файл ', fn, 'содержит ошибки.')
    return False


def not_up_to_date():
    global last_update, ut_last_checked
    curr_version()
    ts1 = datetime(int(last_update[0:4]),
                   int(last_update[5:7]),
                   int(last_update[8:10]),
                   int(last_update[11:13]),
                   int(last_update[14:16]),
                   int(last_update[17:19])) \
        .timestamp()
    ts2 = datetime.now().timestamp()
    ut_last_checked = ts2
    return (ts2-ts1) > UPD_INTERVAL_SEC


def default_load():
    global curr_list, curr_info
    curr_list = tb_dict_currency.currencies_list
    curr_info = tb_dict_currency.currencies_info
    return


def base_load():
    global curr_list, curr_info
    error_flag = 0
    if not_up_to_date():
        print('Устаревшие данные, загружаем из файлов.')
        d_s = load_dict('tlbdata_cl.pkl')
        if d_s is not None:
            tb_dict_currency.currencies_list = d_s
        else:
            error_flag += 1
        d_s = load_dict('tlbdata_in.pkl')
        if d_s is not None:
            tb_dict_currency.currencies_info = d_s
        else:
            error_flag += 2
    if error_flag & 1 != 1:
        curr_list = tb_dict_currency.currencies_list
    if error_flag & 2 != 2:
        curr_info = tb_dict_currency.currencies_info
    curr_version('Загружена версия котировок от')
    return error_flag
    

def curr_version(info_str='Используется версия котировок от'):
    global last_update
    last_update = curr_list['meta']['last_updated_at']
    # s_out = date_time_stamp() + '    ' + info_str + ' ' + reorder_dt(last_update)
    print(date_time_stamp() + '    ' + info_str + ' ' + reorder_dt(last_update))
    return info_str + '\n' + reorder_dt(last_update)


def ask_server():
    global curr_list, curr_info
    
    curr_dummy = get_all_currency('list')
    if curr_dummy is not None:
        tb_dict_currency.currencies_list = curr_dummy
        curr_list = curr_dummy
        save_dict('tlbdata_cl.pkl')
        
        curr_dummy = get_all_currency('info')
        if curr_dummy is not None:
            tb_dict_currency.currencies_info = curr_dummy
            curr_info = curr_dummy
            save_dict('tlbdata_in.pkl')
            
    curr_version()
    return


def ask_server_if_needed():
    if not_up_to_date():
        print('Устаревшие данные, загружаем с сервера через API.')
        curr_version()
        ask_server()
    return


"""
main +++++++++++++++++++++++++++++++++++++++++++
"""
print(date_time_stamp(), "Телеграмм бот по обмену валют запущен")
print('Период ожидания обновления базы', UPD_INTERVAL_SEC / 3600, ' часов')
default_load()  # загрузка словарей валюты и правил округления (по умолчанию - старые данные)
base_load()
ask_server_if_needed()
bot.infinity_polling()
print(date_time_stamp(), '\n\nЧто-то пошло не так!')  # Сюда попадаем если бот вылетает
