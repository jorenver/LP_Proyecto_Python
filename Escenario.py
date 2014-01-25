#clase escenario
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Escenario(QWidget):
	def __init__(self, *args): 
		QWidget.__init__(self, *args)
        contenedor = QVBoxLayout()
        self.setLayout(contenedor)
		
	def setObserver(self,observer):
		self._observer=observer
		
	def iforma(self):
		self._observer.update()
		
		