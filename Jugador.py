#clase Jugador

class Jugador:

	def __init__(self,x,y,c,v):
		self._posX=x
		self._posY=y
		self._color=c
		self._velocidad=v
	
	def avanzar(self):
		self._posX=self._posX+self._velocidad
	
	def retroceder(self):
		self._posX=self._posX-self._velocidad
		
	def acender(self):
		self._posY=self._posY+self._velocidad
	
	def descender(self):
		self._posY=self._posY-self._velocidad
	
	