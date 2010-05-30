#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sin título.py
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
import sqlite3 as dbapi
try:
    import cPickle as pickle
except:
    import pickle

archivo = file("config.txt",'r')        #archivo donde se encuentran las
datos = pickle.load(archivo)            #configuraciones iniciales.
BASEDEDATOS = datos['BASEDATOS']        #Nombre de la base de datos
TABLA = datos['TABLA']
VASOS = datos['IDVASOS']        # Items de vasos disponibles
BALANZA = datos['IP_BALANZA']   # Ip de la pc que tiene la balanza en su puerto serie
dic = datos['dic']              # estructura de diccionario para la base
llaves = datos['llaves']        # columnas de la base de datos (ordenadas).
archivo.close()


class gestion():
    def __init__(self,archivo):
        self.archivo = archivo
        self.bbdd = dbapi.connect(self.archivo)
        self.bbdd.row_factory = dbapi.Row       #esto me permite obtener diccionarios en vez de tuplas
                                                #cuando consulto la bbdd
        self.cursor = self.bbdd.cursor()
        self.dic = dic
    def VerBase(self):
        self.cursor.execute("""select * from pesadas""")
        for r in self.cursor.fetchall():
            print r
            print "\n"

        
    def nuevaPesada(self,ntupla):
        """Agregar nueva pesada a la base de datos"""
        pass
        
    def nuevoValor(self,nvalor,tuplakey):
        """Agregar un valor en una tupla existente de la base de datos
        recibe una tupla de tuplas en nvalor con ((campo,valor),(campo,valor),...)
        y el valor que identifica la/s tupla (ej, un nombre de usuario, una fecha, etc)"""
        cadena = ""
        for par in nvalor:
            cadena += par[0] + " = " + par[1] + ", "
        print "\nagregar valor " + cadena[:-2] + " en "+tuplakey[0] + " = " + tuplakey[1] + "\n"
        carga = "update " + TABLA + " set " + cadena[:-2] + " where "+tuplakey[0]+ " = " + tuplakey[1]
        self.cursor.execute(carga)
        self.bbdd.commit()
        return 0
    
    def Agregar(self,filas):
        """Agrega nuevos campos a la tabla de la base de datos, recive como\
            Parámetro una lista de diccionarios con los valores a agregar"""
        for dic in filas:
            valores = [dic.get(item, None) for item in llaves]
            qmarks = ','.join(['?']*len(llaves))
            #si el item del diccionario no existe lo crea con el valor
            self.cursor.execute("insert into pesadas values (" + qmarks + ")", valores)
        self.bbdd.commit()
        
    def Consultar(self, iteme, columna,ordenada = 'fechahora'):
        consulta = "select * from " + TABLA + " where " + columna + " = " + "'" + iteme + "' order by " + ordenada
        self.cursor.execute(consulta)
        return self.cursor.fetchall()
        
        
if __name__ == '__main__':
    ges = gestion("base.dat")
    #~ ges.VerBase()
    #listas = ges.Consultar("S.Paleka","Usuario","Usuario")
    ges.nuevoValor((('F1Pi','55.000'),("tF1Pi","22.0"),("dpF1Pi","9.5")),('usuario','M.Ruiz'))

