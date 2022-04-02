#!/usr/bin/env python3
import socket
import sys

def main():
    hostname, port = sys.argv[1], int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((hostname, port))
        s.sendall(b'HELLO')
        data = s.recv(1024)
        print(data)
        #print(data.decode())
    data = data.decode()
    data = data.split()
    print(data)
    a = int(data[2])
    b = int(data[4])
    print(a + b)
    #print(data.decode().rstrip())


if __name__ == '__main__':
    main()