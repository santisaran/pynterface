#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       shyshy3.py
#      
#       Copyright 2010 Santiago <saran@Santi>
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
import threading
import socket
import sys
import time
from wx import xrc

import gestionbbdd as gesbbdd
#~ import conexion


#Cargar configuración desde config.txt---------------------------------#
archivo = file("config.txt", 'r')        #archivo donde se encuentran las
datos = pickle.load(archivo)            #configuraciones iniciales.
BASEDEDATOS = datos['BASEDATOS']        #Nombre de la base de datos
VASOS = datos['IDVASOS']        # Items de vasos disponibles
BALANZA = datos['IP_BALANZA']   # Ip de la pc que tiene la balanza en su puerto serie
dic = datos['dic']              # estructura de diccionario para la base
llaves = datos['llaves']        # columnas de la base de datos (ordenadas).
PORT = datos["PORT"]
archivo.close()
VERSION = "0.0.1"
OK = "K C 7"
UP = "K C 9"
DOWN = "K C 8"
NO = "K C 6"
CERO = "K C 5"
OPENLEFT = "K C 10"
OPENRIGTH = "K C 11"
#----------------------------------------------------------------------#

EVT_NEW_DATA_ID = wx.NewId()

def EVT_RESULT(win, func):
    win.Connect(-1, -1, EVT_NEW_DATA_ID, func)


class AcquireEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_NEW_DATA_ID)
        self.data = data


