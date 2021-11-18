#!/usr/bin/env python3
"""
import socket
import sys

def main():
    hostname, port = sys.argv[1], int(sys.argv[2])

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((hostname, port))
            data = s.recv(1024)
            data = data.decode()
            data = data.split()
            a = int(data[2])
            b = int(data[4][0])
            send = f"{a+b}"
            s.sendall(bytes(send, "utf-8"))
            s.flush()

        print(data)
    print(a + b)
    #print(data.decode().rstrip())

"""
from telnetlib import Telnet
import sys

def main():
    #hostname, port = sys.argv[1], int(sys.argv[2])


    with Telnet(hostname, port) as tn:
        while True:
            try:
                data = tn.read_until(b"\n")
                data = data.decode()
                if data.startswith("KSI"):
                    data = data[:-1]
                    data = data.split("\x1b")
                    password = list(data[0])
                    password = password[4:]
                    pointer = len(password) - 1
                    for i in data[1:]:
                        if i[-1] != "*":
                            if len(i) == 4:
                                if i[2] == "D":
                                    pointer -= int(i[1])
                                if i[2] == "C":
                                    pointer += int(i[1])
                                pointer += 1
                                print(pointer)
                            elif len(i) == 5:
                                if i[3] == "D":
                                    pointer -= int(i[1:3])
                                if i[3] == "C":
                                    pointer += int(i[1:3])
                                pointer += 1
                                print(pointer)
                            try:
                                password[pointer] = i[-1]
                            except IndexError:
                                pass

            except EOFError:
                password = "".join(password)
                print("KSI{"+password+"}")
                return


if __name__ == '__main__':
    main()