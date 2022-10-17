#!/usr/bin/env python3

import socket, sys

PORT = 50007

if len( sys.argv ) != 2:
	print( "Uso: {} <servidor>".format( sys.argv[0] ) )
	exit( 1 )

dir_serv = (sys.argv[1], PORT)

s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

print( "Introduce el mensaje que quieres enviar (mensaje vacío para terminar):" )
while True:
	mensaje = input()
	if not mensaje:
		break
	s.sendto( mensaje.encode(), dir_serv )
	buf = s.recv( len(mensaje.encode()) )
	print( buf.decode() )
s.close()
