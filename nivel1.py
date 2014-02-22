from Escenario import *
from Jugador import*
from Duelo import *
from Observer import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from threading import *
from time import sleep
from PyQt4 import QtCore
import sys
import math
from pantallaPerdio import *

class EstadosPuente:
	"""
	Clase para especificar los estados del puente
	"""
	Subido=1
	Bajando=2
	Bajado=3


class EscenarioUno(Escenario):

	def __init__(self,jugador,observer,*args):
		Escenario.__init__(self,*args)
		self.theta=45   #angulo inicial del puente medido desde la horizontal en sentido contrario a las manecillas del reloj
		self.mover=True #bloque el movimiento del jugador
		self.ActivarPuente=False 
		self.flaqPalanca=False #mueve la palanca
		# hilos para el movimiento del puente y la caida del jugador
		self.hilop=HiloPuente(self) 
		self.hiloC=HiloCaida(self)
		# el puente inicializa como subido
		self.estadoPuente=EstadosPuente.Subido
		#creacion del jugador
		self.jugador=jugador
		self.jugador.setPosX(40)#se ubican al jugador en las posiciones correspondientes
		self.jugador.setPosY(500)
		self.jugador.setColor(Qt.white)
		self.jugador.setNivel(1)
		self.setWindowTitle("Escenario Uno")
		self.observer=observer
		self.p=pantallaPerdio()
		self.show()
		
	def paintEvent(self, event):       
		factRad= math.pi/180 #factor de conversion de grados a radianes
		corxPuente=250*math.cos(self.theta*factRad) #coordenada de la punta del puente
		coryPuente=250*math.sin(self.theta*factRad)
		paint = QPainter()
		paint.begin(self)
		paint.setRenderHint(QPainter.Antialiasing)
		imagen=QImage("Fondo_Escenario_Uno","png")
		center=QPoint(0,0)
		paint.drawImage(center,imagen) # inserto el fondo
		pen =QPen (Qt.red, 5,Qt.SolidLine)
		paint.setPen(pen)
		paint.drawLine(650,520,650+corxPuente,520-coryPuente) # dibuja el puente
		self.pintarPalanca(paint)
		if (self.jugador!=None):
			self.pintarJugador(paint)
		paint.end()
		
	def setJugador(self,jugador):
		self.jugador=jugador
		self.jugador.setNivel(1)
		self.repaint()
	
	def reiniciar(self):
		self.jugador.setPosX(40)
		self.jugador.setPosY(500)
		self.Perdio()
		self.repaint()
		self.mover=True
		
	
	
	def pintarJugador(self,painter):
		center=QPoint(self.jugador.getPosX(),self.jugador.getPosY())
		pen=QPen(Qt.blue,2,Qt.SolidLine)
		painter.setPen(pen)
		painter.setBrush(self.jugador.getColor())
		radio=self.jugador.getRadio()
		painter.drawEllipse(center,radio,radio)
	
	def pintarPalanca(self,painter):
		pen =QPen (Qt.red,5,Qt.SolidLine)
		painter.setPen(pen)
		if (self.flaqPalanca==False): # palanca desactivada
			painter.drawLine(270,520,295,476.7)
		else:
			painter.drawLine(270,520,245,476.7) # palanca activada

	
	def setAngle(self,angulo):
		self.theta=angulo
		self.repaint()
		
	def derecha(self):
		if self.mover :
			self.trasladarJugador()
			if self.mover:
				self.repaint()
	def izquierda(self):
		if self.jugador.getPosX()>20 and self.mover:
			self.jugador.retroceder()
			self.repaint()
	def accion(self):
		if self.mover:
			self.flaqPalanca=True
			self.repaint()
			self.bajarPuente()
		
	def keyPressEvent(self,e):
		if self.mover and e.key()==QtCore.Qt.Key_Right:
			self.trasladarJugador()
			if self.mover:
				self.repaint()
		
		elif self.jugador.getPosX()>20 and self.mover and e.key()==QtCore.Qt.Key_Left:
			self.jugador.retroceder()
			self.repaint()
		
		elif self.mover and e.key()==Qt.Key_X and self.ActivarPuente:
			self.flaqPalanca=True
			self.repaint()
			self.bajarPuente()
			
	def bajarPuente(self):
		if (self.estadoPuente==EstadosPuente.Subido):
			self.hilop.start()
			self.estadoPuente=EstadosPuente.Bajado
		
		
	def trasladarJugador(self):
		x=self.jugador.getPosX()
		# si la posicion X es mayor que 400 llega al abismo
		# ademas si el puente no esta bajado, el jugador caera
		if x>=400 and not self.estadoPuente==EstadosPuente.Bajado:
			self.mover=False
			# ejecuta el hilo de caida
			self.hiloC=HiloCaida(self)
			self.hiloC.start()
		elif x>=250 and x<=290:
			self.jugador.avanzar()
			self.ActivarPuente=True
		elif not (x>=250 and x<=290):
			self.ActivarPuente=False
			self.jugador.avanzar()
			if (x>=825):
				self.mover=False
				self.close()
				self.observer.update2()
		else:
			self.jugador.avanzar()
			
	def Perdio(self):
		if (self.jugador.vidas==0):
			print("perdiste")
			self.mover=False
			self.close()
			self.observer.perder()
	
	
	def Gano(self):
		print "Ganaste!!!"
		
	def detenerHilos(self):
		pass
		
		
			
class HiloPuente(Thread):
	#clase que sirve para descender el puente

	def __init__(self,Escenario):
		Thread.__init__(self)
		self.escenario=Escenario
	
	def run(self):
		angulo=45
		self.escenario.estadoPuente=EstadosPuente.Bajando
		self.escenario.mover=False
		while True:
			angulo+=16.85
			if (angulo<=180):
				self.escenario.setAngle(angulo)
				sleep(0.5)
			else:
				self.escenario.mover=True
				self.escenario.estadoPuente=EstadosPuente.Bajado
				break
						
class HiloCaida(Thread):
	
	def __init__(self,esc):
		Thread.__init__(self)
		self.escenario=esc
		
	def run(self):
		self.escenario.mover=False
		yo= self.escenario.jugador.getPosY()
		xo= self.escenario.jugador.getPosX()
		y=0
		t=0
		while True:
			if (y<=690):
				xo=xo+15
				y=yo+9.8*t
				t+=4
				self.escenario.jugador.setPosY(y)
				self.escenario.jugador.setPosX(xo)
				self.escenario.repaint()
				sleep(0.25)
			else:
				if (self.escenario.jugador.vidas!=0):
					self.escenario.jugador.disminuirVidas()
				print ("ha perdido")
				break
		self.escenario.reiniciar()


'''
if __name__=="__main__":
	app=QApplication(sys.argv)	
	jugador=Jugador(0,0,Qt.white,5)
	escenario=EscenarioUno(jugador)
	escenario.show()
	sys.exit(app.exec_())
'''