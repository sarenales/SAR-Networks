#!/usr/bin/env python3

import socket, sys

# Mirar servidor DNS en fichero "/etc/resolv.conf"
DNS_DIR = "127.0.0.53"
DNS_PORT = 53

# Obtiene un nombre DNS de 'buf' a partir de la posición 'pos_ini'
# según formato DNS (RFC 1035), incluida la compresión de nombres.
# Devuelve el número de bytes que ocupa en buf y el nombre DNS en notación de puntos
def obten_nombre_dns( buf, pos_ini ):
	pos = pos_ini
	qname = ''
	tam_label = buf[pos]
	while tam_label > 0:
		w16bit = bin(int.from_bytes(buf[pos:pos+2], 'big'))[2:].zfill(16)
		if w16bit[0:2] == '11': # if Message compression
			# # OFFSET
			pos += 2
			offset = int(w16bit[2:], 2)
			_, name = obten_nombre_dns(buf, offset)
			return pos - pos_ini, qname + name
		else:
			pos += 1
			qname += buf[pos:pos+tam_label].decode()
			pos += tam_label
			tam_label = buf[pos]
			if tam_label > 0:
				qname += '.'
	pos += 1
	return pos - pos_ini, qname

# Programa principal
if __name__ == "__main__":
	if len( sys.argv ) != 2:
		print( "Uso: python3 {} <Nombre DNS de máquina>".format( sys.argv[0] ) )
		exit( 1 )

	nombre_dns = sys.argv[1]

	serv_dns = (DNS_DIR, DNS_PORT)

	s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )

	# Preparar pregunta DNS
	buf = b''
	# Header section
	# # ID
	ID = (1234).to_bytes(2, 'big') # 1234 podría ser cualquier valor
	buf += ID
	# # Flags
	flags = (0x0100).to_bytes(2, 'big')
	buf += flags
	# # QDCOUNT
	qdcount = (1).to_bytes(2, 'big')
	buf += qdcount
	# # ANCOUNT
	zero = (0).to_bytes(2, 'big')
	buf += zero
	# # NSCOUNT
	buf += zero
	# # ARCOUNT
	buf += zero
	# Question section
	# # QNAME
	for label in nombre_dns.split("."):
		tam_label = (len(label)).to_bytes(1, 'big')
		buf += tam_label
		buf += label.encode()
	tam_label = (0).to_bytes(1, 'big')
	buf += tam_label
	# # QTYPE. type = A
	one = (1).to_bytes(2, 'big')
	buf += one
	# # QCLASS. class = IN
	buf += one
	# -- Pregunta DNS completa --
	#print( "Pregunta DNS a enviar:\r\n", buf )
	# Enviar pregunta DNS
	s.sendto( buf, serv_dns )
	# Recibir respuesta
	buf = s.recv( 1024 )
	#print( "Respuesta recibida:\r\n", buf )
	# Intrepretar respuesta
	# Header section
	# # ID
	pos = 0
	ID_respuesta = buf[pos:pos+2]
	if ID != ID_respuesta:
		print( "El identificador de la respuesta DNS recibida ({}) NO coincide con el enviado ({}).".format( ID_respuesta, ID ) )
		exit( 1 )
	pos += 2
	# # Flags: |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
	# #        +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
	flags = bin(int.from_bytes(buf[pos:pos+2], 'big'))[2:].zfill(16)
	if not flags[0]: # bit QR != 1
		print( "El bit QR de la respuesta DNS recibida no se corresponde con el de una respuesta DNS(1)." )
		exit( 1 )
	RCODE = int(flags[-4:], 2)
	if RCODE != 0:
		msg_err = "Respuesta con código de error {}: ".format( RCODE )
		if RCODE == 1:
			msg_err += "Format error!"
		elif RCODE == 2:
			msg_err += "Server failure!"
		elif RCODE == 3:
			msg_err += "Name Error!"
		elif RCODE == 4:
			msg_err += "Not implemented!"
		elif RCODE == 5:
			msg_err += "Refused!"
		else:
			msg_err += "Error desconocido!"
		print( msg_err )
		exit( 1 )
	pos += 2
	# # QDCOUNT
	qdcount = int.from_bytes(buf[pos:pos+2], 'big')
	pos += 2
	# # ANCOUNT
	ancount = int.from_bytes(buf[pos:pos+2], 'big')
	pos += 2
	# # NSCOUNT
	nscount = int.from_bytes(buf[pos:pos+2], 'big')
	pos += 2
	# # ARCOUNT
	arcount = int.from_bytes(buf[pos:pos+2], 'big')
	pos += 2
	# Question section
	if qdcount:
		# # QNAME
		desp, qname = obten_nombre_dns(buf, pos)
		pos += desp
		# # QTYPE
		pos += 2
		# # QCLASS
		pos += 2
	# Answer section: 4.1.3. Resource record format
	if not ancount:
		print( 'No se ha recibido ningún registro en la sección de respuestas!' )
	else:
		# # NAME
		desp, name = obten_nombre_dns(buf, pos)
		pos += desp
		# # TYPE
		antype = int.from_bytes(buf[pos:pos+2], 'big')
		pos += 2
		# # CLASS
		anclass = int.from_bytes(buf[pos:pos+2], 'big')
		pos += 2
		# # TTL: a 32 bit unsigned integer
		pos += 4
		# # RDLENGTH: an unsigned 16 bit integer
		rdlength = int.from_bytes(buf[pos:pos+2], 'big', signed=False)
		pos += 2
		# # RDATA
		if rdlength:
			if antype == 1 and anclass == 1: # if the TYPE is A and the CLASS is IN
				dir_IP = socket.inet_ntoa(buf[pos:pos+4])
				print( "Dirección IP:", dir_IP )
			else:
				print("Type:", antype)
				print( "RDATA:", buf[pos:pos+rdlength] )
			pos += rdlength
	# Authority section: 4.1.3. Resource record format
	# Additional section: 4.1.3. Resource record format
	s.close()
