from Escenario import *
from Jugador import*
import sys
import time
import threading
from Duelo import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore

class Accion:
	pasadizo=0
	caida=1
	salto=2
	teletransportacion=3

class EstadoEscenario:	
	pasadizoOff=0
	pasadizoOn=1	
	pisoTres=2


class EscenarioDos(Escenario):
	pisoUno=None
	pisoDos=None
	pisoTres=None
	nivel_piso_x=200 #separacion horizontal entre pisos
	nivel_piso_y=300 # altura de los pisos
	valor=0
	tam=0

	def __init__(self,jugador,*args): #constructor		
		Escenario.__init__(self,*args)
		self.mover=True
		self.jugador=jugador
		self.jugador.setPosY(Escenario.dimension_y-self.nivel_piso_y-50)
		self.jugador.setColor(QColor(0,0,155))	
		self.jugador.setRadio(50)
		self.jugador.setNivel(2)
		self.setWindowTitle("Escenario Dos")
		self.thread_pintarPasadizo=Hilo(self,Accion.pasadizo)
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
		paint.drawEllipse(self.jugador.getPosX(),self.jugador.getPosY(),self.jugador.getRadio(),self.jugador.getRadio())
		paint.setBrush(Qt.green)
		paint.drawRect(self.tam,Escenario.dimension_y-self.nivel_piso_y,self.thread_pintarPasadizo.valor_X,10)#rectangulo que se mueve
		paint.end()

	def dibujarPisos(self,painter):
		self.tam=125 #ancho del piso
		valor_X=0 
		valor_Y=0
		pisoUno=QRect(0,Escenario.dimension_y-self.nivel_piso_y,self.tam,self.nivel_piso_y)
		pisoDos=QRect(self.tam,Escenario.dimension_y-20,self.nivel_piso_x,20)
		pisoTres=QRect(self.tam+self.nivel_piso_x,Escenario.dimension_y-self.nivel_piso_y,2*self.tam,self.nivel_piso_y)#piso tres es dos veces mas grande que piso Uno
		pisoCuatro=QRect(3*self.tam+self.nivel_piso_x+self.nivel_piso_x,Escenario.dimension_y-self.nivel_piso_y,2*self.tam,self.nivel_piso_y)#piso cuatro es dos veces mas grande que piso Uno
		painter.setBrush(Qt.green)
		painter.drawRect(pisoUno)
		painter.drawRect(pisoDos)
		painter.drawRect(pisoTres)
		painter.drawRect(pisoCuatro)
		#cajas de habilidad
		painter.setBrush(Qt.red)
		painter.drawRect(self.tam,Escenario.dimension_y-20-20,30,20)
		painter.drawRect(self.tam+self.nivel_piso_x+2*self.tam-30,Escenario.dimension_y-self.nivel_piso_y-20,30,20)

	def keyPressEvent(self,e):
		if self.mover==True and e.key()==QtCore.Qt.Key_Right:
			
			if self.estadoEscenario==EstadoEscenario.pasadizoOff or self.estadoEscenario==EstadoEscenario.pisoTres:
				self.jugador.avanzar()	
			else:
				if self.jugador.getPosX()< (self.tam+self.nivel_piso_x)-50:
					self.jugador.avanzar()

			self.repaint()# se vuelve a pintar el circulo con las nuevas coordenadas
			
			if self.estadoEscenario==EstadoEscenario.pasadizoOff and self.jugador.getPosX()>self.tam-self.jugador.getRadio()/2: #si el pasadizo esta cerrado jugador se cae al piso dos
					self.my_thread=Hilo(self,Accion.caida)
					self.mover=False #Bloquea el movimiento
					self.my_thread.start()

		if self.mover==True and e.key()==QtCore.Qt.Key_Left:

			if self.estadoEscenario==EstadoEscenario.pasadizoOff or self.estadoEscenario==EstadoEscenario.pisoTres:
				self.jugador.retroceder()

			else:
				if self.jugador.getPosX()>self.tam:
					self.jugador.retroceder()

			self.repaint()	

		if self.jugador.getPosY()>Escenario.dimension_y-self.nivel_piso_y and self.jugador.getPosX()< self.tam+30 and e.key()==QtCore.Qt.Key_X:
			self.mover=False #bloquea el movimiento
			self.hilo=Hilo(self,Accion.teletransportacion)
			self.hilo.start()


		if self.jugador.getPosX()== self.tam+self.nivel_piso_x+2*self.tam-50 and e.key()==QtCore.Qt.Key_X:
			self.mover=False #bloquea el movimiento
			self.hilo=Hilo(self,Accion.salto)
			self.hilo.start()
		
		if self.jugador.getPosX()>3*self.tam+self.nivel_piso_x+self.nivel_piso_x:
			self.duelo=Duelo(self.jugador)


	def  activarPasadizo(self):
		self.mover==False #bloquea el movimiento
		self.thread_pintarPasadizo.start()


