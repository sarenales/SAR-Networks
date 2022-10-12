#!/usr/bin/env python3

import socket, sys

PORT = 50007

# Comprueba que se ha pasado un argumento.
if len( sys.argv ) != 2:
	print( "Uso: {} <servidor>".format( sys.argv[0] ) )
	exit( 1 )

"""A COMPLETAR POR EL/LA ESTUDIANTE:
Crear el socket.
"""

print( "Introduce el mensaje que quieres enviar (mensaje vacío para terminar):" )
while True:
	mensaje = input()
	if not mensaje:
		break
	"""A COMPLETAR POR EL/LA ESTUDIANTE:
	Enviar mensaje y recibir 'eco'.
	Mostrar en pantalla lo recibido.
	"""
"""A COMPLETAR POR EL/LA ESTUDIANTE:
Cerrar socket.
"""
