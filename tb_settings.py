"""
t.me/Tallers_bot
https://currencyapi.com/
"""
from tb_sec_set import CR_TOKEN

CR_REQUEST_CR_LIST = 'https://api.currencyapi.com/v3/currencies?apikey=' + CR_TOKEN
CR_REQUEST_CR_LATE = 'https://api.currencyapi.com/v3/latest?apikey=' + CR_TOKEN
UPD_INTERVAL_SEC = 86400 * 3

"""
https://api.currencyapi.com/v3/currencies?apikey=cur_live_uTjWnUO93FJA9mv5ptVsWD3H1XMm7o7zfLpNiod0&currencies=usd%2Crub
{
  "message": "Validation error",
  "errors": {
    "currencies": [
      "The selected currencies is invalid."
    ]
  },
  "info": "For more information, see documentation: https://currencyapi.com/docs/status-codes#_422"
}

https://api.currencyapi.com/v3/currencies?apikey=cur_live_uTjWnUO93FJA9mv5ptVsWD3H1XMm7o7zfLpNiod0&currencies=USD%2CRUB
{
  "data": {
    "RUB": {
      "symbol": "RUB",
      "name": "Russian Ruble",
      "symbol_native": "руб.",
      "decimal_digits": 2,
      "rounding": 0,
      "code": "RUB",
      "name_plural": "Russian rubles"
    },
    "USD": {
      "symbol": "$",
      "name": "US Dollar",
      "symbol_native": "$",
      "decimal_digits": 2,
      "rounding": 0,
      "code": "USD",
      "name_plural": "US dollars"
    }
  }
}

https://api.currencyapi.com/v3/latest?apikey=cur_live_uTjWnUO93FJA9mv5ptVsWD3H1XMm7o7zfLpNiod0&currencies=USD%2CRUB
https://api.currencyapi.com/v3/latest?apikey=cur_live_uTjWnUO93FJA9mv5ptVsWD3H1XMm7o7zfLpNiod0=USD%2CRUB
{
  "meta": {
    "last_updated_at": "2023-08-02T23:59:59Z"
  },
  "data": {
    "RUB": {
      "code": "RUB",
      "value": 93.9059812714
    },
    "USD": {
      "code": "USD",
      "value": 1
    }
  }
}
"""

H_TEXT = 'Команды бота-менялы:\n' \
             '/start, /help, /vinfo\n' \
             '/v,/val,/values - валюты\n' \
             '/e,/exch,/exchange в1 в2 скл\n' \
             '"валюта1" "валюта2" "сколько"\n' \
             '"валюта1" - ее покупаем\n' \
             '"валюта2" - ею платим\n' \
             '"сколько" - валюты1 покупаем\n' \
             'Пример: /exch rub usd 10\n' \
             'Буквы: большие и/или малые'

