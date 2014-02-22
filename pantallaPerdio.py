from Escenario import *
from Jugador import*
from Duelo import *
from Observer import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
import sys
import math


class pantallaPerdio(QWidget):
	dimension_x=1000
	dimension_y=650
	def __init__(self,*args):
		print "Eloy"
		QWidget.__init__(self,*args)
		contenedor=QVBoxLayout()
		self.setGeometry(50,50,self.dimension_x,self.dimension_y)
		self.setWindowIcon(QIcon("icono.png"))
		self.setLayout(contenedor)
		
	def paintEvent(self, event):       
		paint = QPainter()
		paint.begin(self)
		imagen=QImage("gameover","png")
		center=QPoint(0,0)
		paint.drawImage(center,imagen) # inserto el fondo
		paint.end()
		

	
