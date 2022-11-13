class Command:
	User, Password, List, Download, Download2,Upload, Upload2, Delete, Exit = ("USER", "PASS", "LIST", "DOWN", "DOW2", "UP", "UP2","DELE", "EXIT")

"""
Reads exactly one line of text (delimited by '\r\n') from the socket s and returns it.
Nos garantiza que va a ir leyendo hasta que haya un salto de linea.
"""
def recvline( s, removeEOL = True ):
	line = b''
	CRreceived = False
	while True:
		c = s.recv( 1 )
		if c == b'':
			raise EOFError( "Connection closed by the peer before receiving an EOL." )
		line += c
		if c == b'\r':
			CRreceived = True
		elif c == b'\n' and CRreceived:
			if removeEOL:
				return line[:-2]
			else:
				return line
		else:
			CRreceived = False

"""
Reads exactly size bytes from socket s and returns them.
Leer del socket, ya sea cliente o servidor, hasta que lleguemos hasta un determinado tamaño
"""
def recvall( s, size ):
	message = b''
	while( len( message ) < size ):
		chunk = s.recv( size - len( message ) )
		if chunk == b'':
			raise EOFError( "Connection closed by the peer before receiving the requested {} bytes.".format( size ) )
		message += chunk
	return message
