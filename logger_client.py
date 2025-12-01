import socket
import select
from buffer import *

buffer_instance = Buffer(20000)
HOST = "127.0.0.1"
PORT = 22999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    socket_read = [s]

    while True:
        try:
            ready_read, _, _ = select.select(socket_read, [], [], 0.1)
        except:
            s.close()

        for ready in ready_read:
            if ready == s:
                data = ready.recv(10000)
                if data:
                    data = data.decode()
                    buffer_instance.add_frame(data)

                    while data != "":
                        data = buffer_instance.extract_frame()
                        if data != "":
                            print(data)
