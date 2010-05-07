#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       conexion.py
#       
#       Copyright 2010 Santiago <santiagopaleka@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
# 
#   Este programa se encarga de recibir datos desde el puerto serie y 
#   Enviarlos a una conexión socket
#   Cada TIMEOUT envía una señal preguntando si el cliente sigue con vida
#   ("life") si este responde "YESILIVE" continúa, sino se cierra esa conexión
#   y se vuelven a escuchar nuevas conexiones.


import serial
import sys
import threading
import time
import socket
try:
    import cPickle as pickle
except:
    import pickle
    
f = open('config.txt','rw')
datos = pickle.load(f)
PORT = datos["PORT"]
TIMEOUT = 4
f.close()
class main():
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS3', 9600,timeout=3)  # open first serial port
        print self.ser.portstr   # check which port was really used 
    def comienzo(self):
        self.s = socket.socket()
        self.s.bind((get_ip_addr(), PORT))
        self.s.listen(1)
        while True:
            self.alive = True
            self.sc, self.addr = self.s.accept()
            self.sc.send("conexión iniciada\n")
            self.transmitter_thread = threading.Thread(target=self.writer)
            self.receiver_thread = threading.Thread(target=self.reader)
            self.receiver_thread.start()
            self.transmitter_thread.start()
            self.receiver_thread.join()
            print "volviendo a escuchar"
        print "funcionando"

    def reader(self):
        timeout = False
        self.ser.flushInput()
        while self.alive:
            try:
                line = self.ser.readline()
            except :
                print "error lectura en el puerto serie"
                self.alive = False
                continue
            timeout = True if (line == "") else False
            #~ print str(timeout)
            if not timeout:
                #~ print "notimeout"
                sys.stdout.write(line)
                sys.stdout.flush()
                self.sindatos = 0
                try:
                    self.sc.send(line)
                except:
                    self.alive = False
                    print "error escribiendo socket"
                    self.sc.close()
                    break
                line = ""
            #~ else:
                #~ print "serial timeout"
        print "reader muerto"
        
    def writer(self):
        self.sindatos = 0
        self.sc.settimeout(TIMEOUT)
        a=0
        while self.alive:
            try:
                datos = self.sc.recv(32)
            except socket.timeout:
                a+=1
                print a
                if a == 4:
                    self.alive = False
                try:
                    self.sc.send("life")
                except:
                    self.alive = False
                    continue
                continue
            except socket.error, msg:
                print msg
                self.alive = False
                break
            if datos != "":
                a=0
                if (datos[0:4] == "quit")|(datos[0:4] == "QUIT")|(datos[0:4] == "Quit"):
                    self.alive = False
                    self.sc.close()
                    print "conexión cerrada"
                    break
                if datos[0:8] != "YESILIVE":
                    self.ser.write(datos)
                    sys.stdout.write(datos)
                    sys.stdout.flush()
        print "writer muerto"
        try:
            self.sc.close()    
        except:
            pass
            
def get_ip_addr(connection_ip='10.10.10.156'):
    """Returns the ip address of the interface used to connect to the given ip
    10.10.10.156 is a DNS ROOT Server, so it's the default value to
    connect to Internet
    """
    so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    so.connect((connection_ip, 0))
    inet_address = so.getsockname()[0]
    so.close()
    return inet_address
    

if __name__ == '__main__':
    principal = main()
    try:
        principal.comienzo()
    except KeyboardInterrupt:
        principal.s.close()
        try:
            principal.sc.close()
        except:
            pass
        print "terminado por ^C"
        exit()
        


