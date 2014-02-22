from Escenario import *
from Observer import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import *
from time import sleep
from PyQt4 import QtCore
import sys
import math
from neuroListener import *
from nivel1 import *
from pantallaPerdio import *

class Menu(Escenario,NeuroListener):

	def __init__(self,*args):
		Escenario.__init__(self,*args)
		NeuroListener.__init__(self)
		self.setWindowTitle("Ball Neumann")
		self.Jugador=Jugador(0,0,0,5)
		Bt_nuevoJ=QPushButton("Nuevo Juego",self)
		Bt_nuevoJ.setGeometry(360,320,200,65)
		Bt_AcercaDe=QPushButton("Acerca De",self)
		Bt_AcercaDe.setGeometry(360,450,200,65)
		Bt_Instrucciones=QPushButton("Instrucciones",self)
		Bt_Instrucciones.setGeometry(360,580,200,65)
		self.connect(Bt_nuevoJ, SIGNAL("clicked()"), self.nuevoJuego)
		self.connect(Bt_AcercaDe, SIGNAL("clicked()"), self.acercaDe)
		self.connect(Bt_Instrucciones, SIGNAL("clicked()"), self.instrucciones)
		self.EscenarioActual=None
		self.Duelo=Duelo(self)
		self.state=0 #si esta en un escenario es 0 , si esta en un duelo es 1
		self.inst=None
		#self.setDaemon(True)
		
		
	def nuevoJuego(self):
		print "Nuevo Juego"
		self.start()
		self.EscenarioActual=EscenarioUno(self.Jugador,self)
		self.EscenarioActual.show()
		self.close()	
	
	def acercaDe(self):
		print "Acerca De"
		
	def instrucciones(self):
		print "instrucciones"
		self.inst=pantallaPerdio()
		self.inst.show()
	
	def update(self, Escenario):
		self.state=0
		if Escenario!=None:
			self.EscenarioActual=Escenario
			self.EscenarioActual.mover=True
		else:
			self.stop=True
			self.Pperdio=pantallaPerdio()
			sleep(0.1)
			self.Pperdio.show()
	
	def perder(self):
		self.state=0
		self.stop=True
		self.close()

	def update2(self):
		self.state=1
		self.Duelo.setJugador(self.Jugador)
		self.EscenarioActual.mover=False
		self.Duelo.mover=False
		self.Duelo.comenzar(self.Jugador)
		self.Duelo.mover=True
		
	def paintEvent(self, event):       
		paint = QPainter()
		paint.begin(self)
		imagen=QImage("fondo","png")
		center=QPoint(0,0)
		paint.drawImage(center,imagen) # inserto el fondo
		paint.end()
		
	def derecha(self):
		if(self.EscenarioActual!=None and self.state==0):
			self.EscenarioActual.derecha()
		elif(self.state==1):
			self.Duelo.derecha()
	def izquierda(self):
		if(self.EscenarioActual!=None and self.state==0):
			self.EscenarioActual.izquierda()
		elif(self.state==1):
			self.Duelo.izquierda()
	
	def accion(self):
		if(self.EscenarioActual!=None and self.state==0):
			self.EscenarioActual.accion()
		elif(self.state==1):
			self.Duelo.accion()
	
	
	
		
app = QApplication(sys.argv)
nivel1 = Menu()
nivel1.show()
app.exec_()