#!/usr/bin/env python3

import socket

PORT = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('localhost', PORT))

while True:
    mensaje, dir_cli = s.recvfrom(1024)
    print("Cliente \n Direccion cliente "+ dir_cli[0]+"\n Puerto "+ str(dir_cli[1]))
    s.sendto(mensaje.encode(), dir_cli)

s.close()

