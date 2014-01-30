from Escenario import *
from Jugador import*
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import *
from time import sleep
from PyQt4 import QtCore
import sys
import math

class Duelo(QWidget):
	dimension_x=600                                        
	dimension_y=600
	
	def __init__(self,*args):
		QWidget.__init__(self,*args)
		contenedor=QVBoxLayout()
		self.setGeometry(50,50,self.dimension_x,self.dimension_y)
		self.setLayout(contenedor)
		self.jugador=None
		self.dificultad=None
		self.ancho=500
		self.anchopintado=498
		self.hilo=Barra(self)
		self.hilo.start()
		self.setWindowTitle("Batalla")
		self.show()
	
	def setJugador(self,jugador):
		self.jugador=jugador
		print self.jugador
	
	def setDificultad(self,dif):
		self.dificultad=dif
		print self.dificultad
		
	def paintEvent(self, event):       
		paint = QPainter()
		paint.begin(self)
		paint.setRenderHint(QPainter.Antialiasing)
		paint.setBrush(Qt.black) # cambiar el color
		paint.drawRect(50,50,self.ancho,30)
		paint.setBrush(Qt.white)
		paint.drawRect(51,51,self.ancho-2,28)
		paint.setBrush(Qt.red)
		paint.drawRect(51,51,self.anchopintado,28)
		paint.end()
	
	def keyPressEvent(self,e):
		if e.key()==QtCore.Qt.Key_X:
			print "gano"
	
		
class Barra(Thread):
	
	def __init__(self,duel):
		Thread.__init__(self)
		self.duelo=duel
		
	def run(self):
		while True:
			self.duelo.anchopintado-=5
			self.duelo.repaint()
			if(self.duelo.anchopintado<=0):
				print "perdio"
				break;
			sleep(0.1)
		


if __name__=="__main__":
	app=QApplication(sys.argv)	
	Ventana_Duelo=Duelo()
	Ventana_Duelo.setJugador(0)
	Ventana_Duelo.setDificultad(1)
	#Ventana_Duelo.show()
	sys.exit(app.exec_())


