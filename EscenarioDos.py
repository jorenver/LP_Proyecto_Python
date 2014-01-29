from Escenario import *
from Jugador import*
import sys
import time
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore

class Acciones:
	pasadizo=0
	caida=1
	salto=2

class EstadoEscenario:	
	pasadizoOn=1
	pasadizoOff=0



class EscenarioDos(Escenario):
	pisoUno=None
	pisoDos=None
	pisoTres=None
	nivel_piso_x=200 #separacion horizontal entre pisos
	nivel_piso_y=300 # altura de los pisos
	valor=0
	tam=0

	def __init__(self,*args): #constructor		
		Escenario.__init__(self,*args)
		self.jugador=Jugador(0,Escenario.dimension_y-self.nivel_piso_y-50,Qt.blue,10)#posicion inicial del jugador
		self.setWindowTitle("Escenario Dos")
		self.thread_pintarPasadizo=Hilo(self,Acciones.pasadizo)
		self.estadoEscenario=EstadoEscenario.pasadizoOff

	def paintEvent(self, event):
		paint = QPainter()
		paint.begin(self)
		paint.setRenderHint(QPainter.Antialiasing)
		fondoEscenario=QImage("Fondo_Escenario_Dos","png")
		center=QPoint(0,0)
		paint.drawImage(center,fondoEscenario)
		self.dibujarPisos(paint)
		paint.setBrush(self.jugador.getColor())
		paint.drawEllipse(self.jugador.getPosX(),self.jugador.getPosY(), 50, 50)
		paint.setBrush(Qt.green)
		paint.drawRect(self.tam,Escenario.dimension_y-self.nivel_piso_y,self.thread_pintarPasadizo.valor_X,10)#rectangulo que se mueve
		paint.end()

	def dibujarPisos(self,painter):
		self.tam=125 #ancho del piso
		valor_X=0 
		valor_Y=0
		pisoUno=QRect(0,Escenario.dimension_y-self.nivel_piso_y,self.tam,self.nivel_piso_y)
		pisoDos=QRect(self.tam,Escenario.dimension_y-10,self.nivel_piso_x,10)
		pisoTres=QRect(self.tam+self.nivel_piso_x,Escenario.dimension_y-self.nivel_piso_y,2*self.tam,self.nivel_piso_y)#piso tres es dos veces mas grande que piso Uno
		pisoCuatro=QRect(3*self.tam+self.nivel_piso_x+self.nivel_piso_x,Escenario.dimension_y-self.nivel_piso_y,2*self.tam,self.nivel_piso_y)#piso cuatro es dos veces mas grande que piso Uno
		painter.setBrush(Qt.green)
		painter.drawRect(pisoUno)
		painter.drawRect(pisoDos)
		painter.drawRect(pisoTres)
		painter.drawRect(pisoCuatro)

	def keyPressEvent(self,e):
		if e.key()==QtCore.Qt.Key_Right:
			self.valor=self.valor+self.jugador.getVelocidad()
			self.jugador.setPosX(self.valor) #actualiza la posicion x del jugador cada vez que se presione una tecla
			self.repaint()# se vuelve a pintar el circulo con las nuevas coordenadas
			if self.valor>self.tam-10:  # si sale del piso Uno la pelota se cae al piso dos
				if self.estadoEscenario==EstadoEscenario.pasadizoOff :#si el pasadizo esta cerrado entonces la pelota debe caer
					self.my_thread=Hilo(self,Acciones.caida)
					self.my_thread.start()

		if e.key()==QtCore.Qt.Key_Left:
			self.valor=self.valor-self.jugador.getVelocidad()
			self.jugador.setPosX(self.valor)
			self.repaint()


				
	def  actualizar(self):
		self.thread_pintarPasadizo.start()


class Hilo(threading.Thread):

	def __init__(self,Escenario,accion):
		threading.Thread.__init__(self)
		self.escenarioDos=Escenario
		self.accion=accion #define el tipo de accion que se ejecutara
		self.valor_X=0
		self.valor_Y=0

	def run(self):
		if self.accion==0:#pasadizo
			self.pintarPasadizo()
		elif self.accion==1:
			self.jugadorCaida()
		elif self.accion==2:
			self.jugadorSaltar()

	def pintarPasadizo(self):
		self.valor_X=0
		while True:
			self.valor_X=self.valor_X+10
			self.escenarioDos.repaint() #se ejecuta la funcion paint Event mientras el hilo este en ejecucion
			time.sleep(0.5)
			if(self.valor_X==self.escenarioDos.nivel_piso_x):
				self.escenarioDos.estadoEscenario=EstadoEscenario.pasadizoOn#el pasadizo se ha dibujado por completo y se cambia el esta del escenario
				break

	def jugadorCaida(self):
		self.valor_X=self.escenarioDos.jugador.getPosX()
		self.valor_Y=self.escenarioDos.jugador.getPosY()
		while True:
			self.valor_X=self.valor_X+5
			self.valor_Y=self.valor_Y+20
			self.escenarioDos.jugador.setPosX(self.valor_X)
			self.escenarioDos.jugador.setPosY(self.valor_Y)
			self.escenarioDos.repaint()
			if self.valor_Y>self.escenarioDos.dimension_y-50-20:
				self.escenarioDos.actualizar()
				break

	def jugadorSaltar():
		pass	



if __name__=="__main__":
	app=QApplication(sys.argv)	
	#hilo=Hilo(0,10)
	#hilo.start()
	escenario_Dos=EscenarioDos()
	escenario_Dos.show()
	sys.exit(app.exec_())