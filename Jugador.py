#clase Jugador

class Jugador:

	def __init__(self,x,y,c,v):
		self._posX=x
		self._posY=y
		self._color=c
		self._velocidad=v
		self._radio=20
	
	def avanzar(self,v=None):
		if(v==None ):
			self._posX=self._posX+self._velocidad
		else:
			self._posX=self._posX+v
	def retroceder(self,v=None):
		if(v==None ):
			self._posX=self._posX-self._velocidad
		else:
			self._posX=self._posX-v
			
	def acender(self,v=None):
		if v==None:
			self._posY=self._posY-self._velocidad
		else:
			self._posY=self._posY-v
			
	def descender(self,v=None):
		if v==None:
			self._posY=self._posY+self._velocidad
		else:
			self._posY=self._posY+v
	
	def getPosX(self):
		return self._posX
	
	def getPosY(self):
		return self._posY
		
	def getColor(self):
		return self._color
	
	def getRadio(self):
		return self._radio
	
	def setPosX(self,x):
		self._posX=x
	
	def setPosY(self,y):
		self._posY=y
		
	def setColor(self,c):
		self._color=c
	
	def setRadio(self,r):
		self._radio=r
