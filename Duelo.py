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
		contenedor=QVBoxLayout()
		#self.aleatorio=random.choice(range(4))
		self.aleatorio=0
		self.setGeometry(50,50,self.dimension_x,self.dimension_y)
		self.setLayout(contenedor)
		self.jugador=jugador
		self.dificultad=self.jugador.getNivel()
		self.ancho=500
		self.anchopintado=498
		self.hilo=Barra(self)
		self.hilo.start()
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
		#self.crearImagenes(paint)
		paint.end()

	def crearImagenes(self,painter):
		if(self.jugador!=None):
			self.imagenes=[QImage("flecha_abajo","png"),QImage("flecha_arriba","png"),QImage("flecha_derecha","png"),QImage("flecha_izquierda","png")]
			imagen=self.imagenes[self.aleatorio]
			punto=QPoint(150,150)
			painter.drawImage(punto,imagen)

	def infoJugador(self,painter):
		if (self.jugador!=None):
			area=QRectF(250.0,100.0,50.0,25.0)
			text=self.jugador.getVidasString()
			painter.setPen (QColor (168, 34, 3))
			painter.setFont (QFont ('decorativo', 10))
			painter.drawText (area, Qt.AlignCenter, text)   
	
	def keyPressEvent(self,e):
		if e.key()==QtCore.Qt.Key_X:#si presiona x completa la prueba
			self.pruebasCompletadas+=1
			if (self.hilo!=None):
				if self.dificultad==1: #si completa la primera prueba jugador gano
					self.hilo.stop=True
					self.notificar()
					print "gano"
				elif self.dificultad==2: #sigue jugando
					#self.aleatorio=random.choice(range(4))#se genera otro aleatorio para generar otra imagen
					#self.aleatorio=2
					self.anchopintado=498
					if self.pruebasCompletadas==2:
						self.hilo.stop=True
						self.notificar()
						print "gano"
				elif self.dificultad==3:
					#self.aleatorio=random.choice(range(4))
					self.aleatorio=3
					self.anchopintado=498
					if self.pruebasCompletadas==3:
						self.hilo.stop=True
						self.notificar()
						print "gano"
	
	def notificar(self):
		#le cominuna al jugador que paso el nivel ....falta....
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
				self.duelo.repaint()
				if self.duelo.jugador.vidas==0:	
					self.duelo.anchopintado=0
					self.duelo.repaint()
					break
			else:
				self.duelo.anchopintado-=5
				self.duelo.repaint()
			sleep(0.1)
			
			if self.stop:
				break
		
				
if __name__=="__main__":
	app=QApplication(sys.argv)
	jugador=Jugador(40,500,Qt.white,5)
	jugador.setNivel(2)
	Ventana_Duelo=Duelo(jugador)
	sys.exit(app.exec_())
