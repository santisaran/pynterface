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
        recive una tupla en nvalor con (campo,valor) y el valor que identifica
        la tupla (ej, un nombre de usuario, una fecha, etc)"""
        print "agregar valor " + nvalor[0] + "=" + nvalor[1]+ " en "+tuplakey[0] + " = " + tuplakey[1] 
        try:
            self.cursor.execute("update " + TABLA + " set " + nvalor[0]+" = " + "? where "+tuplakey[0]+ " = ?", (nvalor[1], tuplakey[1]))
        except:
            return 1
        self.bbdd.commit()
        return 0
    
    def Agregar(self,filas):
        """Agrega nuevos campos a la tabla de la base de datos, recive como\
            Parámetro una lista de diccionarios con los valores a agregar"""
        for dic in filas:
            print dic
            diccionario = []
            for item in llaves:
                diccionario.append(dic.get(item,None)) 
                #si el item del diccionario no existe lo crea con el valor
                #None
            try:
                self.cursor.execute("insert into "+ TABLA+" values (?,?,?\
                    ,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",diccionario)
            except (NameError, ValueError):
                print NameError+ str (ValueError)
        self.bbdd.commit()
        
    def Consultar(self, iteme, columna,ordenada = 'fechahora'):
        consulta = "select * from " + TABLA + " where " + columna + " = " + "'" + iteme + "' order by " + ordenada
        self.cursor.execute(consulta)
        return self.cursor.fetchall()
        
        
if __name__ == '__main__':
    ges = gestion("base.dat")
    #~ ges.VerBase()
    listas = ges.Consultar("S.Paleka","Usuario","Usuario")
    ges.nuevoValor(('F1Pi','55.000'),('usuario','P.Amaya'))
    ges.nuevoValor(('F1Si','55.000'),('usuario','P.Amaya'))
    print listas