class mimain(wx.App):
    def OnInit(self):
        self.seleccionados = [] #items seleccionados de la lista E
        self.diagCselected = [] #items seleccionados de la lista C
        self.Tareas = []        #lista de diccionarios cada uno con
                                #los valores de una tarea distinta.
        self.widecols = (130,100,wx.LIST_AUTOSIZE_USEHEADER,wx.LIST_AUTOSIZE_USEHEADER,120,130)
        self.valuecols = ("Vin","Modelo","IdVasos","Rep","Usuario","fecha y hora")
        self.gesbbdd = gesbbdd.gestion(BASEDEDATOS)
        self.res = xrc.XmlResource('meter.xrc')

       
        #--------------------------------------------------------------#
        #---------------Dialogo de carga de valores--------------------#
        #Widgets-------------------------------------------------------#
        
        self.diagcarga = self.res.LoadDialog(None, 'dialogoCarga')
        self.ctxtvinVehiculo = xrc.XRCCTRL(self.diagcarga, 'vinVehiculo')
        self.ctxtModelo = xrc.XRCCTRL(self.diagcarga, 'modelo')
        self.choicesRep = xrc.XRCCTRL(self.diagcarga, 'repeticiones')
        self.choiceVasos = xrc.XRCCTRL(self.diagcarga, 'vasos')
        self.comboUser = xrc.XRCCTRL(self.diagcarga, 'usuario')
        self.dlgCList = xrc.XRCCTRL(self.diagcarga, 'listaCargando')
        self.dlgEList = xrc.XRCCTRL(self.diagcarga, 'listaSinCompletar')

        #~ self.dlgCbtnEmp = xrc.XRCCTRL(self.diagcarga, 'btnEmpezar')
        #~ self.dlgCbtnBor = xrc.XRCCTRL(self.diagcarga, 'btnBorrar')
        
        #Handlers -----------------------------------------------------#
        
        self.diagcarga.Bind(wx.EVT_CLOSE,self.OnCloseDiagCarga)
        self.diagcarga.Bind(wx.EVT_BUTTON,self.OnCargar,id=xrc.XRCID('btnCargar'))
        self.diagcarga.Bind(wx.EVT_BUTTON,self.OnBorrarLista,id=xrc.XRCID('btnBorrar'))
        self.diagcarga.Bind(wx.EVT_BUTTON,self.OnBorrarSeleccion,id=xrc.XRCID('btnBorrarItem'))       
        self.diagcarga.Bind(wx.EVT_BUTTON,self.OnEmpezar,id=xrc.XRCID('btnEmpezar'))
        self.diagcarga.Bind(wx.EVT_BUTTON,self.OnContinuar,id=xrc.XRCID('btnContinuar'))       
        self.diagcarga.Bind(wx.EVT_BUTTON,self.OnMostrarBase,id=xrc.XRCID('btnACargado'))

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnEItemSelected, self.dlgEList)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnEItemDeselected, self.dlgEList)
 
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnCItemSelected, self.dlgCList)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnCItemDeselected, self.dlgCList)

        self.ctxtvinVehiculo.Bind(wx.EVT_SET_FOCUS, self.OnFocusVin)       
        
        #Valores iniciales---------------------------------------------#
        self.choiceVasos.SetItems(VASOS)
        for col, text in enumerate(self.valuecols):
            self.dlgCList.InsertColumn(col, text)
            self.dlgEList.InsertColumn(col, text)
        
        for anchos in enumerate(self.widecols):
            self.dlgCList.SetColumnWidth(anchos[0], anchos[1])
            self.dlgEList.SetColumnWidth(anchos[0], anchos[1])
            
        self.NoTerminadas = self.gesbbdd.Consultar("N","terminado")
        for listadedic in self.NoTerminadas:
            self.CargarEnLista(self.dlgEList,listadedic)
        #--------------------------------------------------------------#
        #--------------------------------------------------------------#
        #--------------------------------------------------------------#
        
        self.diagcarga.Show()
        
        #--------------------------------------------------------------#
        #-----------------------Vista de Base de datos-----------------#
        #--------------------------------------------------------------#
        
        self.vistabase = self.res.LoadFrame(None,'FrameBase')
        
        #Handlers------------------------------------------------------#
        
        self.vistabase.Bind(wx.EVT_BUTTON,self.OnCargarSelec,id=xrc.XRCID('btnCargaSel'))    
        self.vistabase.Bind(wx.EVT_BUTTON,self.OnFecha,id=xrc.XRCID('btnfecha'))
        self.vistabase.Bind(wx.EVT_CLOSE, self.OnCloseVistaBase)
        self.vistabase.txFIni = xrc.XRCCTRL(self.vistabase, '')
        self.vistabase.txFFin = xrc.XRCCTRL(self.vistabase, '')
        self.vistabase.selFechaIni = xrc.XRCCTRL(self.vistabase, '')
        self.vistabase.selFechaFin = xrc.XRCCTRL(self.vistabase, '')
        
        #--------------------------------------------------------------#
        #-----------------------Vista Principal------------------------#
        #--------------------------------------------------------------#
        
        self.frame = self.res.LoadFrame(None,'MyFrame')
        self.frame.CList = xrc.XRCCTRL(self.frame, 'listaApesar')
        self.frame.SalidaText = xrc.XRCCTRL(self.frame, 'salidaBal')
        self.frame.f1ip = xrc.XRCCTRL(self.frame, 'f1ip')
        self.frame.f1is = xrc.XRCCTRL(self.frame, 'f1is')
        self.frame.f1fp = xrc.XRCCTRL(self.frame, 'f1fp')
        self.frame.f1fs = xrc.XRCCTRL(self.frame, 'f1fs')
        self.frame.r1i = xrc.XRCCTRL(self.frame, 'r1i')
        self.frame.r1f = xrc.XRCCTRL(self.frame, 'r1f')
        self.frame.f2ip = xrc.XRCCTRL(self.frame, 'f2ip')
        self.frame.f2is = xrc.XRCCTRL(self.frame, 'f2is')   
        self.frame.f2fp = xrc.XRCCTRL(self.frame, 'f2fp')
        self.frame.f2fs = xrc.XRCCTRL(self.frame, 'f2fs')
        self.frame.r2i = xrc.XRCCTRL(self.frame, 'r2i')
        self.frame.r2f = xrc.XRCCTRL(self.frame, 'r2f')
        
        self.frame.texpeso = {"ini":(xrc.XRCCTRL(self.frame, 'r1i'),
            xrc.XRCCTRL(self.frame, 'f1ip'),
            xrc.XRCCTRL(self.frame, 'f1is'),
            xrc.XRCCTRL(self.frame, 'f2ip'),
            xrc.XRCCTRL(self.frame, 'f2is'),
            xrc.XRCCTRL(self.frame, 'r2i')),
            "fin":(xrc.XRCCTRL(self.frame, 'r1f'),
            xrc.XRCCTRL(self.frame, 'f1fp'),
            xrc.XRCCTRL(self.frame, 'f1fs'),
            xrc.XRCCTRL(self.frame, 'f2fp'),
            xrc.XRCCTRL(self.frame, 'f2fs'),
            xrc.XRCCTRL(self.frame, 'r2f'))}       
            
        self.frame.btnCom = xrc.XRCCTRL(self.frame, 'btnComenzar')
        self.frame.btnEnviar = xrc.XRCCTRL(self.frame, 'btnEnviar')
        self.frame.btnEnviar.Disable()
        self.winFinal = (self.frame.f1fp, self.frame.f1fs, self.frame.r1f,
            self.frame.f2fp, self.frame.f2fs, self.frame.r2f) 
        self.winIni = (self.frame.f1ip, self.frame.f1is, self.frame.r1i,
            self.frame.f2ip,self.frame.f2is, self.frame.r2i) 
        for col, text in enumerate(self.valuecols):
            self.frame.CList.InsertColumn(col, text)
        for anchos in enumerate(self.widecols):
            self.frame.CList.SetColumnWidth(anchos[0], anchos[1])
        #Handlers------------------------------------------------------#
        self.frame.Bind(wx.EVT_CLOSE, self.OnCloseFrame)
        self.frame.Bind(wx.EVT_MENU, self.OnFrameSalir, id=xrc.XRCID('salir')) # Menú salir
        self.frame.Bind(wx.EVT_MENU, self.OnFrameAcerca, id=xrc.XRCID('acercaDe')) #Menú información
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCf1ip,id=xrc.XRCID('cf1ip'))
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCf1fp,id=xrc.XRCID('cf1fp'))
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCf1is,id=xrc.XRCID('cf1is'))
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCf1fs,id=xrc.XRCID('cf1fs'))
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCr1i,id=xrc.XRCID('cr1i'))
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCr1f,id=xrc.XRCID('cr1f'))
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCf2ip,id=xrc.XRCID('cf2ip'))
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCf2fp,id=xrc.XRCID('cf2fp'))
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCf2is,id=xrc.XRCID('cf2is'))
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCf2fs,id=xrc.XRCID('cf2fs'))
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCr2i,id=xrc.XRCID('cr2i'))
        #~ self.frame.Bind(wx.EVT_BUTTON,self.OnCr2f,id=xrc.XRCID('cr2f'))
        self.frame.Bind(wx.EVT_BUTTON,self.OnEnviar,id=xrc.XRCID('btnEnviar'))
        self.frame.Bind(wx.EVT_TOGGLEBUTTON,self.OnComenzarPesada,id=xrc.XRCID('btnComenzar'))
        EVT_RESULT(self.frame, self.OnAcquireData)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnPItemSelected, self.frame.CList)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnPItemDeselected, self.frame.CList)        
        self.frame.conectado = False    # flag que indica conexión con la balanza
        self.frame.alive = True         # flag que mantiene con vida el trhead de conexión
        self.frame.selected = []        # item seleccionado de la lista a pesar en el frame
        #--------------------------------------------------------------#
        #~ self.alive = True
        return True
    
    #------------------------------------------------------------------#
    
    #Funciones del Diálogo de carga------------------------------------#
    def OnCloseDiagCarga(self,evt):
        self.CloseAll()
        evt.Skip()
        
    def OnMostrarBase(self,evt):
        evt.Skip()
    
    def OnFocusVin(self,evt):
        """borra lo escrito y desengancha el evento"""
        self.ctxtvinVehiculo.Clear()
        self.ctxtvinVehiculo.Unbind(wx.EVT_SET_FOCUS)
        evt.Skip()
        
    def OnCargar(self,evt):
        """carga los elementos agregados por el usuario a la lista de tareas
        siempre que los mismos sean coherentes (vin no repetido, vasos no 
        repetidos y sin datos vacíos)"""    
        VASOS = self.choiceVasos.GetStringSelection()
        VIN = self.ctxtvinVehiculo.GetValue()
        MODELO = self.ctxtModelo.GetValue()
        USUARIO = self.comboUser.GetValue()
        #Verifica que se hayan ingresado todos los campos
        if ((VASOS != "")&(VIN != "")&(MODELO != "")&(USUARIO != "")&
            (VIN != "Ingrese VIN")):
            #Verifica que no se ingrese un mismo vin para dos ensayos    
            for item in self.Tareas:
                if item["vin"]==VIN:
                    wx.MessageBox('''Ese VIN ya existe''')
                    return
            self.choiceVasos.Delete(self.choiceVasos.GetSelection())      
        #elimina los vasos para no usarlos mas de una vez
            hora = time.strftime("%Y%m%d%H%M%S",time.localtime())
        #la hora llena el campo fechahora de la base de datos esta es
        #la key y es única para cada tupla.
        #Agregar taréa a la lista-------------------------------#   
            self.Tareas.append({"vin":VIN,"modelo":MODELO,"vasos":VASOS,
                "repeticiones":self.choicesRep.GetStringSelection(),
                "usuario":USUARIO,"fechahora":hora,"terminado":"N"})
            for a in llaves:
                self.Tareas[-1].setdefault(str(a),None) 
            #-------------------------------------------------------#
            #poner en la lista los valores cargados por el usuario--#
            self.CargarEnLista(self.dlgCList,self.Tareas[-1])
            #-------------------------------------------------------#
            #Borrar campos para una nueva carga---------------------#
            self.ctxtvinVehiculo.Clear()
            self.ctxtModelo.Clear()  
            #-------------------------------------------------------#
        else:
            wx.MessageBox('''Por Favor \nCompletar TODOS\nlos campos ''')
        evt.Skip()
            
    def forfechahora(self,fecha):
        """transforma el formato de la fecha a uno legible"""
        cadena = fecha[0:4] + "-" + fecha[4:6] + "-" + fecha[6:8] \
            + " " + fecha[8:10] + ":" + fecha[10:12] + ":" +fecha[12:14]
        return cadena
        
    def OnEItemSelected(self, evt):
        """Agrega item seleccionado a una lista, si se acepta esta será 
        la lista de tareas a pesar"""
        self.currentItem = evt.m_itemIndex
        self.seleccionados.append(self.currentItem)
        evt.Skip()

    def OnEItemDeselected(self, evt):
        """elimina de la lista self.seleccionados un item de la lista 
        de tareas empezadas"""
        item = evt.m_itemIndex
        self.seleccionados.remove(item)
        #print ("OnItemDeselected: %d" % evt.m_itemIndex)
        evt.Skip()
        
    def OnCItemSelected(self, evt):
        """ Selecciona elementos de la lista para poder borrarlos """
        item = evt.m_itemIndex
        self.diagCselected.append(item)
        evt.Skip()
        
    def OnCItemDeselected(self, evt):
        item = evt.m_itemIndex
        print "deseleccionado %s " % item,
        self.diagCselected.remove(item)
        print self.diagCselected
        evt.Skip()
 
    def OnBorrarSeleccion(self,evt):
        #~ print self.Tareas
        for item in self.diagCselected:
            self.dlgCList.DeleteItem(item)
            self.Tareas.pop(-item-1)
        self.diagCselected = []
        #~ print self.Tareas
        evt.Skip()
    
    def OnBorrarLista(self,evt):
        """Borra la lista de tareas, la lista self.Tareas y rellena el item
            Vasos"""
        self.Tareas = []
        self.dlgCList.DeleteAllItems()    #ClearAll() generaba segmetation fail
        self.choiceVasos.SetItems(VASOS) 
        evt.Skip()
        
    def OnEmpezar(self,evt):
        if self.Tareas == []:
            wx.MessageBox('''No hay tareas que hacer!''')
            return
        self.gesbbdd.Agregar(self.Tareas)
        self.ComenzarFramePesar()
        evt.Skip()
        #carga tareas en la lista

    def OnContinuar(self,evt):
        print "continuar pesadas anteriores"
        if self.seleccionados == []:
            wx.MessageBox('''No hay tareas seleccionadas!''')
            return
        self.Tareas = []
        #carga tareas en la lista
        for index in self.seleccionados:
            #La lista de tareas no terminadas extraída de la base de datos
            #es inversa a la lista que
            #se muestra en diagEList por eso se usa [-index-1]            
            self.Tareas.append(self.NoTerminadas[-1 -index])
        self.ComenzarFramePesar()
        evt.Skip()
        
    def ComenzarFramePesar(self):
        for items in self.Tareas:
            self.CargarEnLista(self.frame.CList,items)
        self.frame.Show()
        self.frame.Fit()
        self.frame.Center()
        self.diagcarga.Destroy()

    #------------------------------------------------------------------#    
    #Funciones del frame cargar desde Base-----------------------------#
    #------------------------------------------------------------------#    

    def OnCargarSelec(self,evt):
        evt.Skip()

    def OnFecha(self,evt):
        evt.Skip()

    def OnCloseVistaBase(self,evt):
        self.CloseAll()
        evt.Skip()
        
    #------------------------------------------------------------------#    
    #Funciones del frame inicial---------------------------------------#
    #------------------------------------------------------------------#    
    
    def OnFrameSalir(self,evt):
        self.frame.Close() 
        evt.Skip() 
        
    def OnFrameAcerca(self,evt):
        info = wx.AboutDialogInfo()
        info.Name = "Tecno Cuchis"
        info.Version = VERSION
        info.Copyright = "(C) 2010 Santiago Paleka"
        info.Description =  "Sofware de manejo simplificado\nPara Balanza \
Mettler Toledo"
        info.Developers = [ "Santiago Paleka" ]
        wx.AboutBox(info)
        evt.Skip()
        
    def OnCloseFrame(self, evt):
        self.CloseAll()
        evt.Skip()
        
    def OnComenzarPesada(self,evt):
        if self.frame.btnCom.GetValue():
            self.frame.SetTitle("Pesada de filtros, Pesando")
            self.frame.mensaje = ""
            self.frame.alive = True   #mantiene vivo el thread
            self.Conexion = conector(self.frame)
        else:
            self.frame.SetTitle("Pesada de filtros")
            if self.frame.conectado:
                self.frame.conectado = False
                self.Conexion.writer('DW')
                self.Conexion.writer('K 4')
                time.sleep(0.3)
                self.Conexion.Close()
        if self.frame.conectado:            
        #si el thread está conectado con la balanza habilita botón enviar y
        # prosigue con la secuencia
            self.frame.btnEnviar.Enable()   
            #botón para probar envío de datos
            #~ self.DisableFinal()             
            #deshabilita cuadros de texto
            #~ self.DisableInicial()
            
            self.Conexion.writer('K 3')     
            self.Conexion.writer("WS 0")
            self.puerta = 0
        #deshabilita la respuesta de los botones a la terminal de la balanza
        #los datos son enviados al puerto serie.
            self.indice = -1            #índice que apuntará a una tarea
            self.frame.estados = {"TAREA": self.esTarea, "PESAR": self.esPesar,
                "PESANDO": self.esPesando, "TERMINADO": self.esTerminado,
                "BORRANDO": self.esBorrando }
            self.estado = "TAREA"       #estado del programa.
            self.mettlertoledo()        #función que se comunica con la balanza
    #de aquí en mas cada dato que llegue de la balanza será atendido como un 
    #evento EVT_NEW_DATA unido a la función OnAcquireData(self,evt):
        else:
            #si no hubo conexión, o se cerró 
            self.frame.btnEnviar.Disable()
            self.EnableFinal()
            self.EnableInicial()
        evt.Skip()
    
        
    def OnEnviar(self,evt):
        if self.frame.conectado:
            self.frame.SalidaText.Clear()
            self.Conexion.writer("SIU")
        evt.Skip()
        
    def OnPItemSelected(self, evt):
        item = evt.m_itemIndex
        self.frame.selected = item
        self.CargarPesos(self.Tareas[-item-1])
        evt.Skip()
        
    def OnPItemDeselected(self, evt):
        item = evt.m_itemIndex
        self.frame.selected = None
        for wins in self.winIni:
            wins.Clear()
        evt.Skip()
    
    def OnAcquireData(self,evt):
        """Recibe un dato del el thread lector y dependiendo su valor dispara
        la función necesaria, el switch se hace con un diccionario 
        de funciones"""
        print "llegó el dato: " + evt.data + " estado actual: " + self.estado
        if evt.data == CERO:
            self.Conexion.writer("DW")
            self.Conexion.writer("Z")
            evt.Skip()
        elif evt.data == OPENLEFT:
            if self.puerta == 0:        #puerta cerrada, abrir
                self.Conexion.writer("WS 2")
                self.puerta = 2
            else:
                self.Conexion.writer("WS 0")
                self.puerta = 0
        elif evt.data == OPENRIGTH:
            if self.puerta == 0:        #puerta cerrada, abrir
                self.Conexion.writer("WS 1")
                self.puerta = 1
            else:
                self.Conexion.writer("WS 0")
                self.puerta = 0
        else:
            self.frame.estados[self.estado](evt) #diccionario de funciones
        
        
