#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       sin título.py
#       
#       Copyright 2010 Santiago Paleka <saran@Santi>
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

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A4,legal


def main():
    c=canvas.Canvas("primer.pdf",pagesize=A4)
    c.drawString(50,500, "Mi primer pdf")
    c.drawString(250,300, "coordenada (250,300)")
    c.showPage
    c.save()
    return 0

if __name__ == '__main__':
    main()
