"""
t.me/Tallers_bot
https://currencyapi.com/
"""
from tb_sec_set import CR_TOKEN

CR_REQUEST_CR_LIST = 'https://api.currencyapi.com/v3/currencies?apikey=' + CR_TOKEN
CR_REQUEST_CR_LATE = 'https://api.currencyapi.com/v3/latest?apikey=' + CR_TOKEN
UPD_INTERVAL_SEC = 86400 * 2

H_TEXT = 'Команды бота-менялы:\n' \
             '/v,/val,/values - валюты\n' \
             '/e,/exch,/exchange в1 в2 скл\n' \
             '"валюта1" "валюта2" "сколько"\n' \
             '"валюта1" - ее покупаем\n' \
             '"валюта2" - ею расплачиваемся\n' \
             '"сколько" - валюты1 покупаем\n' \
             'Пример: /exch rub usd 10'
