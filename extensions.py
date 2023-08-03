"""

"""

import tb_settings
import requests
import json

class APIexceptions(Exception):
    def __init__(self):
        pass
    
class NoLinkToDB(APIexceptions):
    def __init__(self, errmsg=''):
        self.errmsg = "API error:" + errmsg
    
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
    