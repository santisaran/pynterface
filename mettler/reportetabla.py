#!/usr/bin/env python
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import Spacer, SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph, Image
from reportlab.lib import colors
try:
    import cPickle as pickle
except:
    import pickle
import gestionbbdd as gesbbdd

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

gesbd = gesbbdd.gestion(BASEDEDATOS)
baserows = gesbd.VerBase()
d = {}
data = []

#---------data = [(col, dic),(),(),()...]

for e,dic in enumerate(baserows):
    for key in llaves:
        d[key] = dic[key]
    data.append(d)
    d = {}

A = 1


def generar(item):
    A=item
    styleSheet=getSampleStyleSheet()
    story=[]
    h1=styleSheet['Title']
    h1.pageBreakBefore=0   # evita el salto de página por cada cabezera nueva.
    h1.keepWithNext=1
    #h1.backColor=colors.yellow
    h2=styleSheet['Heading2']
    h2.pageBreakBefore=0
    h2.keepWithNext=1
    P=Paragraph("<bold>Pesada de Particulado</bold>",h1)
    story.append(P)
    story.append(Spacer(10,10))
    
    #-------------------Datos de la base--------------------------------
    fecha = "Fecha: " + forfechahora(data[A]["fechahora"])
    horaini = "Inicial: " + forfechahora(data[A]["horainicio"])
    horafin = "Final: " + forfechahora(data[A]["horafin"])
    responsable = "Responsable: " + data[A]["usuario"]
    vin = "VIN: " + data[A]["vin"]
    vasos = "id vasos: " + data[A]["vasos"]
    repet = data[A]["repeticiones"]
    F1Pi = data[A][ "F1Pi"]
    tF1Pi = data[A]["tF1Pi"]
    dpF1Pi = data[A]["dpF1Pi"]
    F1Pf = data[A]["F1Pf"]
    tF1Pf = data[A]["tF1Pf"]
    dpF1Pf = data[A]["dpF1Pf"]
    F1Si = data[A]["F1Si"]
    tF1Si = data[A]["tF1Si"]
    dpF1Si = data[A]["dpF1Si"]
    F1Sf = data[A]["F1Sf"]
    tF1Sf = data[A]["tF1Sf"]
    dpF1Sf = data[A]["dpF1Sf"]
    F2Pi = data[A]["F2Pi"]
    tF2Pi = data[A]["tF2Pi"]
    dpF2Pi = data[A]["dpF2Pi"]
    F2Pf = data[A]["F2Pf"]
    tF2Pf = data[A]["tF2Pf"]
    dpF2Pf = data[A]["dpF2Pf"]
    F2Si = data[A]["F2Si"]
    tF2Si = data[A]["tF2Si"]
    dpF2Si = data[A]["dpF2Si"]
    F2Sf = data[A]["F2Sf"]
    tF2Sf = data[A]["tF2Sf"]
    dpF2Sf = data[A]["dpF2Sf"]
    R1i = data[A]["R1i"]
    tR1i = data[A]["tR1i"]
    dpR1i = data[A]["dpR1i"]
    R1f = data[A]["R1f"]
    tR1f = data[A]["tR1f"]
    dpR1f = data[A]["dpR1f"]
    R2i = data[A]["R2i"]
    tR2i = data[A]["tR2i"]
    dpR2i = data[A]["dpR2i"]
    R2f = data[A]["R2f"]
    tR2f = data[A]["tR2f"]
    dpR2f = data[A]["dpR2f"]
    
    #Tabla principal, datos de vehículo, horas y usuario.
    t=Table([[fecha,horaini,horafin],
            [vin, responsable, vasos, "Repeticiones: " + repet]
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
    doc=SimpleDocTemplate("paragrahp.pdf",pagesize=A4,topMargin=30,leftMargin=30,rightMargin=10, title="Particulado",
        author = "Pynterface")
  

    
    doc.build(story)
    
if __name__ == '__main__':
    generar(-7)
