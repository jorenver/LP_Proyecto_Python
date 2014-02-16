from Escenario import *
from Jugador import*
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import *
from time import sleep
from PyQt4 import QtCore
import sys
import math
import random

class Duelo(QWidget):
	dimension_x=600                                        
	dimension_y=600
	pruebasCompletadas=0
	
	def __init__(self,jugador,*args):
		QWidget.__init__(self,*args)
		self.imagenes=[QImage("accion","png"),QImage("flecha_derecha","png"),QImage("flecha_izquierda","png")]
		contenedor=QVBoxLayout()
		self.aleatorio=random.choice(range(3))
		self.setGeometry(50,50,self.dimension_x,self.dimension_y)
		self.setLayout(contenedor)
		self.jugador=jugador
		self.dificultad=self.jugador.getNivel()
		self.ancho=500
		self.anchopintado=498
		self.hilo=Barra(self)
		self.hilo.start()
		self.pintar=Pintar(self)
		self.pintar.start()
		self.setWindowTitle("Batalla")
		self.show()

	def setJugador(self,jugador):
		self.jugador=jugador
	
	def setDificultad(self,dif):
		self.dificultad=dif

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
		punto=QPoint(150,150)
		imagen=self.imagenes[self.aleatorio]
		paint.drawImage(punto,imagen)
		paint.end()

			

	def infoJugador(self,painter):
		if (self.jugador!=None):
			area=QRectF(250.0,100.0,50.0,25.0)
			text=self.jugador.getVidasString()
			painter.setPen (QColor (168, 34, 3))
			painter.setFont (QFont ('decorativo', 10))
			painter.drawText (area, Qt.AlignCenter, text)   
	
	def keyPressEvent(self,e):
		if e.key()==QtCore.Qt.Key_Right and self.aleatorio==1:
			self.anchopintado=498
			if (self.dificultad>1):
				self.aleatorio=random.choice(range(3))
				self.dificultad-=1
			else:
				self.hilo.stop=True
				self.pintar.stop=True
				print "gano"
				self.notificar()
		if e.key()==QtCore.Qt.Key_Left and self.aleatorio==2:
			self.anchopintado=498
			if (self.dificultad>1):
				self.aleatorio=random.choice(range(3))
				self.dificultad-=1
			else:
				self.hilo.stop=True
				self.pintar.stop=True
				print "gano"
				self.notificar()
		if e.key()==QtCore.Qt.Key_X and self.aleatorio==0:
			self.anchopintado=498
			if (self.dificultad>1):
				self.aleatorio=random.choice(range(3))
				self.dificultad-=1
			else:
				self.hilo.stop=True
				self.pintar.stop=True
				print "gano"
				self.notificar()
	
	
	
	def notificar(self):
		#le cominuna al jugador que paso el nivel 
		self.close()#cierra la ventana


class Barra(Thread):
	
	def __init__(self,duel):
		Thread.__init__(self)
		self.duelo=duel
		self.stop=False
		
	def run(self):
		while True:
			if self.duelo.anchopintado<=0:
				self.duelo.anchopintado=498
				self.duelo.jugador.disminuirVidas()
				if self.duelo.jugador.vidas==0:	
					self.duelo.anchopintado=0
					break
			else:
				self.duelo.anchopintado-=5
			sleep(0.1)
			if self.stop:
				break
			if self.duelo.jugador.getVidas()==0:
				print "pierde"
				break
				
				
class Pintar(Thread):
	def __init__(self,duel):
		Thread.__init__(self)
		self.duelo=duel
		self.stop=False
	def run(self):
		while(True):
			self.duelo.repaint()
			sleep(0.1)
			if self.stop:
				break
			if self.duelo.jugador.getVidas()==0:
				break
		
				
if __name__=="__main__":
	app=QApplication(sys.argv)
	jugador=Jugador(40,500,Qt.white,5)
	jugador.setNivel(2)
	Ventana_Duelo=Duelo(jugador)
	sys.exit(app.exec_())
