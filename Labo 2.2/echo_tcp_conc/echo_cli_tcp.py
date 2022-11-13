#!/usr/bin/env python3

import socket, sys

PORT = 50007

if len( sys.argv ) != 2:
	print( "Uso: {} <servidor>".format( sys.argv[0] ) )
	exit( 1 )

dir_serv = (sys.argv[1], PORT)

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
s.connect( dir_serv )

print( "Introduce el mensaje que quieres enviar (mensaje vacío para terminar):" )
while True:
	mensaje = input()
	if not mensaje:
		break
	s.sendall( mensaje.encode() )
	# Es necesario un blucle porque no hay garantías de que la respuesta
	# completa se reciba en una única lectura.
	bytes_por_leer = len( mensaje.encode() )
	mensaje = b""
	while bytes_por_leer:
		buf = s.recv( bytes_por_leer )
		mensaje += buf
		bytes_por_leer -= len( buf )
	print( mensaje.decode() )
s.close()
