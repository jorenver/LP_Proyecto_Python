from Escenario import *
from Observer import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import *
from time import sleep
from PyQt4 import QtCore
import sys
import math


class Menu(Escenario):

	def __init__(self,*args):
		Escenario.__init__(self,*args)
		self.setWindowTitle("Ball Neumann")
		Bt_nuevoJ=QPushButton("Nuevo Juego",self)
		Bt_nuevoJ.setGeometry(360,320,200,65)
		Bt_AcercaDe=QPushButton("Acerca De",self)
		Bt_AcercaDe.setGeometry(360,450,200,65)
		self.connect(Bt_nuevoJ, SIGNAL("clicked()"), self.nuevoJuego)
		self.connect(Bt_AcercaDe, SIGNAL("clicked()"), self.acercaDe)
 
	def nuevoJuego(self):
		print "Nuevo Juego"
		
	def acercaDe(self):
		print "Acerca De"
		
		
	def paintEvent(self, event):       
		paint = QPainter()
		paint.begin(self)
		imagen=QImage("fondo","png")
		center=QPoint(0,0)
		paint.drawImage(center,imagen) # inserto el fondo
		paint.end()
		
app = QApplication(sys.argv)
nivel1 = Menu()
nivel1.show()
app.exec_()