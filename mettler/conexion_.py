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

import threading
import socket
import sys
import wx
try:
    import cPickle as pickle
except:
    import pickle

archivo = file("config.txt",'r')
datos = pickle.load(archivo)
BALANZA = datos['IP_BALANZA']
PORT = datos["PORT"]
archivo.close()

class ThreadLector(threading.Thread):
    """
    This just simulates some long-running task that periodically sends
    a message to the GUI thread.
    """
    def __init__(self, threadNum, window, conector):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.window = window
        self.conector = conector

    def stop(self):
        self.window.s.close()
    
    def run(self):  
        mensaje = ""
        self.conector.s.settimeout(1)
        while self.window.alive:
            try:
                mensaje = self.conector.s.recv(1024)
            except socket.timeout:
                continue
            if mensaje != "":
                if mensaje == "life":
                    self.conector.writer("YESILIVE")
                else:
                    #~ mensaje = mensaje[:-4] + "\n"
                    wx.CallAfter(self.window.SalidaText.Clear)
                    wx.CallAfter(self.window.SalidaText.AppendText,mensaje[:-2])

        print "conexión cerrada"

class conector:
    def __init__(self,window):
        self.window = window
        self.s = socket.socket()
        print BALANZA + ":" + str(PORT)
        try:
            self.s.connect((BALANZA, PORT))
        except:
            print "no se pudo abrir Conexión con " + BALANZA + ":" + str(PORT) 
            self.window.btnCom.SetValue(False)
            return
        print "conectado"
        self.window.conectado = True
        self.count = 1
        self.thread = ThreadLector(self.count, self.window, self)
        self.thread.start()


    def writer(self, code): 
        if code[0:4] == "quit":
            print "CerrandoSocket"
            self.s.send("quit")
            self.s.close()
            return
        c = code + "\r\n"
        self.s.send(c)
 
    def Close(self):
        self.window.alive = False
        self.s.send("quit")
        self.s.close()
