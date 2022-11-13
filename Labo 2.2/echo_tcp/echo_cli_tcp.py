#!/usr/bin/env python3

import socket, sys

PORT = 50007

# Comprueba que se ha pasado un argumento.
if len( sys.argv ) != 2:
	print( "Uso: {} <servidor>".format( sys.argv[0] ) )
	exit( 1 )

"""A COMPLETAR POR EL/LA ESTUDIANTE:
Crear un socket y enviar peticion de conexion al servidor.
"""

dir_serv = (sys.argv[1], PORT)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((sys.argv[1],PORT))

print( "Introduce el mensaje que quieres enviar (mensaje vacío para terminar):" )
while True:

	mensaje = input()
	respuesta = ""
	
	if not mensaje:
		break
	"""A COMPLETAR POR EL/LA ESTUDIANTE:
	Enviar mensaje y recibir 'eco'.
	Mostrar en pantalla lo recibido.
	¡Cuidado! Recuerda que no hay garantías de recibir
	el mensaje completo en una única lectura.
	"""
	s.sendall(mensaje.encode())
	
	while True:
		buf= s.recv(1024)
		respuesta +=buf.decode()
		if respuesta == mensaje:
			break
	print(respuesta)

# print("Datos recibidos del servidor:", mensaje.decode())
s.close()
