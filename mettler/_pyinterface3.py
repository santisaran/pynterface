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
import conexion


#Cargar configuración desde config.txt---------------------------------#
archivo = file("config.txt", 'r')        #archivo donde se encuentran las
datos = pickle.load(archivo)            #configuraciones iniciales.
BASEDEDATOS = datos['BASEDATOS']        #Nombre de la base de datos
VASOS = datos['IDVASOS']        # Items de vasos disponibles
BALANZA = datos['IP_BALANZA']   # Ip de la pc que tiene la balanza en su puerto serie
dic = datos['dic']              # estructura de diccionario para la base
llaves = datos['llaves']        # columnas de la base de datos (ordenadas).
archivo.close()
VERSION = "0.0.1"
SI = "K C 7"
UP = "K C 9"
DOWN = "K C 8"
#----------------------------------------------------------------------#

class SerialEvent(wx.PyEvent):
    def __init__(self, evtType, id):
        wx.PyEvent.__init__(self, evtType, id)
        self.mensaje = ""

    def GetMensaje(self):
        return self.mensaje

    def SetMensaje(self, mensaje):
        self.mensaje = mensaje

class mimain(wx.App):
    def OnInit(self):
        self.seleccionados = []
        self.diagCselected = []
        self.Tareas = []
        self.widecols = (120,100,wx.LIST_AUTOSIZE_USEHEADER,wx.LIST_AUTOSIZE_USEHEADER,120,130)
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
        #~ self.dlgEList.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        #~ self.dlgEList.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

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
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnPItemSelected, self.frame.CList)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnPItemDeselected, self.frame.CList)        
        self.frame.conectado = False
        self.frame.alive = True
        self.frame.selected = []
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
        cadena = fecha[0:4] + "-" + fecha[4:6] + "-" + fecha[6:8] \
            + " " + fecha[8:10] + ":" + fecha[10:12] + ":" +fecha[12:14]
        return cadena
        
    def OnEItemSelected(self, evt):
        self.currentItem = evt.m_itemIndex
        self.seleccionados.append(self.currentItem)
        #print ("OnItemSelected: %s, %s, \n" %
        #                (self.currentItem,
        #                self.dlgEList.GetItemText(self.currentItem)))
        #print self.seleccionados
        evt.Skip()

    def OnEItemDeselected(self, evt):
        item = evt.m_itemIndex
        self.seleccionados.remove(item)
        #print ("OnItemDeselected: %d" % evt.m_itemIndex)
        evt.Skip()
        
    def OnCItemSelected(self, evt):
        item = evt.m_itemIndex
        self.diagCselected.append(item)
        print "seleccionado %s " % item,
        print self.diagCselected
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
            self.frame.alive = True
            self.Conexion = conexion.conector(self.frame)
        else:
            if self.frame.conectado:
                self.frame.conectado = False
                self.Conexion.writer('DW')
                self.Conexion.writer('K 4')
                time.sleep(0.3)
                self.Conexion.Close()
        if self.frame.conectado:
            self.frame.btnEnviar.Enable()   #botón para probar envío de datos
            self.DisableFinal()
            self.DisableInicial()
            self.Conexion.writer('K 3')
            self.mettlertoledo()        #función que se comunica con la balanza
        else:
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
        print self.Tareas[-item-1]
        self.CargarPesos(self.Tareas[-item-1])
        evt.Skip()
        
    def OnPItemDeselected(self, evt):
        item = evt.m_itemIndex
        self.frame.selected = None
        for wins in self.winIni:
            wins.Clear()
        evt.Skip()
        
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
        self.frame.f1ip.Clear()
        self.frame.f2ip.Clear()
        self.frame.f1is.Clear()
        self.frame.f2is.Clear()
        self.frame.r1i.Clear()
        self.frame.r2i.Clear()
        self.frame.f1ip.AppendText(str(diccio["F1Pi"]))
        self.frame.f2ip.AppendText(str(diccio["F2Pi"]))
        self.frame.f1is.AppendText(str(diccio["F1Si"]))
        self.frame.f2is.AppendText(str(diccio["F2Si"]))
        self.frame.r1i.AppendText(str(diccio["R1i"]))
        self.frame.r2i.AppendText(str(diccio["R2i"]))
        
    def mettlertoledo(self):
        #~ for tarea in self.Tareas:
        #~ self.Conexion.writer('D "Comenzar"')
        for tarea in self.Tareas:
            if (((tarea['F1Pi'] == "")|(tarea['F1Si'] == "")|\
                (tarea['F2Pi'] == "")|(tarea['F2Si'] == ""))|\
                ((tarea['F1Pi'] == None)|(tarea['F1Si'] == None)\
                |(tarea['F2Pi'] == None)|(tarea['F2Si'] == None))):
        #Este if verifica que no existan datos iniciales para esta tarea
                cadena = 'D "Inicial V ' + str(tarea['vasos']) +'"'
                self.Conexion.writer(cadena)
            else:
                self.Conexion.writer('D "pes Final"')
                
                
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
        
if __name__ == '__main__':
    Aplicacion = mimain()
    Aplicacion.MainLoop()
    
