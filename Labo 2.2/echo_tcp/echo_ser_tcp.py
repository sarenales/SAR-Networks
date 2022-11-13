#!/usr/bin/env python3

import socket

PORT = 50007

"""A COMPLETAR POR EL/LA ESTUDIANTE:
Crear un socket, asignarle su dirección y
convertirlo en socket de escucha.
"""
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('', PORT))
s.listen(5)

while True:
	"""A COMPLETAR POR EL/LA ESTUDIANTE:
	Aceptar peticion de conexion.
	Mientras el cliente no cierre la conexion,
	recibir un mensaje y responder con el mismo.
	Cerrar conexión.
	"""

	diagolo, _ = s.accept()
	
	while True:
		mensaje = diagolo.recv(1024)
		if not mensaje:
			diagolo.close()
		else:
			diagolo.sendall(mensaje.encode())
	


"""A COMPLETAR POR EL/LA ESTUDIANTE:
Cerrar socket de escucha.
"""

s.close()

