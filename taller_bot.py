"""
How are we going to call it? Please choose a name for your bot.
taller_bot

Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
Tallers_bot

t.me/Tallers_bot
"""
from tb_sec_set import TB_TOKEN
from extensions import *
import tb_dict_currency
import telebot
import pickle
import currencyapicom

client = currencyapicom.Client(CR_TOKEN)

bot = telebot.TeleBot(TB_TOKEN)

last_update = None
ut_last_checked = 0
curr_list = {}          # объявление рабочего списка валют
curr_info = {}          # объявление рабочего списка правил округления и обозначения валют
user_id = ''            # Идентификатор пользователя текущего сеанса
awaiting_curr_cont = False  # Флаг ожидания ввода валюты и числа
time_to_wait = UPD_INTERVAL_SEC  # время ожидания возможности обновления через API


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
    global user_id
    print(day_time_sender(message))
    name = str(message.chat.first_name)
    bot.send_message(message.chat.id, 'Приветствуем Вас, ' + name + '.\nЗдесь можно узнать котировки\n'
                                                                    'обычных и цифровых валют.')
    bot.send_message(message.chat.id, H_TEXT)
    user_id = str(message.chat.id)  # установка флага возможности просмотра подробной инструкции


# Обрабатываются сообщения, содержащие команду '/mentor для проверяющего
@bot.message_handler(commands=['mentor'])
def handle_start_help(message):
    global user_id
    print(day_time_sender(message))
    bot.send_message(message.chat.id, H_ADTN)
    
    
def check_instance_list(to_test=''):
    if to_test == '':
        return to_test
    if isinstance(to_test, list):
        return to_test
    else:
        return to_test.split()
    
    
def exchange_procedure(cmd_ln, message):
    global awaiting_curr_cont
    cmd_ln = check_instance_list(cmd_ln)    # проверка на наличие команды с атрибутами
    print(day_time_sender(message))
    if len(cmd_ln) == 4:  # обработка команды на конверсию
        try:  # просмотр по словарю наличие информации по запросу
            pair_rate = None
            pair_info = None
            if cmd_ln[0].lower() == '/elive':  # принудительный запрос двух валют через API  ++++++++++++++++++++
                pair_rate = API.get_currency_pair_rate(tb_db, str(cmd_ln[1].upper()), str(cmd_ln[2].upper()))
                pair_info = API.get_currency_pair_info(tb_db, str(cmd_ln[1].upper()), str(cmd_ln[2].upper()))
            else:
                ask_server_if_needed()  # проверка на необходимость обновления локальной базы котировок валют
            if pair_rate is not None:   # если считывали две валюты через API, нам сюда
                val1 = pair_rate['data'][str(cmd_ln[1].upper())]['code']
                val2 = pair_rate['data'][str(cmd_ln[2].upper())]['code']
            else:  # если считывания через API не было/не получилось, нам сюда, в локальную базу
                val1 = curr_info['data'][str(cmd_ln[1].upper())]['code']
                val2 = curr_info['data'][str(cmd_ln[2].upper())]['code']
            
            s_a = str(cmd_ln[3]).replace(',', '.')  # исправление десятичного разделителя на "автомате"
            
            amount = float(s_a)
            if amount < 0:
                amount *= -1  # исправление отрицательных чисел на "автомате"
            elif amount == 0:
                raise ValueError  # исключение обмена нулевых сумм
        except KeyError as e:
            bot.send_message(message.chat.id, str('Код валюты введен с ошибкой!\n' + str(e.args[0]) + '\n' + H_TEXT))
            print('Код валюты введен с ошибкой =', e.args[0])
            return
        except ValueError as e:
            err_str = 'Число введено с ошибкой!\n' + str(e) + '\n'
            bot.send_message(message.chat.id, err_str + '\n' + H_TEXT)
            print(err_str)
            return
        # наличие подтверждено, блок TRY не напакостил
        if pair_rate is not None:  # если запрашивали пару валют через API
            rate1 = pair_rate['data'][val1]['value']    # тут и возьмем
            rate2 = pair_rate['data'][val2]['value']
            if pair_info is not None:  # если при запросе еще и информацию по паре подтянули - тоже берем тут
                form_str1 = str(pair_info['data'][val1]['decimal_digits'])
                form_str2 = str(pair_info['data'][val2]['decimal_digits'])
            else:  # нет, информация не подтянулась, ошибка, то берем из локальной базы
                form_str1 = str(curr_info['data'][val1]['decimal_digits'])
                form_str2 = str(curr_info['data'][val2]['decimal_digits'])
        else:  # через API не запрашивали, берем курс и информацию из локальной базы
            rate1 = curr_list['data'][val1]['value']
            rate2 = curr_list['data'][val2]['value']
            form_str1 = str(curr_info['data'][val1]['decimal_digits'])
            form_str2 = str(curr_info['data'][val2]['decimal_digits'])
        result = amount * rate2 / rate1    # тут делаем то, ради чего все задумано
        
        dec_v1 = '%.' + form_str1 + 'f'    # оформляем по приличнее
        dec_v1 = dec_v1 % amount
        dec_v2 = '%.' + form_str2 + 'f'
        dec_v2 = dec_v2 % result
        s = str(val1 + '=' + dec_v1 + ' <=> ' + val2 + '=' + dec_v2)
        print(date_time_stamp(), s)               # выводим в консоль
        bot.send_message(message.chat.id, s)      # выводим в бот заказчику
    else:  # тут ясно, что заказчик не полностью ввел команду на обмен, предлагаем ему доделать по "быстрее"
        bot.send_message(message.chat.id, str('Введите две валюты и сколько надо '
                                              'первой из них?'))
        awaiting_curr_cont = True  # ставим флаг, открывающий эту "быстроту"
    return


