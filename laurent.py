import requests
# echo-server.py

import socket

HOST = "192.168.10.101"  # Standard loopback interface address (localhost)
PORT = 2424  # Port to listen on (non-privileged ports are > 1023)

chunk = b'$KE,TMP\r\n'
print(chunk, end='<')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    s.sendall(chunk)
    data = s.recv(1024)

print(f"Received {data!r}")

            
# r = requests.get('http://192.168.10.161:2424', timeout=(2, 5))
# print(r)