#-------------------------------------------------------------------------#
#------Funciones llamadas desde el diccionario self.frame.estados---------#
#-------------------------------------------------------------------------#

    def esTarea(self,evt):
        if evt.data == OK:
                self.estado = "PESAR"
                self.flg_borrar = False
                self.Filtros = filtros(self,self.pesando[0],self.Tareas\
                    [self.indice]["repeticiones"])
                #instancia de la clase filtros, inicial o final, y con el 
                #numero de repeticiones.
                self.Conexion.printM(self.pesando[1][0])
                #imprime en la pantalla de la terminal mettler y en un log
        elif evt.data == DOWN:
            self.indice -= 1
            if self.indice < -len(self.Tareas):
                self.indice = self.indice + len(self.Tareas)
            self.mettlertoledo()
        elif evt.data == UP:
            self.indice += 1
            if self.indice == 0:
                self.indice = -len(self.Tareas)
            self.mettlertoledo()
        elif evt.data == NO:
            pass
 
    def esPesar(self,evt):
        if evt.data == OK:
            self.estado = "PESANDO"
            #Cambia al estado pesando
            self.Conexion.writer("DW")
            #Vuelve a mostrar el peso en pantalla
            print self.Filtros.quefiltro
        elif evt.data == DOWN:
            self.Filtros.downpuntero()
            self.Conexion.printM(self.pesando[1][self.Filtros.puntero])
        elif evt.data == UP:
            self.Filtros.uppuntero()
            self.Conexion.printM(self.pesando[1][self.Filtros.puntero])
        elif evt.data == NO:
            self.estado = "BORRANDO"
            self.Conexion.printM("del ultimo?")
            self.selector = 0
            self.queborrar = ("ult","todo")
        evt.Skip()
            
    def esBorrando(self,evt):
        if evt.data == OK:
            print "borrando " + self.queborrar[self.selector] + " filtro " + self.pesando[1][self.Filtros.puntero]
            self.Filtros.Del(self.selector)
            self.estado = "PESAR"
            self.Conexion.printM(self.pesando[1][self.Filtros.puntero])
        elif evt.data == DOWN:
            self.selector -= 1
            if self.selector == -1:
                self.selector = len(self.queborrar)-1
            self.Conexion.printM("del " + self.queborrar[self.selector])
        elif evt.data == UP:
            self.selector += 1
            if self.selector == len(self.queborrar):
                self.selector = 0
            self.Conexion.printM("del " + self.queborrar[self.selector])
        elif evt.data == NO:
            self.estado = "PESAR"
            self.Conexion.printM(self.pesando[1][self.Filtros.puntero])

            
    def esPesando(self,evt):
        if (((evt.data[0:3] == "S S")|(evt.data[0:3] == "S D"))&(self.Filtros.guardar)):
            """si el dato que llega es una medida de peso y se está pesando"""
            if self.Filtros.Append(evt.data[-11:-3]):   
        # guarda el valor del peso, si retorna True es por que ya se  
        # pesaron las repeticiones.
                if not self.pesando[2][self.Filtros.puntero]:
                    self.pesando[1][self.Filtros.puntero] += "*"
                    self.pesando[2][self.Filtros.puntero] = True  
                #tilda el filtro como pesado
                self.frame.texpeso[self.pesando[0]][self.Filtros.puntero].Clear()
                self.frame.texpeso[self.pesando[0]][self.Filtros.puntero].\
                    AppendText(self.Filtros.Promedio(self.Filtros.puntero))
                if False in self.pesando[2]:
                    #~ self.Filtros.puntero = vacio #apunta al próximo filtro vacío
                    self.Filtros.uppuntero()
                    self.estado = "PESAR"
                    self.Conexion.printM(self.pesando[1][self.Filtros.puntero])
                else:    
                    self.Conexion.printM("terminado?")
                    self.estado = "TERMINADO"
            self.Filtros.guardar = False
            print evt.data
        if evt.data == OK:
            self.Conexion.writer("SIU")
            self.Filtros.guardar = True
        #este flag indica que hay que guardar el próximo valor 
        #que llegue de la balanza
        elif evt.data == NO:
            self.estado = "BORRANDO"
            self.Conexion.printM("del ultimo?")
            self.selector = 0
            self.queborrar = ("ult","todo")
            
        elif evt.data == DOWN:
            """Mientras se está pesando un filtro se puede cambiar a otro"""
            self.estado = "PESAR"
            self.Filtros.downpuntero()
            self.Conexion.printM(self.pesando[1][self.Filtros.puntero])
        elif evt.data == UP:
            self.estado = "PESAR"
            self.Filtros.uppuntero()
            self.Conexion.printM(self.pesando[1][self.Filtros.puntero])


        evt.Skip()
            
    def esTerminado(self,evt):
        """Tarea terminada, pregunta si seguir o guardar promedio"""
        if evt.data == NO:
            self.estado = "PESAR"
            self.Conexion.printM(self.pesando[1][self.Filtros.puntero])
        elif evt.data == OK:
            self.saveonbase()
            self.estado = "TAREA"
            self.mettlertoledo()
        
    def saveonbase(self):
        """salva el valor actual de el diccionario en la base de datos"""
        for n in range(6):
            self.gesbbdd.nuevoValor((self.Filtros.quefiltro[n],self.Filtros.Promedio(n)),
            ("fechahora",self.Tareas[self.indice]["fechahora"]))
        
