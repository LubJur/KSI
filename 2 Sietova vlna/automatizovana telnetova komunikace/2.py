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
    hostname, port = sys.argv[1], int(sys.argv[2])

    with Telnet(hostname, port) as tn:
        while True:
            try:
                data = tn.read_until(b"\n")
                #print(data)
                data = data.decode().split()
                #print(data)
                if data[0].startswith("KSI"):
                    print(data[0])
                    return
                else:
                    a = int(data[2])
                    b = int(data[4][:-1])
                    send = f"{a + b}"
                    tn.write(bytes(send, "utf-8"))
            except EOFError:
                pass
                #print(tn.read_all().decode())
        #print(tn.read_until(b"\n"))


if __name__ == '__main__':
    main()