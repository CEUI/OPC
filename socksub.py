#!/user/bin/env python3

import socket
import binascii

from opcua import Server
from opcua import ua
from opcua import Client
from random import randint
import datetime
import time


HOST = '127.0.0.1'
PORT = 12345

#OPC UA Connection
url = "opc.tcp://10.0.0.99:8899/freeopcua/server/"
client = Client(url)
client.connect()

val1 = client.get_node("ns=2;i=3")
val2 = client.get_node("ns=2;i=4")
val3 = client.get_node("ns=2;i=5")
val4 = client.get_node("ns=2;i=6")
val5 = client.get_node("ns=2;i=7")
val6 = client.get_node("ns=2;i=8")
val7 = client.get_node("ns=2;i=9")
val8 = client.get_node("ns=2;i=10")
val9 = client.get_node("ns=2;i=11")
val10 = client.get_node("ns=2;i=12")
val11 = client.get_node("ns=2;i=13")
val12 = client.get_node("ns=2;i=14")
val13 = client.get_node("ns=2;i=15")
val14 = client.get_node("ns=2;i=16")
	
value1 = val1.get_value()
value2 = val2.get_value()
value3 = val3.get_value()
value4 = val4.get_value()
value5 = val5.get_value()
value6 = val6.get_value()
value7 = val7.get_value()
value8 = val8.get_value()
value9 = val9.get_value()
value10 = val10.get_value()
value11 = val11.get_value()
value12 = val12.get_value()
value13 = val13.get_value()
value14 = val14.get_value()



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind(('',PORT))
	s.listen()
	conn, addr = s.accept()
	with conn:
		print('Connection from:',addr)
		while True:

			#Receive data from client
			data = conn.recv(1024)

			if not data:
				break

			stringd = data.decode('utf-8')

			#convert string to integer
			intd = int(stringd)

			
			if (intd == 0):
				print("Entry: 0")
				print(value11)
				print("Set value")
				val11.set_value(0, ua.VariantType.Int16)
				value11 = val11.get_value()
				print(value11)
			elif (intd == 1):
				print("Entry: 1")
				print(value11)
				print("Set value")
				val11.set_value(1, ua.VariantType.Int16)
				value11 = val11.get_value()
				print(value11)
			else:
				print("++++++++++++++++++++++")
				print("Line 01-02 I Res: "+str(value2))
				print("Line 01-02 V Res: "+str(value5))
				print("Line 01-02 f Res: "+str(value6))
				print("Line 01-39 I Res: "+str(value7))
				print("======================"+"\n")


			
			time.sleep(2)

			#covert inetger to string
			value2 = val2.get_value()
			stringd = str(value2)

			#convert string to bytes data
			data = stringd.encode()

			#send data back to client
			conn.sendall(data)

			print('send to CC:',data)

client.disconnect()
