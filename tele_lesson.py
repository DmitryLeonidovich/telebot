import requests
import json

r = requests.get(  # делаем запрос на сервер по переданному адресу
    'https://baconipsum.com/api/?type=all-meat&paras=3&start-with-lorem=1&format=html')
print(r.content)
print(r.status_code)  # узнаем статус полученного ответа

r = requests.get('https://baconipsum.com/api/?type=meat-and-filler')  # попробуем поймать json-ответ
print(r.content)

texts = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы
print(type(texts))  # проверяем тип сконвертированных данных

for text in texts:  # выводим полученный текст. Но для того чтобы он влез в консоль, оставим только первые 50 символов.
    print(text[:50], '\n')

r = requests.get('https://api.github.com')

print(r.content)

d = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы

print(type(d))
print(d['following_url'])  # обращаемся к полученному объекту как к словарю и попробуем напечатать одно из его значений

r = requests.post('https://192.168.10.161', data = {'key':'$KE,TMP'})  # отправляем POST-запрос
print(r.content)  # содержимое ответа и его обработка происходит так же, как и с GET-запросами, разницы никакой нет

data = {'key': 'value'}

r = requests.post('http://httpbin.org/post', json=json.dumps(
    data))  # отправляем POST-запрос, но только в этот раз тип передаваемых данных будет JSON
print(r.content)