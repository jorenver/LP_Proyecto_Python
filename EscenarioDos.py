from Escenario import *
from Jugador import*
import sys
import time
import threading
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class EscenarioDos(Escenario):
	pisoUno=None
	pisoDos=None
	pisoTres=None
	nivel_piso_x=200 #separacion horizontal entre pisos
	nivel_piso_y=300 # altura de los pisos
	my_thread=None

	def __init__(self,*args,Jugador): #constructor		
		Escenario.__init__(self,*args)
		self.my_thread=Hilo(self,125,0)
		self.my_thread.start()
		self.jugador=Jugador
		self.setWindowTitle("Escenario Dos")

	def paintEvent(self, event):
		paint = QPainter()
		paint.begin(self)
		paint.setRenderHint(QPainter.Antialiasing)
		paint.setBrush(Qt.white) # cambiar el color
		paint.drawRect(event.rect())
		fondoEscenario=QImage("Fondo_Escenario_Dos","png")
		center=QPoint(0,0)
		paint.drawImage(center,fondoEscenario)
		self.dibujarPisos(paint)
		paint.end()

	def dibujarPisos(self,painter):
		tam=125 #ancho del piso
		valor_X=0 
		valor_Y=0
		painter.drawRect(self.my_thread.valor_X,self.my_thread.valor_Y,self.nivel_piso_x,10)#rectangulo que se mueve
		pisoUno=QRect(0,Escenario.dimension_y-self.nivel_piso_y,tam,self.nivel_piso_y)
		pisoDos=QRect(tam,Escenario.dimension_y-10,self.nivel_piso_x,10)
		pisoTres=QRect(tam+self.nivel_piso_x,Escenario.dimension_y-self.nivel_piso_y,2*tam,self.nivel_piso_y)#piso tres es dos veces mas grande que piso Uno
		pisoCuatro=QRect(3*tam+self.nivel_piso_x+self.nivel_piso_x,Escenario.dimension_y-self.nivel_piso_y,2*tam,self.nivel_piso_y)#piso cuatro es dos veces mas grande que piso Uno
		painter.setBrush(Qt.green)
		painter.drawRect(pisoUno)
		painter.drawRect(pisoDos)
		painter.drawRect(pisoTres)
		painter.drawRect(pisoCuatro)

	def jugar(self):


		
	
class Hilo(threading.Thread):

	def __init__(self,Escenario,valor_X,valor_Y):
		threading.Thread.__init__(self)
		self.escenarioDos=Escenario
		self.valor_X=valor_X
		self.valor_Y=valor_Y

	def run(self):
		while True:
			#self.valor_X=self.valor_X+10
			self.valor_Y=self.valor_Y+10
			self.escenarioDos.repaint() #se ejecuta la funcion paint Event mientras el hilo este en ejecucion
			time.sleep(1)
			if(self.valor_Y==self.escenarioDos.dimension_y-self.escenarioDos.nivel_piso_y-10):
				break




if __name__=="__main__":
	app=QApplication(sys.argv)	
	#hilo=Hilo(0,10)
	#hilo.start()
	escenario_Dos=EscenarioDos()
	escenario_Dos.show()
	sys.exit(app.exec_())