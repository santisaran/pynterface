#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       reportetabla.py
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

#--------------------
#   Programa encargado de generar reportes en pdf con datos provenientes de la
# base de datos.

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph, Image
from reportlab.lib import colors
try:
    import cPickle as pickle
except:
    import pickle



archivo = file("config.txt", 'r')        #archivo donde se encuentran las
datos = pickle.load(archivo)            #configuraciones iniciales.
BASEDEDATOS = datos['BASEDATOS']        #Nombre de la base de datos
llaves = datos['llaves'] 
archivo.close()

def forfechahora(fecha):
    """transforma el formato de la fecha a uno legible"""
    if type(fecha) is not (unicode or str):
        return ""
    cadena = fecha[0:4] + "-" + fecha[4:6] + "-" + fecha[6:8] \
        + " " + fecha[8:10] + ":" + fecha[10:12] + ":" +fecha[12:14]
    return cadena

def genrep(tupla,archivo = "pesadas.pdf"):
    #si la tupla está vacía no genera un pdf vacío.
    if len(tupla) == 0: 
        return
    styleSheet=getSampleStyleSheet()
    story=[]
    h1=styleSheet['Title']
    h1.pageBreakBefore=0   # evita el salto de página por cada cabezera nueva.
    h1.keepWithNext=1
    #h1.backColor=colors.yellow
    h2=styleSheet['Heading2']
    h2.pageBreakBefore=0
    h2.keepWithNext=1
    P=Paragraph("Pesada de Particulado",h1)
    story.append(P)
    story.append(Spacer(10,10))
    
    for data in tupla:
        #-------------------Datos de la base--------------------------------
        fecha = "Fecha: " + forfechahora(data["fechahora"])
        horaini = "Inicial: " + forfechahora(data["horainicio"])
        horafin = "Final: " + forfechahora(data["horafin"])
        responsable = "Responsable: " + data["usuario"]
        vin = "VIN: " + data["vin"]
        vasos = "id vasos: " + data["vasos"]
        modelo = "Modelo: " + data["modelo"]
        repet = data["repeticiones"]    
        F1Pi = data[ "F1Pi"]
        tF1Pi = data["tF1Pi"]
        dpF1Pi = data["dpF1Pi"]
        F1Pf = data["F1Pf"]
        tF1Pf = data["tF1Pf"]
        dpF1Pf = data["dpF1Pf"]
        F1Si = data["F1Si"]
        tF1Si = data["tF1Si"]
        dpF1Si = data["dpF1Si"]
        F1Sf = data["F1Sf"]
        tF1Sf = data["tF1Sf"]
        dpF1Sf = data["dpF1Sf"]
        F2Pi = data["F2Pi"]
        tF2Pi = data["tF2Pi"]
        dpF2Pi = data["dpF2Pi"]
        F2Pf = data["F2Pf"]
        tF2Pf = data["tF2Pf"]
        dpF2Pf = data["dpF2Pf"]
        F2Si = data["F2Si"]
        tF2Si = data["tF2Si"]
        dpF2Si = data["dpF2Si"]
        F2Sf = data["F2Sf"]
        tF2Sf = data["tF2Sf"]
        dpF2Sf = data["dpF2Sf"]
        R1i = data["R1i"]
        tR1i = data["tR1i"]
        dpR1i = data["dpR1i"]
        R1f = data["R1f"]
        tR1f = data["tR1f"]
        dpR1f = data["dpR1f"]
        R2i = data["R2i"]
        tR2i = data["tR2i"]
        dpR2i = data["dpR2i"]
        R2f = data["R2f"]
        tR2f = data["tR2f"]
        dpR2f = data["dpR2f"]
    
        #Tabla principal, datos de vehículo, horas y usuario.
        t=Table([[fecha,horaini,horafin,responsable],
                [vin, modelo, vasos, "Repeticiones: " + repet]
                ])
        t.hAlign = 0
        t.setStyle([('BOX',(0,0),(-1,-1), 0.5, colors.black),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ])
        story.append(t)
        story.append(Spacer(10,10))
        
        t1=Table([["","","Peso: mg","","", "Temperatura: ºC","","", "Punto de rocío: ºC"],
            ["","","Primario", "Secundario", "Referencia","Primario", "Secundario", "Ref","Primario", "Secundario", "Ref"],
            ["Fase 1","Inicial",F1Pi,F1Si,R1i,tF1Pi,tF1Si,tR1i,dpF1Pi,dpF1Si,dpR1i],
            [None,"Final",F1Pf,F1Sf,R1f,tF1Pf,tF1Sf,tR1f,dpF1Pf,dpF1Sf,dpR1f],
            ["Fase 2","Inicial",F2Pi,F2Si,R2i,tF2Pi,tF2Si,tR2i,dpF2Pi,dpF2Si,dpR2i],
            [None, "Final", F2Pf, F2Sf, R2f, tF2Pf, tF2Sf, tR2f, dpF2Pf, dpF2Sf, dpR2f]
            ])
            
        t1.setStyle([('TEXTCOLOR',(0,1),(0,-1),colors.blue),
            ('BOX',(0,0),(-1,-1), 0.5, colors.black),
            ('BOX',(2,2),(3,5),2, colors.red),
            ('LINEABOVE', (0,4), (-1,4), 2, colors.purple),
            #('LINEBELOW', (0,0), (-1,0), 1, colors.purple),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('SPAN',(0,2),(0,3)),
            ('SPAN',(0,4),(0,5)),
            ('SPAN',(2,0),(4,0)),
            ('SPAN',(5,0),(7,0)),
            ('SPAN',(8,0),(10,0)),
            ('SPAN',(0,0),(1,1)),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ])
        t1.hAlign = 0
        story.append(t1)
        
        story.append(Spacer(0,15))
    #~ img=Image("images/logo.jpg")
    #~ story.append(img)
    doc=SimpleDocTemplate(archivo,pagesize=A4,topMargin=30,leftMargin=30,rightMargin=10, title="Particulado",
        author = "Pynterface")
  

    
    doc.build(story)
    
if __name__ == '__main__':
    import gestionbbdd
    gesbd = gestionbbdd.gestion(BASEDEDATOS)
    item = gesbd.Consultar("S.Paleka","Usuario","Usuario") #"20100511083405","fechahora")
    genrep(item)
