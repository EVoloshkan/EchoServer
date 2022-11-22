import socket
import time


HOST = "127.0.0.1"
PORT = 40404
template_request = f"/?status=[code]\r\n\r\n"
while True:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.settimeout(1)
            code = input("Input http code:")
            requests = template_request.replace("[code]", code)
            sock.send(requests.encode("utf-8"))
            data = sock.recv(1024)
            print("Received:", data.decode("utf-8"))
    except Exception as ex:
        print(f"Exception: {ex}")
        time.sleep(1)