# Обрабатывается запрос конвертации валют
@bot.message_handler(commands=['e', 'exchange', 'elive'])
def handle_exchange(_message):
    _cmd_ln = _message.text.split()
    exchange_procedure(_cmd_ln, _message)
    return


# Обрабатывается загрузка списка валют из запроса по API к сервису в словарь с его сохранением +++++++++++++++++++++++
@bot.message_handler(commands=['vload'])
def handle_load_values(message):
    print(day_time_sender(message))
    print(date_time_stamp(), 'Запрос данных через API')
    if ask_server():
        bot.send_message(message.chat.id, 'Успешно загружено ' + str(len(curr_list['data']))
                         + ' записей о доступных валютах')
    return


# Отрабатывается запись текущего словаря на диск
@bot.message_handler(commands=['vsave'])
def handle_save_values(message):
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
def handle_check_values_age(message):
    global time_to_wait
    print(day_time_sender(message))
    s = 'Время обновления базы котировок ' + ttw(time_to_wait)
    print(date_time_stamp(), 'Время "свежего" запроса к базе ',
          datetime.fromtimestamp(ut_last_checked).strftime('%d-%m-%Y %H:%M:%S'), s)
    bot.send_message(message.chat.id, curr_version() + '\n' + s + '\n\nИсточник данных:\nhttps://currencyapi.com\n')
    return


def currency_listing_procedure(message):
    print(day_time_sender(message))
    ask_server_if_needed()
    all_currency_list_out(message)  # вывод всех обслуживаемых валют и крипты
    return


# Обрабатывается запрос списка валют
@bot.message_handler(commands=['v', 'values'])
def handle_values(_message):
    currency_listing_procedure(_message)
    return


