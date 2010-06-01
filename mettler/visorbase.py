#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       visorbase.py
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

try:
    import cPickle as pickle
except:
    import pickle
import wx
from wx import xrc
import gestionbbdd as gesbbdd

archivo = file("config.txt", 'r')        #archivo donde se encuentran las
datos = pickle.load(archivo)            #configuraciones iniciales.
BASEDEDATOS = datos['BASEDATOS']        #Nombre de la base de datos
dic = datos['dic']              # estructura de diccionario para la base
llaves = datos['llaves']        # columnas de la base de datos (ordenadas).
archivo.close()

class mimain(wx.App):
    def OnInit(self):
        self.seleccionados = [] #items seleccionados de la lista E
        self.Tareas = []        #lista de diccionarios cada uno con
                                #los valores de una tarea distinta.
        self.widecols = (130,100,wx.LIST_AUTOSIZE_USEHEADER,wx.LIST_AUTOSIZE_USEHEADER,120,130)
        self.gesbbdd = gesbbdd.gestion(BASEDEDATOS)
        self.res = xrc.XmlResource('visbase.xrc')
        self.visorbase = self.res.LoadFrame(None,'FrameBase')
        hora = time.strftime("%Y%m%d%H%M%S",time.localtime())
        self.filas = self.gesbbdd.Consultar("N","terminado")
        
        self.visorbase.Show()
        
        return True
        
if __name__ == '__main__':
    Aplicacion = mimain(0)
    Aplicacion.MainLoop()
    
