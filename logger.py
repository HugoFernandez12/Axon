import socket
import select
import time
from buffer import *
from datetime import datetime
import threading
import os.path

lock = threading.RLock()
buffer_instance = Buffer(20000)


class Logger:
    def __init__(self, port, debug_level, retention_days):
        self.port = port
        self.debug_level = debug_level
        self.retention_days = retention_days
        self.connection = ""
        self.start_server()

    def send_socket(self):
        HOST = "127.0.0.1"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, self.port))
        s.listen()

        while True:
            socket_list = [s]
            ready_to_read, ready_to_write, in_error = select.select(socket_list, socket_list, [], 0.1)

            if len(ready_to_read) != 0:
                for sock in ready_to_read:
                    if sock is s:
                        conn, addr = s.accept()
                        print("addr", addr)
                        print(f"Connected by {addr}")
                        self.connection = conn

    def log(self, level, text):
        with lock:
            timestamp = datetime.now().strftime("%Y%m%d %H%M%S.%f")[:-3]

            if int(level) <= int(self.debug_level):
                if type(self.connection) is socket.socket:
                    try:
                        self.connection.sendall(
                            buffer_instance.create_frame(timestamp + " " + level + " " + text).encode())
                    except:
                        self.connection.close()
                        self.connection = ""

                log_path = "logs/logs_" + str(datetime.now().strftime("%Y%m%d")) + ".log"

                if os.path.isfile(log_path):
                    f = open(log_path, "a")
                    f.write(timestamp + " " + level + " " + text + "\n")
                    self.cleanup_old_logs()
                else:
                    open(log_path, "x")
                    f = open(log_path, "a")
                    f.write(timestamp + " " + level + " " + text + "\n")
                    self.cleanup_old_logs()

                print(timestamp + " " + level + " " + text)

    def fatal(self, text):
        self.log("1", text)

    def critical(self, text):
        self.log("2", text)

    def error(self, text):
        self.log("3", text)

    def warning(self, text):
        self.log("4", text)

    def notice(self, text):
        self.log("5", text)

    def information(self, text):
        self.log("6", text)

    def trace(self, text):
        self.log("7", text)

    @staticmethod
    def is_leap_year():
        year = int(datetime.now().year)
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def calculate_deletion_date(self):
        control = int(datetime.now().day) - self.retention_days

        if control <= 0:
            if control == 0:
                days_to_subtract = 0
            else:
                for x in range(1, 32):
                    if control + x == 0:
                        days_to_subtract = x
                        break

            month_to_check = int(datetime.now().month) - 1

            if month_to_check == 0:
                month_to_check = 12

            if int(month_to_check) in [1, 3, 5, 7, 8, 10, 12]:
                days_to_subtract = 31 - days_to_subtract
            elif int(month_to_check) in [4, 6, 9, 11]:
                days_to_subtract = 30 - days_to_subtract
            elif int(month_to_check) == 2:
                if self.is_leap_year():
                    days_to_subtract = 29 - days_to_subtract
                else:
                    days_to_subtract = 28 - days_to_subtract

            month_control = int(datetime.now().strftime("%m")) - 1
            days = str(days_to_subtract)

            if month_control == 0:
                year_control = int(datetime.now().strftime("%Y")) - 1
                deletion_date = str(year_control) + "12" + days
                return deletion_date
            else:
                if len(str(month_control)) == 1:
                    month_control = "0" + str(month_control)
                deletion_date = str(datetime.now().strftime("%Y")) + str(month_control) + days
                return deletion_date
        else:
            if len(str(control)) == 1:
                control = "0" + str(control)
            deletion_date = str(datetime.now().strftime("%Y%m")) + str(control)
            return deletion_date

    def cleanup_old_logs(self):
        folder = "logs"
        deletion_date = self.calculate_deletion_date()

        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)

            if os.path.isfile(file_path):
                file_mod_time = os.path.getctime(file_path)
                file_mod_date = datetime.fromtimestamp(file_mod_time)
                file_mod_date = file_mod_date.strftime("%Y%m%d")

                if deletion_date > file_mod_date:
                    if os.path.isfile(file_path):
                        os.remove(file_path)

                if int(deletion_date) > int(file[5:13]):
                    if os.path.isfile(file_path):
                        os.remove(file_path)

    def start_server(self):
        threading.Thread(target=self.send_socket).start()
