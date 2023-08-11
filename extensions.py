"""
Файл с модулями обработки ошибок, запросов API и JSON
"""

from tb_settings import *
from datetime import datetime
import requests
import json


def date_time_stamp(date_message=None):
    if date_message is not None:
        return datetime.fromtimestamp(int(date_message)).strftime('%d-%m-%Y %H:%M:%S')
    else:
        return datetime.now().strftime('%d-%m-%Y %H:%M:%S')


class APIexceptions(Exception):
    pass


class NoLinkToDB(APIexceptions):
    def __init__(self, _e_code=200, _se=''):
        self.e_code = _e_code
        self.se = _se
        rsc_dict = {
            200: 'Все ОК',
            403: "Нет прав на использование сервиса",
            422: "Запрос был с ошибкой",
            429: "Число запросов к сервису превышено",
            500: "На сервере беда. Что-то пошло не так"
        }
        e_legal = [200, 403, 422, 429, 500]
        if _e_code in e_legal:
            self.se = f' [{self.e_code}] {rsc_dict[self.e_code]} : {self.se}'
        else:
            self.se = "Unexpected error"
    
    def __add__(self, other):
        return self.se + ' ' + other
    
    
class API:
    def __init__(self, _curr_rate=None, _curr_info=None):  #
        self.err_report = ''
        self.api_bypass = False     # Флаг пропуска реального запроса к API
        self._cu_list = _curr_rate
        self._cu_info = _curr_info
    
    @staticmethod   # Tо, что в задании называется "get_price()", а два параметра сидят в "mode"."amount" тут не нужен
    def get_all_currency(self, mode='list'):
        
        mode_type = 'котировки валюты'
        r = None
        _curr = None
        se = ''
        if mode == 'list':
            mode = CR_REQUEST_CR_LATE
        elif mode == 'info':
            mode_type = 'информация о валюте'
            mode = CR_REQUEST_CR_LIST
        try:
            print(' ' * 23 + 'API request has started')
            if self.api_bypass:
                return _curr  # пропускаем обращение к API
            r = requests.get(mode)  # запрашиваем данные валют в соответствии с запросом
            _curr = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы
            if r.status_code != 200:
                if r.status_code == 422:
                    s = str(*_curr["errors"]["currencies"])
                    self.err_report = s
                raise NoLinkToDB(r.status_code, s)
        except requests.exceptions.ConnectionError as e:
            se = e
        except requests.exceptions.ReadTimeout as e:
            se = e
        except TypeError as e:
            se = e
        except NoLinkToDB as e:
            se = 'API Error [' + mode_type + '] ' + e.se
        else:  # Ошибок нет, выведем в консоль полученные данные и число валют
            print(f'RAW response of {len(r.content)} bytes :\n', r.content)
            print('Number of currencies', len(_curr['data']))
        finally:   # Выйдем из блока обращения к API не забыв дать сообщение если была ошибка
            if se != '':
                self.err_report = f'{date_time_stamp()} !! {se}'
                print(self.err_report)
                _curr = None
            elif self.api_bypass:
                self.err_report = ''
                print(mode)
                print(' ' * 25 + 'API request bypass!')
                _curr = None
            print(' ' * 23 + 'API request ended')
        return _curr
    
    def get_currency_pair_rate(self, val1, val2):  # запрашиваем текущие курсы двух валют
        return API.get_all_currency(self, CR_REQUEST_CR_LATE + '&currencies=' + val1 + "%2C" + val2)
    
    def get_currency_pair_info(self, val1, val2):  # запрашиваем текущую информацию курсы двух валют
        return API.get_all_currency(self, CR_REQUEST_CR_LIST + '&currencies=' + val1 + "%2C" + val2)

if __name__ == '__main__':
    print('Не тот файл запустили!')