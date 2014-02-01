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
		self.setGeometry(100,100,self.dimension_x,self.dimension_y)
		self.setLayout(contenedor)
		self.jugador=None
		self.dificultad=None
		self.NivelObservador=None
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
		
	def setNivelObservador(self,Nivel):
		self.NivelObservador=Nivel
		
	def paintEvent(self, event):       
		paint = QPainter()
		paint.begin(self)
		paint.setRenderHint(QPainter.Antialiasing)
		paint.setBrush(Qt.white)
		paint.drawRect(event.rect())
		paint.setBrush(Qt.black) # cambiar el color
		paint.drawRect(50,50,self.ancho,30)
		paint.setBrush(Qt.white)
		paint.drawRect(51,51,self.ancho-2,28)
		paint.setBrush(Qt.red)
		paint.drawRect(51,51,self.anchopintado,28)
		self.infoJugador(paint)
		paint.end()
		
	def infoJugador(self,painter):
		if (self.jugador!=None):
			area=QRectF(100.0,50.0,200.0,150.0)
			text=self.jugador.getVidasString()
			painter.setPen (QColor (168, 34, 3))
			painter.setFont (QFont ('decorativo', 10))
			painter.drawText (area, Qt.AlignCenter, text)   		
		
	def reiniciar(self):
		if (self.jugador!=None):
			if(self.jugador.vidas!=1):
				self.anchopintado=498
				self.jugador.disminuirVidas()
				self.repaint()
				self.hilo=Barra(self)
				self.hilo.start()
			else:
				self.jugador.disminuirVidas()
				self.repaint()
				if self.NivelObservador!=None:
					self.NivelObservador.Perdio()
				self.close()
							
	
	def keyPressEvent(self,e):
		if e.key()==QtCore.Qt.Key_X:
			if (self.hilo!=None):
				self.hilo.stop=True
			if (self.NivelObservador!=None):
				self.NivelObservador.Gano()
			self.close()
	
		
class Barra(Thread):
	
	def __init__(self,duel):
		Thread.__init__(self)
		self.duelo=duel
		self.stop=False
		
	def run(self):
		while True:
			self.duelo.anchopintado-=5
			self.duelo.repaint()
			if (self.stop):
				break
			if(self.duelo.anchopintado<=0):
				self.duelo.reiniciar()
				break
			sleep(0.1)
		


if __name__=="__main__":
	app=QApplication(sys.argv)
	jugador=Jugador(40,500,Qt.white,5)
	Ventana_Duelo=Duelo()
	Ventana_Duelo.setJugador(jugador)
	Ventana_Duelo.setDificultad(1)
	#Ventana_Duelo.show()
	sys.exit(app.exec_())