#-------------------------------------------------------------------------#
#-------------------------------------------------------------------------#
#-------------------------------------------------------------------------#

    def DisableFinal(self):
        for wins in self.winFinal:
            wins.Disable()
            
    def EnableFinal(self):
        for wins in self.winFinal:
            wins.Enable()
        4    
    def DisableInicial(self):
        for wins in self.winIni:
            wins.Disable()
            
    def EnableInicial(self):
        for wins in self.winIni:
            wins.Enable()
            
    def CargarPesos(self,diccio):
        for win in self.winIni:
            win.Clear()
        self.frame.f1ip.AppendText(str(diccio["F1Pi"]))
        self.frame.f2ip.AppendText(str(diccio["F2Pi"]))
        self.frame.f1is.AppendText(str(diccio["F1Si"]))
        self.frame.f2is.AppendText(str(diccio["F2Si"]))
        self.frame.r1i.AppendText(str(diccio["R1i"]))
        self.frame.r2i.AppendText(str(diccio["R2i"]))
        
    def mettlertoledo(self):
        tarea = self.Tareas[self.indice]
        if (((tarea['F1Pi'] == "")|(tarea['F1Si'] == "")|
            (tarea['F2Pi'] == "")|(tarea['F2Si'] == ""))|
            ((tarea['F1Pi'] == None)|(tarea['F1Si'] == None)
            |(tarea['F2Pi'] == None)|(tarea['F2Si'] == None))):
    #Este if verifica que no existan datos iniciales para esta tarea
            self.Conexion.printM('Ini Vas=' + str(tarea['vasos']))
            self.pesando = ["ini",['ref 1','pri fas 1','sec fas 1',
                'pri fas 2','sec fas 2','ref 2'],[False,False,False,False,
                False,False]]
        else:
            self.Conexion.printM('fin Vas=' + str(tarea['vasos']))
            self.pesando = ["fin",['ref 1','pri fas 1','sec fas 1',
                'pri fas 2','sec fas 2','ref 2'],[False,False,False,False,
                False,False]]
            
