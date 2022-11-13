#!/usr/bin/env python3

import socket, os, signal

PORT = 50007

"""NOTA:
Los números de los comentarios (entre paréntesis) identifican distintos
ejercicios. Es necesario realizar los distintos ejercicios de uno en
uno, probando su correcto funcionamiento antes de pasar al siguiente.
"""

s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

s.bind( ('', PORT) )
s.listen( 5 )

"""A COMPLETAR POR EL/LA ESTUDIANTE:
(2) Evitar que procesos hijo queden como zombi.
Para ello habra que usar la funcion 'signal' para que trate
las señales tipo SIGCHLD.
"""

signal.signal(signal.SIGCHLD, signal.SIG_IGN)

while True:
	dialogo, dir_cli = s.accept()
	print( "Cliente conectado desde {}:{}.".format( dir_cli[0], dir_cli[1] ) )

	"""A COMPLETAR POR EL/LA ESTUDIANTE:
	(1) Crear un nuevo proceso que atienda al cliente recien conectado.
	Mientras, el proceso principal quedará a la espera de nuevas conexiones.
	"""
	
	
	while True:
		buf = dialogo.recv( 1024 )

		if not buf:
			break

		if c.fork():
			dialogo.close()
		else:
			s.close()
			dialogo.sendall(buf.encode())
			dialogo.close()
			exit(0)

		#dialogo.sendall( buf )
	print( "Solicitud de cierre de conexión recibida." )
	dialogo.close()
s.close()
