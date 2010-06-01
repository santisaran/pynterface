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
import os
import Queue
try:
    import cPickle as pickle
except:
    import pickle
    
pids = []
f = open('config.txt','rw')
datos = pickle.load(f)
PORT = datos["PORT"]
TIMEOUT = 4
f.close()
class main():
    def __init__(self):
        self.ser = serial.Serial('/dev/ttyS3', 9600,timeout=3)  
        self.serdp = serial.Serial('/dev/ttyS2', 1200,timeout=5)
        global pids
        print self.ser.portstr
        print self.serdp.portstr 
        print "padre" + str(os.getpid())
    def comienzo(self):
        self.s = socket.socket()
        self.s.bind((get_ip_addr(), PORT))
        self.s.listen(1)
        self.lista = Queue.Queue()
        self.lstbal = Queue.Queue()
        while True:

            self.sc, self.addr = self.s.accept()
            self.sc.send("conexión iniciada\n")
            self.transmitter_thread = threading.Thread(target=self.writer)
            self.dp_thread = threading.Thread(target=self.dp)
            self.receiver_thread = threading.Thread(target=self.reader)
            self.enviar_thread = threading.Thread(target=self.enviar)
            self.temp_thread = threading.Thread(target=self.temperatura)
            self.balanza_thread = threading.Thread(target=self.balserie)
            self.alive = True
            self.receiver_thread.start()
            self.dp_thread.start()
            self.transmitter_thread.start()
            self.enviar_thread.start()
            self.temp_thread.start()
            self.balanza_thread.start()
            self.receiver_thread.join()
            self.alive = False
            print "volviendo a escuchar"
        print "funcionando"

    def balserie(self):
         """thread encargado de enviar datos a la balanza"""
         while self.alive:
            try:
                datos = self.lstbal.get(timeout=2)    
            except:
                continue
            else:
                self.ser.write(datos)
                sys.stdout.write(datos)
                sys.stdout.flush()
        
    def enviar(self):
        """thread encargado de enviar datos por el socket"""
        while self.alive:
            try:
                self.obj = self.lista.get(timeout=2)
            except:
                continue
            else:
                try:
                    self.sc.send(self.obj)
                except:
                    self.alive = False
                    print "error escribiendo socket"
                    self.sc.close()
                    break

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
                #se usa este bloqueo por que hay mas de un thread que necesitan
                #conexión con el socket
                self.lista.put(line)
                #dato enviado al thread "self.enviar"
                line = ""
            #~ else:
                #~ print "serial timeout"
        print "reader muerto"
    
    def dp(self):
        """thread que lee la información del sensor de humedad 
        y envía un promedio de los últimos 8 valores por el socket abierto
        por la clase padre"""
        dwpt = [9.5,9.5,9.5,9.5,9.5,9.5,9.5,9.5,9.5] #Carga inicial
        longitud = len(dwpt)
        timeout = False
        self.serdp.flushInput() #Limpiar lecturas anteriores.
        i = 0                   #
        while self.alive:
            try:
                line = self.serdp.readline()
            except :
                print "error lectura en el puerto serie DewPoint"
                continue
            timeout = True if (line == "") else False
            if not timeout:
                sys.stdout.write(line)
                sys.stdout.flush()
                if line[0:9] == "DP  C   =":
                    dwpt.pop(0)
                    dwpt.insert(8,line[9:19])
                    if i >= 2:          #enviar promedio cada 3 lecturas.
                        promedio = 0.0
                        for item in dwpt:
                            promedio += float(item)
                        promedio = promedio/longitud
                        #enviar promedio mediante lista, notificando al thread enviar
                        self.lista.put("DP C " + str(round(promedio,4)))
                        i = 0
                    else:
                        i+=1
            else:
                print "DP timeout"
                line = ""
        print "DP reader muerto"
    
    def temperatura(self):
        """Thread encargado de consultar la temperatura a la balanza,
         cada 10 segundos""" 
        while self.alive:
            self.lstbal.put("M28\r\n")
            time.sleep(10)
        
    def writer(self):
        """recibe comandos por el socket conectado a la interface de usuario
        y las envía a la balanza"""
        self.sindatos = 0
        self.sc.settimeout(TIMEOUT)
        a=0
        while self.alive:
            try:
                datos = self.sc.recv(32)
            except socket.timeout:
                a+=1
                if a == 4:
                #si a llega a 4 la conexión se da por caída
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
                    #si los datos recibidos no son "quit" ni "YESILIVE" envía
                    #los mismos por el puerto serie a la balanza
                    print "encolando " + datos
                    self.lstbal.put(datos)
                    print "enviado a la lista" + datos
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
        


