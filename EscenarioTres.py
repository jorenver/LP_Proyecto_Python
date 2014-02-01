from Escenario import *
from Jugador import*
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import *
from time import sleep
from PyQt4 import QtCore
import sys
import math
from Duelo import *

class EscenarioTres(Escenario):

	def __init__(self,*args):
		Escenario.__init__(self,*args)
		self.mover=True #sirve para saber si el jugador se puede mover
		self.todoTerreno=False
		self._iniPendiente=500
		self._finPendiente=755
		self.hiloCaida=None
		self.hiloSalto=None
		self.piso1=430
		self.piso2=290
		self.Duelo=None
		self.jugador=Jugador(20,430,Qt.white,5)
		self.setWindowTitle("Escenario Tres")

	def dibujarCofres(self,paint):
		paint.setBrush(Qt.red)
		paint.drawRect(40,413,35,35)
		paint.drawRect(370,413,35,35)
		
	def paintEvent(self, event):       
		paint = QPainter()
		paint.begin(self)
		paint.setRenderHint(QPainter.Antialiasing)
		paint.setBrush(Qt.white) # cambiar el color
		paint.drawRect(event.rect())
		imagen=QImage("fondo3","jpg")
		center=QPoint(0,0)
		paint.drawImage(center,imagen)
		self.dibujarCofres(paint)
		paint.setBrush(self.jugador.getColor())
		center = QPoint(self.jugador.getPosX(), self.jugador.getPosY())
		paint.drawEllipse(center,self.jugador.getRadio(),self.jugador.getRadio())
		paint.end()
		
	
		
		
	#se define el movimiento de el jugador
	def keyPressEvent(self,e):
		if self.mover and e.key()==QtCore.Qt.Key_Right:
			x=self.jugador.getPosX()
			if (x>= 850) :
				self.mover = False
				self.Duelo=Duelo(self.jugador)
			elif(self.todoTerreno and x>self._iniPendiente and x<self._finPendiente):
				self.jugador.avanzar()
				self.jugador.acender(2.65)
			elif x<=self._iniPendiente or x>=self._finPendiente:
				self.jugador.avanzar()
			
			if x>=100 and x<=200:
				self.hiloCaida=HiloCaida(self,1)
				self.hiloCaida.start()
			else:
				self.repaint()
		if self.mover and e.key()==QtCore.Qt.Key_Left:
			x=self.jugador.getPosX()
			if(x>self._iniPendiente and x<self._finPendiente):
				self.jugador.retroceder()
				self.jugador.descender(2.65)
			elif x<=self._iniPendiente or x>=self._finPendiente:
				self.jugador.retroceder()
			if x>=200 and x<=300:
				self.hiloCaida=HiloCaida(self,-1)
				self.hiloCaida.start()
			else:
				self.repaint()
		if self.mover and e.key()==QtCore.Qt.Key_X:
			if(self.jugador.getPosX()>=40 and self.jugador.getPosX()<=75):
				self.hiloSalto=HiloSalto(self)
				self.hiloSalto.start()
			if(self.jugador.getPosX()>=370 and self.jugador.getPosX()<=420):
				self.todoTerreno=True
				self.jugador.setColor(Qt.black)
				self.repaint()
class HiloCaida(Thread):
	
	def __init__(self,esc,dir):
		Thread.__init__(self)
		self.dir=dir
		self.escenario=esc
		
	def run(self):
		self.escenario.mover=False
		yo= self.escenario.jugador.getPosY()
		xo= self.escenario.jugador.getPosX()
		y=0
		t=0
		while True:
			if (y<=690):
				xo=xo+15*(self.dir)
				y=yo+9.8*t
				t+=4
				self.escenario.jugador.setPosY(y)
				self.escenario.jugador.setPosX(xo)
				self.escenario.repaint()
				sleep(0.25)
			else:
				if(self.escenario.jugador.getVidas()==1):
					print "perdio"
				else:
					self.escenario.jugador.disminuirVidas()
					self.escenario.jugador.setPosX(20)
					self.escenario.jugador.setPosY(430)
					self.escenario.repaint()
					self.escenario.mover=True
				break
	
class HiloSalto(Thread):
	
	def __init__(self,esc):
		Thread.__init__(self)
		self.escenario=esc
		
	def run(self):
		self.escenario.mover=False
		yo= self.escenario.jugador.getPosY()
		xo= self.escenario.jugador.getPosX()
		y=self.escenario.jugador.getPosY()
		#y=0
		while True:
			if (xo<=205):
				yo=yo-9.8
			elif (yo<y):
				yo=yo+9.8
			else:
				self.escenario.mover=True
				break
			xo=xo+30
			self.escenario.jugador.setPosY(yo)
			self.escenario.jugador.setPosX(xo)
			self.escenario.repaint()
			print yo ," ", y
			sleep(0.25)

	
if __name__=="__main__":
	app=QApplication(sys.argv)	
	escenario_Tres=EscenarioTres()
	escenario_Tres.show()
	sys.exit(app.exec_())