@bot.message_handler(func=lambda message: True)  # не обслуженный входной поток
def other_messages(message):
    global user_id, awaiting_curr_cont, time_to_wait
    print(day_time_sender(message))
    ms = message.text.lower()
    print(' ' * 20 + 'Парсинг нераспознанной команды:[' + ms + '] Message chat ID:', message.chat.id)
    if '/exchange ' in ms or '/e ' in ms:
        print(' ' * 20 + 'На исправление команды определения курса')
        exchange_procedure(ms, message)
        return
    if '/v' in ms or '/values' in ms:
        print(' ' * 20 + 'На исправление команды вывода списка валют')
        currency_listing_procedure(message)
        return
    if '/start' in ms or '/help' in ms or ms == '?':
        print(' ' * 20 + 'На исправление команды вывода справки')
        bot.send_message(message.chat.id, H_TEXT)
        user_id = str(message.chat.id)
        return
    if ms == '/more':
        if user_id == str(message.chat.id):
            s = 'Вывод подробной информации пользователю после просмотра им краткой справки'
            bot.send_message(message.chat.id, str(H_ADTN1))
        else:
            s = 'Вывод подробной информации пользователю только после просмотра краткой справки'
        print(' ' * 20 + s)
        user_id = ''
        return
    ms = message.text.lower().split()
    if ms[0] == 'time' and is_numeric(ms[1]):
        print(' ' * 20 + 'На установку времени обновления')
        time_to_wait = int(ms[1])
        if time_to_wait < 0:
            time_to_wait = -time_to_wait
        s = 'Время обновления базы котировок ' + ttw(time_to_wait)
        print(' ' * 20 + s)
        bot.send_message(message.chat.id, s)
        return
    if len(ms) == 1 and ms[0] == 'api':  # проверка на вкл\выкл API
        print(' ' * 20 + 'На API on/off')
        tb_db.api_bypass = not tb_db.api_bypass
        if tb_db.api_bypass:
            s = 'API bypass ON'
        else:
            s = 'API bypass OFF'
        print(' ' * 20 + s)
        bot.send_message(message.chat.id, s)
        return
    if len(ms) == 1 and ms[0] == 'list':  # проверка на вывод в консоль словарей
        print(' ' * 20 + 'Действующие словари')
        print('Котировки к доллару США')
        for keys, values in curr_list.items():
            for keys1, values1 in values.items():
                print(keys1, values1)
        print('\nПравила написания, округления и визуализации')
        for keys, values in curr_info.items():
            for keys1, values1 in values.items():
                print(keys1, values1)
        print(tb_db.err_report)
        print(' ' * 20 + '--------------------')
        bot.send_message(message.chat.id, 'В консоль выведено')
        return
    awaiting_curr_cont = True  # заглушка, позволяющая просто вводить валюты
    ms = message.text.upper().split()
    if awaiting_curr_cont:  # проверка на продолжение ввода валют
        print(' ' * 20 + 'На продолжение ввода валют')
        awaiting_curr_cont = False
        if len(ms) > 2:
            if ms[0] in curr_list['data'] and ms[1] in curr_info['data']:
                ms[2] = str(ms[2]).replace(',', '.')  # исправление десятичного разделителя на "автомате"
                if is_numeric(ms[2]):
                    ms.insert(0, '/e')
                    exchange_procedure(ms, message)
                    return
        print(' ' * 20 + 'Ошибка при вводе данных ' + str(ms))
        bot.send_message(message.chat.id, 'Вы ошиблись при вводе данных. Попробуйте еще раз.')
        return
    bot.send_message(message.chat.id, str('Что Вы имели ввиду набрав:\n"' + message.text +
                                          '"?\nВ помощь:' + H_TEXT))
    user_id = str(message.chat.id)
    return


def ttw(tt):
    if tt >= 3600:
        st = str(f'{tt / 3600:.2f}') + ' ч.'
    else:
        st = str(int(tt)) + ' сек.'
    return st


def is_numeric(s):  # проверка строки на содержание в ней целого или дробного десятичного числа
    try:
        float(s)
        return True
    except ValueError:
        return s.isnumeric()
        

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
    if (ts2-ts1) > time_to_wait:
        tf2 = (ts2-ts1) / 3600
        print(' ' * 23 + f'Превышено время ожидания на {tf2:.2f} ч ({int(ts2 - ts1):8} сек)')
    return (ts2-ts1) > time_to_wait


def default_load():
    global curr_list, curr_info
    curr_list = tb_dict_currency.currencies_list
    curr_info = tb_dict_currency.currencies_info
    return


def base_load():
    global curr_list, curr_info
    error_flag = 0
    if not_up_to_date():
        print(' ' * 23 + 'Устаревшие данные, загружаем из файлов.')
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
    print(date_time_stamp() + '    ' + info_str + ' ' + reorder_dt(last_update))
    return info_str + '\n' + reorder_dt(last_update)


def ask_server():
    global curr_list, curr_info
    load_ok = False
    curr_dummy = API.get_all_currency(tb_db, 'list')        # request to API
    if curr_dummy is not None:
        tb_dict_currency.currencies_list = curr_dummy
        curr_list = curr_dummy
        save_dict('tlbdata_cl.pkl')
        
        curr_dummy = API.get_all_currency(tb_db, 'info')    # request to API
        if curr_dummy is not None:
            tb_dict_currency.currencies_info = curr_dummy
            curr_info = curr_dummy
            save_dict('tlbdata_in.pkl')
            load_ok = True
    
    curr_version()
    return load_ok


def ask_server_if_needed():
    if not_up_to_date():
        print(' ' * 23 + 'Устаревшие данные, загружаем с сервера через API.')
        curr_version()
        ask_server()
    return


"""
main +++++++++++++++++++++++++++++++++++++++++++
"""
tb_db = API(curr_list, curr_info)
print(date_time_stamp(), "Телеграмм бот по обмену валют запущен")
print('Период ожидания обновления базы', ttw(time_to_wait))
print(H_ADTN)
default_load()  # загрузка словарей валюты и правил округления (по умолчанию - старые данные)
base_load()
ask_server_if_needed()
bot.infinity_polling()
print(date_time_stamp(), '\n\nЧто-то пошло не так!')  # Сюда попадаем если бот вылетает
