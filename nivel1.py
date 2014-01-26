from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import *
from time import sleep
import sys
import math


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



class EscenarioUno(Escenario):

	def __init__(self,*args):
		Escenario.__init__(self,*args)
		self.theta=45
		self.hilop=HiloPuente(self)
		self.setWindowTitle("Escenario Uno")
		self.hilop.start()
		
	def paintEvent(self, event):       
		factRad= math.pi/180 #factor de conversion de grados a radianes
		corxPuente=250*math.cos(self.theta*factRad) #coordenada de la punta del puente
		coryPuente=250*math.sin(self.theta*factRad)
		paint = QPainter()
		paint.begin(self)
		paint.setRenderHint(QPainter.Antialiasing)
		imagen=QImage("esc1","png")
		center=QPoint(0,0)
		paint.drawImage(center,imagen)
		pen =QPen (Qt.blue, 10,Qt.SolidLine)
		paint.setPen(pen)
		paint.drawLine(650,520,650+corxPuente,520-coryPuente)
		paint.end()
	
	def setAngle(self,angulo):
		self.theta=angulo
		self.repaint()
        

class HiloPuente(Thread):
	#clase que sirve para descender el puente

	def __init__(self,Escenario):
		Thread.__init__(self)
		self.escenario=Escenario
	
	def run(self):
		angulo=45
		while True:
			angulo+=16.85
			if (angulo<=180):
				self.escenario.setAngle(angulo)
				sleep(0.5)
			else:
				break
			
		
		
		
app = QApplication(sys.argv)
nivel1 = EscenarioUno()
nivel1.setAngle(180)
nivel1.show()
app.exec_()