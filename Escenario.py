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
			self.setLayout(contenedor)
		
	def setObserver(self,observer):
		self._observer=observer
		
	def informa(self):
		self._observer.update()
		