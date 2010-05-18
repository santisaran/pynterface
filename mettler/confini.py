#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sin título.py
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

def main():
    datos = {'IP_BALANZA':'10.10.8.151',
        'BASEDATOS':'base.dat','TABLA':'pesadas',
        'IDVASOS':('1','2','3','4','5','6','7','8','9'),
        'dic' : {"vin": None,"modelo":None ,"fechahora":None, "vasos":None, "repeticiones":None,
            "horainicio":None, "horafin":None, "usuario":None,"F1Pi": None,
            "tF1Pi": None,"dpF1Pi": None,"F1Pf": None,"tF1Pf": None,
            "dpF1Pf": None,"F1Si": None,"tF1Si": None,"dpF1Si": None,
            "F1Sf": None,"tF1Sf": None,"dpF1Sf": None,"F2Pi": None,
            "tF2Pi": None,"dpF2Pi": None,"F2Pf": None,"tF2Pf": None,
            "dpF2Pf": None,"F2Si": None,"tF2Si": None,"dpF2Si": None,
            "F2Sf": None,"tF2Sf": None,"dpF2Sf": None,"R1i": None,"tR1i": None,
            "dpR1i": None,"R1f": None,"tR1f": None,"dpR1f": None,"R2i": None,
            "tR2i": None,"dpR2i": None,"R2f": None,"tR2f": None,"dpR2f":None,
            "terminado": "N"}, 'llaves': ("vin", "modelo", "fechahora", "vasos", "repeticiones",
            "horainicio", "horafin", "usuario","F1Pi",
            "tF1Pi", "dpF1Pi", "F1Pf", "tF1Pf",
            "dpF1Pf", "F1Si", "tF1Si", "dpF1Si",
            "F1Sf", "tF1Sf", "dpF1Sf", "F2Pi",
            "tF2Pi", "dpF2Pi", "F2Pf", "tF2Pf",
            "dpF2Pf", "F2Si", "tF2Si", "dpF2Si",
            "F2Sf", "tF2Sf","dpF2Sf", "R1i", "tR1i",
            "dpR1i", "R1f", "tR1f", "dpR1f", "R2i",
            "tR2i", "dpR2i", "R2f", "tR2f", "dpR2f",
            "terminado"),
            "PORT":9099
            }
    f = open('config.txt', 'w')
    pickle.dump(datos,f)
    f.close()
    
    return 0

if __name__ == '__main__':
	main()
