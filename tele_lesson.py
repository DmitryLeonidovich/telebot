import requests
import json
import lxml
import lxml.html
from lxml import etree

r = requests.get(  # делаем запрос на сервер по переданному адресу
    'https://baconipsum.com/api/?type=all-meat&paras=3&start-with-lorem=1&format=html')
print(r.content)
print(r.status_code)  # узнаем статус полученного ответа
print()

r = requests.get('https://baconipsum.com/api/?type=meat-and-filler')  # попробуем поймать json-ответ
print(r.content)
print(r.status_code)  # узнаем статус полученного ответа
print()

print('To JSON conversion')
texts = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы
print(type(texts))  # проверяем тип сконвертированных данных
print()

for text in texts:  # выводим полученный текст. Но для того чтобы он влез в консоль, оставим только первые 50 символов.
    print(text[:50], '\n')
print()

r = requests.get('https://api.github.com')

print(r.content)

d = json.loads(r.content)  # делаем из полученных байтов Python-объект для удобной работы

print(type(d))
print(d['following_url'])  # обращаемся к полученному объекту как к словарю и попробуем напечатать одно из его значений

data = {'key': 'value'}

r = requests.post('http://httpbin.org/post', json=json.dumps(
    data))  # отправляем POST-запрос, но только в этот раз тип передаваемых данных будет JSON
print(r.content)

print('\n\n')



html = requests.get('https://www.python.org/').content  # получим html главной странички официального сайта python

tree = lxml.html.document_fromstring(html)
title = tree.xpath('/html/head/title/text()')
                                                # забираем текст тега <title> из тега <head>,
                                                # который лежит в свою очередь внутри тега <html>
                                                # (в этом невидимом теге <head> у нас хранится основная информация
                                                # о страничке, её название и инструкции по отображению в браузере)

print(title)  # выводим полученный заголовок страницы

# Создадим объект ElementTree. Он возвращается функцией parse()
tree = etree.parse('Welcome to Python.org.html', lxml.html.HTMLParser())
                    # попытаемся спарсить наш файл с помощью html-парсера.
                    # Сам html - это то, что мы скачали и поместили в папку из браузера.

ul = tree.findall('/body/div/div[3]/div/section/div[2]/div[1]/div/ul/li')
                    # помещаем в аргумент метода findall скопированный xpath.
                    # Здесь мы получим все элементы списка новостей. (Все заголовки и их даты)

# создаём цикл, в котором мы будем выводить название каждого элемента из списка
for li in ul:
    a = li.find('a')    # в каждом элементе находим, где хранится заголовок новости.
                        # У нас это тег <a>. Т. е. гиперссылка, на которую нужно нажать, чтобы перейти
                        # на страницу с новостью. (Гиперссылки в html это всегда тег <a>)
    time = li.find('time')
    print(time.get('datetime'), a.text)  # из этого тега забираем текст, это и будет нашим названием