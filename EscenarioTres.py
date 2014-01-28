from Escenario import *
from Jugador import*
import sys
import time
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore

class EscenarioTres(Escenario):

	def __init__(self,*args):
		Escenario.__init__(self,*args)
		self.mover=True #sirve para saber si el jugador se puede mover
		self.todoTrreno=True
		self._iniPendiente=500
		self._finPendiente=755
		self.piso1=430
		self.piso2=290
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
			if(self.todoTrreno and x>self._iniPendiente and x<self._finPendiente):
				self.jugador.avanzar()
				self.jugador.acender(2.65)
			elif x<=self._iniPendiente or x>=self._finPendiente:
				self.jugador.avanzar()
			self.repaint()
		if self.mover and e.key()==QtCore.Qt.Key_Left:
			self.jugador.retroceder()
			self.repaint()
		if self.mover and e.key()==QtCore.Qt.Key_X:
			if(self.jugador.getPosX()>=40 and self.jugador.getPosX()<=75):
				print "se abre el cofre"
			
	
if __name__=="__main__":
	app=QApplication(sys.argv)	
	escenario_Tres=EscenarioTres()
	escenario_Tres.show()
	sys.exit(app.exec_())
