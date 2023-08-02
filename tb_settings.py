"""
How are we going to call it? Please choose a name for your bot.
taller_bot

Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
Tallers_bot

Use this token to access the HTTP API:
5945616553:AAFU_h6Kg3JuHOx-Chppj1tD8JF1s932N5Q
Keep your token secure and store it safely, it can be used by anyone to control your bot.

t.me/Tallers_bot
"""
from tb_sec_set import CR_TOKEN

CR_REQUEST_CR_LIST = 'https://api.currencyapi.com/v3/currencies?apikey=' + CR_TOKEN
CR_REQUEST_CR_LATE = 'https://api.currencyapi.com/v3/latest?apikey=' + CR_TOKEN
UPD_INTERVAL_SEC = 86400

H_TEXT = 'Команды бота-менялы:\n' \
             '/v,/val,/values - валюты\n' \
             '/e,/exch,/exchange в1 в2 скл\n' \
             '"валюта1" "валюта2" "сколько"\n' \
             '"валюта1" - ее покупаем\n' \
             '"валюта2" - ею расплачиваемся\n' \
             '"сколько" - валюты1 покупаем\n' \
             'Пример: /exch rub usd 10'


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
