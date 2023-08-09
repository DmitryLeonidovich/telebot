"""

"""

import tb_settings
import requests
import json

class APIexceptions(Exception):
    pass


class NoLinkToDB(APIexceptions):
    def __init__(self, e_code):
        rsc_dict = {
            200: 'Все ОК',
            403: "Нет прав на использование сервиса",
            422: "Запрос был с ошибкой",
            429: "Число запросов к сервису превышено",
            500: "На сервере беда. Что-то пошло не так"
        }
        e_legal = [200, 403, 422, 429, 500]
        if e_code in e_legal:
            self.e_code = rsc_dict[e_code]
        else:
            self.e_code = "Unexpected error"
    
    def __add__(self, other):
        return self + ' ' + other
    
    
class API:
    def __init__(self, _curr_rate=None, _curr_info=None):
        _cu_list = _curr_rate
        _cu_info = _curr_info
    
    def get_price(self, _base, _quote, _amount ):
        pass
    
    def get_curr_late(self):
        r = requests.get(tb_settings.CR_REQUEST_CR_LATE)  # запрашиваем текущие курсы всех валют
        print(f'RAW responce of {len(r.content)} bytes :\n', r.content)
        print('Status code : ', r.status_code)  # узнаем статус полученного ответа
        curr = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы
        print(len(curr['data']))
    