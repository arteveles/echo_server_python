import os
import socket
from http import HTTPStatus

HOST = "127.0.0.1"
PORT = 11869

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Сервер стартанул на {HOST}:{PORT}, id процесса: {os.getpid()}")
    s.bind((HOST, PORT))
    s.listen(1)

    while True:
        print("Ожидание запроса клиента.")
        conn, address = s.accept()
        print("Подключение от", address)

        data = conn.recv(1024)
        print(f"Полученные данные: \n{data}\n")
        data = data.decode("utf-8").strip()

        status_value = 200
        status_phrase = "OK"
        try:
            status = data.split()[1].split("/?status=")
            if len(status) == 2:
                status_code = int(status[1].split()[0])
                stat = HTTPStatus(status_code)
                status_value = status_code
                status_phrase = stat.phrase
        except (ValueError, IndexError):
            pass

        status_line = f"{data.split()[2]} {status_value} {status_phrase}"
        resp = "\r\n".join(data.split("\r\n")[1:])

        conn.send(f"{status_line}\r\n\r\n"
                  f"\nRequest method: {data.split()[0]}"
                  f"\nRequest source: {address}"
                  f"\nResponse status: {status_value} {status_phrase} \r\n"
                  f"\n{resp}".encode("utf-8")
                  )
        conn.close()