class Hilo(threading.Thread):

	def __init__(self,Escenario,accion):
		threading.Thread.__init__(self)
		self.escenarioDos=Escenario
		self.accion=accion #define el tipo de accion que se ejecutara
		self.valor_X=0
		self.valor_Y=0
		self.light=self.light=0

	def run(self):
		if self.accion==Accion.pasadizo:#pasadizo
			self.pintarPasadizo()
		elif self.accion==Accion.caida:# jugador se cae
			self.jugadorCaida()
		elif self.accion==Accion.salto: #jugador salta
			self.jugadorSaltar()
		elif self.accion==Accion.teletransportacion: # teletransportacion
			self.jugadorTeletransportacion()

	def pintarPasadizo(self):
		self.valor_X=0
		while True:
			self.valor_X=self.valor_X+20
			self.escenarioDos.repaint() #se ejecuta la funcion paint Event mientras el hilo este en ejecucion
			time.sleep(0.01)
			if(self.valor_X==self.escenarioDos.nivel_piso_x):
				self.escenarioDos.estadoEscenario=EstadoEscenario.pasadizoOn#el pasadizo se ha dibujado por completo y se cambia el estado del escenario
				self.escenarioDos.mover=True#el pasadizo se ha dibujado por completo entonces el jugador se puede mover
				break

	def jugadorCaida(self):
		self.valor_X=self.escenarioDos.jugador.getPosX()
		self.valor_Y=self.escenarioDos.jugador.getPosY()
		while True:
			self.valor_X=self.valor_X+20
			self.valor_Y=self.valor_Y+40
			self.escenarioDos.jugador.setPosX(self.valor_X)
			self.escenarioDos.jugador.setPosY(self.valor_Y)
			time.sleep(0.25)
			self.escenarioDos.repaint()
			if self.valor_Y>self.escenarioDos.dimension_y-80:
				self.escenarioDos.activarPasadizo()
				break

	def jugadorSaltar(self):
		tiempo=0.1
		posicionX=self.escenarioDos.jugador.getPosX()
		posicionY=self.escenarioDos.jugador.getPosY()
		flag=1
		while True:	
			if flag==1:
				posicionX=posicionX+20
				posicionY=posicionY-0.5*9.8*tiempo
				if posicionY<250:
					flag=0
			else:
				posicionX=posicionX+20
				posicionY=posicionY+0.5*9.8*tiempo
				if posicionY>=self.escenarioDos.dimension_y-self.escenarioDos.nivel_piso_y-50:
					posicionY=posicionY-5
					posicionX=posicionX-5
			self.escenarioDos.jugador.setPosX(posicionX)
			self.escenarioDos.jugador.setPosY(posicionY)
			self.escenarioDos.repaint()
			tiempo+=0.2
			if tiempo>3.3: 
				self.escenarioDos.mover=True
				break
			time.sleep(0.01)

	def jugadorTeletransportacion(self):
		dark=0
		light=0
		while True:
			if light<100:
				light=light+20
				color=QColor(0,0,155+light,255)
				self.escenarioDos.jugador.setColor(color)#cambiando el color en cada iteraccion # si color es mayor que un valor x se cambia la posicion del jugador a posDestino_X,PosDestion_Y
				self.escenarioDos.repaint()
				time.sleep(0.1)
			else:
				dark=dark+20
				color=QColor(0,0,255-dark,255)
				self.escenarioDos.jugador.setColor(color)
				self.escenarioDos.jugador.setPosX(self.escenarioDos.tam+self.escenarioDos.nivel_piso_x) 
				self.escenarioDos.jugador.setPosY(self.escenarioDos.dimension_y-self.escenarioDos.nivel_piso_y-self.escenarioDos.jugador.getRadio())
				self.escenarioDos.repaint()
				self.escenarioDos.estadoEscenario=EstadoEscenario.pisoTres
				time.sleep(0.1)
				if(dark>=100):
					self.escenarioDos.mover=True#jugador puede moverse
					break


if __name__=="__main__":
	app=QApplication(sys.argv)	
	jugador=Jugador(0,0,Qt.white,5)
	escenario_Dos=EscenarioDos(jugador)
	escenario_Dos.show()
	sys.exit(app.exec_())