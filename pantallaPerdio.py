from Escenario import *
from Jugador import*
from Duelo import *
from Observer import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
import sys
import math


class pantallaPerdio(Escenario):

	def __init__(self,*args):
		Escenario.__init__(self,*args)
		Bt_reiniciar=QPushButton("Volver a Jugar",self)
		Bt_reiniciar.setGeometry(340,400,200,65)
		self.connect(Bt_reiniciar, SIGNAL("clicked()"), self.nuevoJuego)
				
	def paintEvent(self, event):       
		paint = QPainter()
		paint.begin(self)
		imagen=QImage("gameover","png")
		center=QPoint(0,0)
		paint.drawImage(center,imagen) # inserto el fondo
		paint.end()
		
	def nuevoJuego(self):
		print "volver a jugar"
		
if __name__=="__main__":
	app=QApplication(sys.argv)	
	escenario=pantallaPerdio()
	escenario.show()
	sys.exit(app.exec_())