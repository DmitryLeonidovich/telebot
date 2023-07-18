import requests
import socket

HOST = "192.168.10.101"  # interface address
PORT = 2424  # Port to data exchange

@bot.message_handler(commands=['temp'])
def handle_start_help(message):
    name = str(message.chat.first_name)
    print('Пришел запрос температуры от ', name)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b'$KE,TMP\r\n')
        data = s.recv(1024)
        s.close()
    data_str = str(data)[7:11] + '\xB0С'
    print('Выслали вот такую температуру ', data_str)
    bot.send_message(message.chat.id, 'В доме ' + data_str)

bot.polling(none_stop=True)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(b'$KE,TMP\r\n')
    data = s.recv(1024)
    data_str = str(data)[7:13]
    print('|' + data_str + '|')
    print(f"Температура {data!r}")
    
    s.close()
    quit(0)
    
    s.sendall(b'$KE,RD,ALL\r\n')
    data = s.recv(1024)
    print(f"Входные  линии {data!r}")
    
    s.sendall(b'$KE,RID,ALL\r\n')
    data = s.recv(1024)
    print(f"Выходные линии {data!r}")
    
    s.sendall(b'$KE,RDR,1\r\n')
    data = s.recv(1024)
    print(f"Реле 1 {data!r}")
    
    s.sendall(b'$KE,RDR,2\r\n')
    data = s.recv(1024)
    print(f"Реле 2 {data!r}")
    
    s.sendall(b'$KE,RDR,3\r\n')
    data = s.recv(1024)
    print(f"Реле 3 {data!r}")
    
    s.sendall(b'$KE,RDR,4\r\n')
    data = s.recv(1024)
    print(f"Реле 4 {data!r}")
    
    s.sendall(b'$KE,DAT,OFF\r\n')
    data = s.recv(1024)
    print(f"info= {data!r}")

s.close()

quit(0)

r = input('Для включения периодического считывания состояния введите любой символ=')
if len(r) == 0:
    quit(0)
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'$KE,DAT,ON\r\n')
    r = 0
    while r < 6:
        data = s.recv(1024)
        print(f"Статус = {data!r}")
        r += 1
    s.sendall(b'$KE,DAT,OFF\r\n')
    data = s.recv(1024)
    print(f"info= {data!r}")
    s.close()

# r = requests.get('http://192.168.10.101:2424', timeout=(2, 5))
# print(r)  $KE,RD,ALL