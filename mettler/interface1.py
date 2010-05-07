#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Tue Apr 13 12:25:49 2010

import wx
import threading
import socket
import sys

try:
    import cPickle as pickle
except:
    import pickle

archivo = file("config.txt",'r')
datos = pickle.load(archivo)
BALANZA = datos['IP_BALANZA']
PORT = datos["PORT"]
archivo.close()


class WorkerThread(threading.Thread):
    """
    This just simulates some long-running task that periodically sends
    a message to the GUI thread.
    """
    def __init__(self, threadNum, window):
        threading.Thread.__init__(self)
        self.threadNum = threadNum
        self.window = window
        self.timeToQuit = threading.Event()
        self.timeToQuit.clear()

    def stop(self):
        self.window.s.close()
        self.timeToQuit.set()
    
    def run(self):    
        while self.window.alive:
            self.window.s.settimeout(4)
            try:
                mensaje = self.window.s.recv(1024)
            except socket.timeout:
                continue
            except socket.error, msg:
                print msg
                print "broken Pipe2"
                self.window.alive = False
                break
            else:
                if mensaje == "life":
                    self.window.s.send("YESILIVE")
                else:
                    wx.CallAfter(self.window.salidatex.AppendText,mensaje)


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.enviadotex = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.salidatex = wx.TextCtrl(self, -1, "Entrada de datos\n", style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        self.intext = wx.TextCtrl(self, -1, "", style=wx.TE_PROCESS_ENTER)
        self.__set_properties()
        self.__do_layout()
        
        self.Bind(wx.EVT_TEXT_ENTER, self.OnText, self.intext)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        
        self.CenterOnParent()
        self.s = socket.socket()
        self.s.settimeout(4)
        print BALANZA + ":" + str(PORT)
        try:
            self.s.connect((BALANZA, PORT))
        except:
            print "no se pudo abrir Conexión con " + BALANZA + ":" + str(PORT) 
            exit(1)
        self.s.settimeout(None)
        self.count = 1
        self.thread = WorkerThread(self.count, self)
        self.alive = True
        #~ self.threads.append(thread)
        self.thread.start()
        
    def writer(self,c):
        self.s.send(c)
            
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("frame_1")
        self.SetSize((400, 300))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.enviadotex, 1, wx.ALL|wx.EXPAND, 2)
        sizer_1.Add(self.intext, 0, wx.ALL|wx.EXPAND, 3)
        sizer_1.Add(self.salidatex, 4, wx.ALL|wx.EXPAND, 2)
        
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def OnText(self, event): # wxGlade: MyFrame.<event_handler>
        code = self.intext.GetValue()
        print code
        if code[0:4] == "quit":
            self.writer("quit\r\n")
            self.OnCloseWindow(wx.EVT_CLOSE)
            return
        self.enviadotex.AppendText(code + "\n")
        self.intext.Clear()
        code = code.upper()
        self.writer(code + "\r\n")
        event.Skip()
        
    def OnCloseWindow(self, event):
        print "cerrando ventana"
        self.writer("quit")
        self.alive = False
        self.thread.stop() #aqui falta eliminar el thread lector
        self.s.close()
        self.thread.join()
        self.Destroy()
        exit()


# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()