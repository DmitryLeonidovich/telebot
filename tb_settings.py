"""
t.me/Tallers_bot
https://currencyapi.com/
"""
from tb_sec_set import CR_TOKEN

CR_REQUEST_CR_LIST = 'https://api.currencyapi.com/v3/currencies?apikey=' + CR_TOKEN
CR_REQUEST_CR_LATE = 'https://api.currencyapi.com/v3/latest?apikey=' + CR_TOKEN
UPD_INTERVAL_SEC = 86400 * 1.2

"""
https://api.currencyapi.com/v3/currencies?apikey=cur_live_JA9mv5ptVsWD3H1XMm7o7zfLpNiod0&currencies=usd%2Crub
{
  "message": "Validation error",
  "errors": {
    "currencies": [
      "The selected currencies is invalid."
    ]
  },
  "info": "For more information, see documentation: https://currencyapi.com/docs/status-codes#_422"
}

https://api.currencyapi.com/v3/currencies?apikey=cur_live_JA9mv5ptVsWD3H1XMm7o7zfLpNiod0&currencies=USD%2CRUB
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

https://api.currencyapi.com/v3/latest?apikey=cur_live_JA9mv5ptVsWD3H1XMm7o7zfLpNiod0&currencies=USD%2CRUB
https://api.currencyapi.com/v3/latest?apikey=cur_live_JA9mv5ptVsWD3H1XMm7o7zfLpNiod0=USD%2CRUB
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

H_TEXT = '\nПример команды бота-менялы:\n\n' \
         '/exchange USD RUB 10\n\n' \
         'USD - ее покупаем\n' \
         'RUB - ею платим\n' \
         '10 - сколько USD покупаем\n\n' \
         'Можно так:\n/e,   /exchange\n' \
         'Список доступных валют\n' \
         '/v,   /values\n' \
         'Справочные команды:\n' \
         '/start,   /help,   ?\n' \
         'Буквы латинские любые.\n' \
         'Подробнее, нажмите:\n/more\n'

H_ADTN = 'Уголок Ментора.\nИспользуемый API сервис для бесплатного тарифного плана поставляет ' \
         'данные котировок только раз в сутки.\nВыбрать базовую валюту тоже нельзя. Пересчет идет через доллар США.\n' \
         'В месяц позволительно сделать только 300 запросов к сервису.\n' \
         'В связи с этим, при написании бота использована модель системы с локальной базой котировок.\n' \
         'При старте бот загружает "древнюю" версию котировок из тела программы, ' \
         'затем смотрит в директории программы наличие файлов с котировками и информацией по валютам.\n' \
         'Если они есть, загружает их, и проверяет "свежесть".\nЕсли на диске они более свежие - заменяет ' \
         'ими рабочую базу в программе.\nЗатем бот обращается к сервису  через API и запрашивает ' \
         'актуальную информацию по валютам.\nЕсли связи нет - работает загруженная из директории бота база валют, ' \
         'если связь есть - актуальная база считывается и сохраняется на диск бота и ' \
         'обновляет рабочую базу в программе.\nВы можете отправить боту сообщение "time 3600" и ' \
         'время ожидания необходимости обновления базы котировок через API станет 1 час. ' \
         'Время указывается в секундах.\nСообщение "api" - выключит/включит отправку запроса к сервисам API. ' \
         'При выключенной, в консоль выведется ссылка запроса к API.\nСообщение "list" выведет действующие ' \
         'словари котировок и информации в консоль.\n\nСлужебные команды со стороны пользователя. ' \
         '\nВводить их нужно именно так, как тут показано, коррекция ошибок при ' \
         'вводе для обычных команд здесь не используется:\n' \
         'Запрос в реальном времени пары валют через API:\n' \
         '/elive USD RUB 10\n' \
         'Обновление базы валют через API с сохранением на диск бота:\n' \
         '/vload\n' \
         'Создание базы валют на диске бота:\n' \
         '/vsave\n' \
         'Информация о последнем обращении к API:\n' \
         '/vinfo\n\n' \
         'Источник данных:\nhttps://currencyapi.com\n'

H_ADTN1 = '\n'\
         'Пояснение по правилам ввода команды конвертации валют ' \
         'на примере приобретения долларов США за российские рубли:\n' \
         'Введите символ "/" и слово "exchange".\n' \
         'Через пробел введите код валюты "USD" или "usd", которую вы хотите купить.\n' \
         'Через пробел введите код валюты "RUB" или "rub", которой ' \
         'вы планируете оплачивать приобретение долларов США.\n' \
         'Через пробел введите сколько долларов США вы планируете приобрести.\n' \
         'Копейки, центы и дробные части отделяйте от целых символами "." или ",".\n' \
         'Например, у вас получилась команда:\n"/exchange USD RUB 10.15"\n' \
         'Она сообщит боту, что вы хотите приобрести 10 долларов 15 центов ' \
         'США за российские рубли.\nНажмите кнопку "Отправить".\nВам придет ответ:\n' \
         '"USD=10.15 <=> RUB=986.55"\n' \
         'Это взаимно-однозначное соотношение количеств долларов США и российских рублей.\n' \
         'Для приобретения 10 долларов 15 центов США вам нужно потратить 986 рублей 55 копеек.\n' \
         'Для ускорения процесса можно выбирать синие команды на экране вашего устройства.\n' \
         'Еще быстрее - вводите две валюты и интересующую сумму первой валюты через пробел.\n\n' \
         'Источник данных:\nhttps://currencyapi.com\n'


if __name__ == '__main__':
    print(H_TEXT)
    print(H_ADTN1)
    print(H_ADTN)