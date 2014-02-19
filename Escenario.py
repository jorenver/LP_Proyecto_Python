#clase escenario
import sys
import time
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Escenario(QWidget):
	dimension_x=1000
	dimension_y=650

	def __init__(self,*args):
			QWidget.__init__(self,*args)
			contenedor=QVBoxLayout()
			self.setGeometry(50,50,self.dimension_x,self.dimension_y)
			self.setWindowIcon(QIcon("icono.png"))
			self.setLayout(contenedor)
		
	def setObserver(self,observer):
		self._observer=observer
		
	def informa(self):
		self._observer.update()

	def dibujarVidas(self,painter):
		vidas=QImage("vida","png")
		desplazamiento=0
		for i in range (self.jugador.getVidas()):
			painter.drawImage(QPoint(10+desplazamiento,10),vidas)
			desplazamiento+=55

	def deterHilos(self):
		pass
		
