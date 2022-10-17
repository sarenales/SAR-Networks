#!/usr/bin/env python3

import socket

PORT = 50007

s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

s.bind( ('', PORT) )

while True:
	buf, dir_cli = s.recvfrom( 1024 )
	s.sendto( buf, dir_cli)
s.close()

