import datetime
import re
import socket
from http import HTTPStatus


http_response = (
    f"HTTP/1.0 [status]\r\n"
    f"Server: my_srv\r\n"
    f"Date: [date]\r\n"
    f"Content-Type: text/html; charset=UTF-8\r\n"
    f"\r\n"
)
end_of_stream = '\r\n\r\n'


def handle_client(connection):
    client_data = ''
    with connection:
        while True:
            data = connection.recv(1024)
            if not data:
                break
            client_data += data.decode()
            if end_of_stream in client_data:
                break

        print("Received:", client_data.strip(), sep="\r\n")

        code = re.search(r"\d+|$", client_data).group()
        try:
            status_code = HTTPStatus(int(code))
        except ValueError:
            status_code = HTTPStatus.OK

        date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        connection.send(http_response.replace("[date]", date)
                        .replace("[status]", f"{status_code.value} {status_code.phrase}").encode()
                        + f"<H3>{status_code.value} {status_code.phrase}</H3>\r\n".encode()
                        + client_data.replace('\r\n', '<br>').encode()
                        + f"\r\n".encode())


with socket.socket() as serverSocket:
    serverSocket.bind(("127.0.0.1", 40404))
    serverSocket.listen(10)

    while True:
        (clientConnection, clientAddress) = serverSocket.accept()
        handle_client(clientConnection)
        print(f"Sent data to {clientAddress}")
