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
		self._iniPendiente=250
		self._medPendiente=520
		self._finPendiente=760
		self.jugador=Jugador(20,430,Qt.red,5)
		self.setWindowTitle("Escenario Tres")

		
	def paintEvent(self, event):       
		paint = QPainter()
		paint.begin(self)
		paint.setRenderHint(QPainter.Antialiasing)
		paint.setBrush(Qt.white) # cambiar el color
		paint.drawRect(event.rect())
		imagen=QImage("fondo3","jpg")
		center=QPoint(0,0)
		paint.drawImage(center,imagen)
		#paint.setBrush(self.jugador.getColo())
		center = QPoint(self.jugador.getPosX(), self.jugador.getPosY())
		paint.drawEllipse(center,self.jugador.getRadio(),self.jugador.getRadio())
		paint.end()
		
	#se define el movimiento de el jugador
	def keyPressEvent(self,e):
		if e.key()==QtCore.Qt.Key_Right:
			self.jugador.avanzar()
			self.repaint()
		if e.key()==QtCore.Qt.Key_Left:
			self.jugador.retroceder()
			self.repaint()
		if e.key()==QtCore.Qt.Key_X:
			if(self.jugador.getPosX()>200 and self.jugador.getPosX()<250):
				print "se abre el cofre"
			
	
if __name__=="__main__":
	app=QApplication(sys.argv)	
	escenario_Tres=EscenarioTres()
	escenario_Tres.show()
	sys.exit(app.exec_())
