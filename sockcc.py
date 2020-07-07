#!/user/bin/env python3

import socket
import binascii

HOST = '127.0.0.1'
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))

	#ask input
	value=input()
	valbytes=value.encode()

	#send data to server
	s.sendall(valbytes)

	#recive data from server
	data = s.recv(1024)

print('Data:',data)