#----------------------------------------------------------------------#
#---------Funciones para todas las ventanas----------------------------#
#----------------------------------------------------------------------#
    
    def CloseAll(self):
        if self.frame.conectado:
            self.Conexion.writer("quit")
            self.frame.alive = False
            self.Conexion.thread.join()
        self.alive = False
        try:
            self.diagcarga.Destroy()
        except:
            pass
        try:
            self.vistabase.Destroy()
        except:
            pass
        try:
            self.frame.Destroy()
        except:
            pass
    
    def CargarEnLista(self,Lista,Dic):
        index = Lista.InsertStringItem(0, str(Dic["vin"]))
        Lista.SetStringItem(index, 1, str(Dic["modelo"]))
        Lista.SetStringItem(index, 2, str(Dic["vasos"]))
        Lista.SetStringItem(index, 3, str(Dic["repeticiones"]))
        Lista.SetStringItem(index, 4, str(Dic["usuario"])) 
        Lista.SetStringItem(index, 5, self.forfechahora(str(Dic["fechahora"])))
        


class ThreadLector(threading.Thread):
    """
    Thread que se queda escuchando datos en el puerto de conexión.
    Y mantiene con vida la conexión
    """
    def __init__(self, threadNum, window, conector):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.window = window
        self.conector = conector

    def stop(self):
        self.window.s.close()
    
    def run(self):  
        """thread que se encarga de recibir los datos que vienen de la balanza
        Por medio de una conexión TCP"""
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
                    #protocolo propio de este programa para mantener viva la 
                    #conexió y detectar posibles cortes
                else:
                    wx.PostEvent(self.window, AcquireEvent(mensaje[:-2]))   
        print "conexión cerrada"

