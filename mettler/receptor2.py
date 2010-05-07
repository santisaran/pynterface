# -*- coding: utf-8 -*-
import threading
import socket
import sys
BALANZA = "10.10.8.76"
PORT = 9999

class main():
	def __init__(self):
		self.s = socket.socket()
		print BALANZA + ":" + str(PORT)
		try:
			self.s.connect((BALANZA, PORT))
		except:
			print "no se pudo abrir Conexión con " + BALANZA + ":" + str(PORT) 
			exit(1)
		self.receiver_thread = threading.Thread(target=self.reader)
		self.receiver_thread.setDaemon(1)
		self.receiver_thread.start()
		self.receiver_thread.join()
		# enter console->serial loop
		self.transmitter_thread = threading.Thread(target=self.writer)
		#self.transmitter_thread.setDaemon(1)
		self.transmitter_thread.start()
	def reader(self):
		while True:
			try:
				mensaje = self.s.recv(1024)
			except:
				print "broken Pipe2"
				break
			sys.stdout.write(mensaje)
			sys.stdout.flush()
	def writer(self):
		while True:
			c=input()
			print "pasa esto"
			try:
				self.s.send(c)
			except:
				print "broken pipe"
				break
if __name__ == '__main__':
    main()