class conector:
    """esta  clase se dedica a recibir y enviar datos al servidor conectado\
    a la balanza"""
    def __init__(self,window):
        self.window = window
        self.s = socket.socket()
        self.s.settimeout(4)
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
        """envía el dato code a la balanza, le agrega el fin de linea
        requerido por la misma, si code = quit, procede a cerrar a conexión
        y matar el thread"""
        if code[0:4] == "quit":
            print "CerrandoSocket"
            self.s.send("quit")
            self.s.close()
            return
        c = code + "\r\n"
        self.s.send(c)

    def printM(self,texto):
        """imprime el texto pasado por argumento en la pantalla"""
        cadena = 'D "'+texto+'"'+'\r\n'
        self.s.send(cadena)
        self.scrMett = texto       #conserva la última cadena enviada a la pantalla
                                    #mettler
        
    def Close(self):
        """cierra la conexión, mata el thread lector"""
        self.window.alive = False
        self.window.conectado = False
        self.s.send("quit")
        self.s.close()

class filtros():
    
    def __init__(self,win,momento,repeticiones):
        self.win = win              #ventana que instancia
        self.rep = repeticiones
        self.guardar = False
        self.puntero = 0
        # carga un diccionario y tres tuplas con las llaves correspondientes 
        # a una carga inicial o una final
        if momento == "ini":
            self.filtros = {"F1Pi": [],"tF1Pi": None, "dpF1Pi": None,"F1Si": [],
                "tF1Si": None,"dpF1Si": None,"F2Pi": [],"tF2Pi": None,"dpF2Pi": None,
                "F2Si": [],"tF2Si": None,"dpF2Si": None,"R1i": [],"tR1i": None,
                "dpR1i": None,"R2i": [],"tR2i": None,"dpR2i": None}
            self.quefiltro = ("R1i","F1Pi","F1Si","F2Pi","F2Si","R2i")
            self.quefiltrodp = ("dpR1i","dpF1Pi","dpF1Si","dpF2Pi","dpF2Si","dpR2i")
            self.quefiltrotemp = ("tR1i","tF1Pi","tF1Si","tF2Pi","tF2Si","tR2i")
        elif momento == "fin":
            self.filtros = {"F1Pf": [],"tF1Pf": None, "dpF1Pf": None,"F1Sf": [],
                "tF1Sf": None,"dpF1Sf": None,"F2Pf": [],"tF2Pf": None,
                "dpF2Pf": None,"F2Sf": [],"tF2Sf": None,"dpF2Sf": None,
                "R1f": [],"tR1f": None,"dpR1f": None,"R2f": [],
                "tR2f": None, "dpR2f": None}
            self.quefiltro = ("R1f","F1Pf","F1Sf","F2Pf","F2Sf","R2f")
            self.quefiltrodp = ("dpR1f","dpF1Pf","dpF1Sf","dpF2Pf","dpF2Sf","dpR2f")
            self.quefiltrotemp = ("tR1f","tF1Pf","tF1Sf","tF2Pf","tF2Sf","tR2f")
        else:
            return 1
        
    def Append(self,peso):
        """Agrega el valor peso pasado por argumento a el filtro que está 
        apuntado por self.puntero, si ya se cumplió con el número de repeticiones
        requeridas devuelve True, si no False"""
        if str(len(self.filtros[self.quefiltro[self.puntero]])) < self.rep:
            self.filtros[self.quefiltro[self.puntero]].append(peso)
        if str(len(self.filtros[self.quefiltro[self.puntero]])) >= self.rep:
            if self.win.pesando[2][self.puntero]:
                self.filtros[self.quefiltro[self.puntero]].append(peso)
                
            print str(self.filtros[self.quefiltro[self.puntero]]) + " " \
                +str(self.quefiltro[self.puntero])
            
            return True
        elif str(len(self.filtros[self.quefiltro[self.puntero]])) > self.rep:
            self.win.estado = "agregando"
        return False
        
    def Del(self,queborrar):
        """elimina valores de pesadas, todos, ultimo o el inidicado* """
        if queborrar == 1:
            """elimina todos los valores"""
            self.filtros[self.quefiltro[self.puntero]] = []
        elif queborrar == 0: 
            """elimina el último valor"""
            self.filtros[self.quefiltro[self.puntero]].pop()
        if len(self.filtros[self.quefiltro[self.puntero]]) < self.rep:
            print "ahora le faltan pesadas"
            self.win.pesando[2][self.puntero] = False
            self.win.pesando[1][self.puntero] = self.win.pesando[1][self.puntero].replace("*","") 
                          
    def downpuntero(self):
        """decrementa el puntero y da la vuelta si llegó al principio de la lista"""
        self.puntero -= 1
        if self.puntero < 0:         #analiza la lista circularmente
            self.puntero = 5
    
    def uppuntero(self):
        """Incrementa el puntero y da la vuelta si llegó al fin de la lista"""
        self.puntero += 1
        if self.puntero == 6:
            self.puntero = 0
    
    def Promedio(self,punt):
        """devuelve un string con el valor promedio del filtro apuntado por
        punt enviado como argumento"""
        total = 0.0
        for valor in self.filtros[self.quefiltro[punt]]:
            total += float(valor)
        return str(round(total/(len(self.filtros[self.quefiltro[punt]])),3)) 
        #retorna el valor promedio redondeado en tres cifras dps de la coma
        #en formato de cadena

        

            
        #~ self.traductor = {'ref 1':[],'prim fase 1':[],'secu fase 1':[],'prim fase 2':[],'secu fase 2':[],'ref 2':[]}

if __name__ == '__main__':
    Aplicacion = mimain()
    Aplicacion.MainLoop()
    
