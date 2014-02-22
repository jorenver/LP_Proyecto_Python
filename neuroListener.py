# python version >= 2.5
import ctypes
import sys
import os
from ctypes import *
from numpy import *
import time
from ctypes.util import find_library
from threading import *
from pantallaPerdio import *
libEDK = cdll.LoadLibrary(".\\edk.dll")

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
write = sys.stdout.write
EE_EmoEngineEventCreate = libEDK.EE_EmoEngineEventCreate
EE_EmoEngineEventCreate.restype = c_void_p
eEvent      = EE_EmoEngineEventCreate()

EE_EmoEngineEventGetEmoState = libEDK.EE_EmoEngineEventGetEmoState
EE_EmoEngineEventGetEmoState.argtypes=[c_void_p,c_void_p]
EE_EmoEngineEventGetEmoState.restype = c_int

ES_GetTimeFromStart = libEDK.ES_GetTimeFromStart
ES_GetTimeFromStart.argtypes=[ctypes.c_void_p]
ES_GetTimeFromStart.restype = c_float

EE_EmoStateCreate = libEDK.EE_EmoStateCreate
EE_EmoStateCreate.restype = c_void_p
eState=EE_EmoStateCreate()

ES_GetWirelessSignalStatus=libEDK.ES_GetWirelessSignalStatus
ES_GetWirelessSignalStatus.restype = c_int
ES_GetWirelessSignalStatus.argtypes = [c_void_p]


ES_CognitivGetCurrentAction=libEDK.ES_CognitivGetCurrentAction
ES_CognitivGetCurrentAction.restype = c_int
ES_CognitivGetCurrentAction.argtypes= [c_void_p]

ES_CognitivGetCurrentActionPower=libEDK.ES_CognitivGetCurrentActionPower
ES_CognitivGetCurrentActionPower.restype = c_float
ES_CognitivGetCurrentActionPower.argtypes= [c_void_p]

userID            = c_uint(0)
user                    = pointer(userID)
#composerPort          = c_uint(1726)
#timestamp = c_float(0.0)
#option      = c_int(0)
state     = c_int(0)



    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------
class NeuroListener(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.stop=False
		
	def logEmoState(self,userID,eState):
		#print "Accion: ",ES_CognitivGetCurrentAction(eState),"\n"
		if(ES_CognitivGetCurrentAction(eState)==0x0020):
		   self.izquierda()
		if(ES_CognitivGetCurrentAction(eState)==0x0002):
		   self.accion()	   
		if(ES_CognitivGetCurrentAction(eState)==0x0040):
		   self.derecha()
		if(ES_CognitivGetCurrentAction(eState)==0x0001):
		   self.neutro()
		print "poder: ",ES_CognitivGetCurrentActionPower(eState),"\n"
	#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	def izquierda(self):
		print "izquierda\n"
		
	def derecha(self):
		print "derecha\n"
		
	def neutro(self):
		pass
		
	def accion(self):
		print "push\n"

	def conectar(self):
		if  libEDK.EE_EngineRemoteConnect("127.0.0.1",3008)!=0:
			eProfile  = libEDK.EE_ProfileEventCreate()
			libEDK.EE_GetBaseProfile(eProfile)
			libEDK.EE_GetUserProfile(userID, eProfile)
	
	def run(self):
		self.conectar()
		self.stop=False
		while (1):
			state = libEDK.EE_EngineGetNextEvent(eEvent)
			if state == 0:
				eventType = libEDK.EE_EmoEngineEventGetType(eEvent)
				libEDK.EE_EmoEngineEventGetUserId(eEvent, user)
				if eventType == 64:
					libEDK.EE_EmoEngineEventGetEmoState(eEvent,eState)
					self.logEmoState(userID,eState)   
			elif state != 0x0600:
				time.sleep(0.1)
			if self.stop==True:
				break
		self.desconectar()
		

	def desconectar(self):
		libEDK.EE_EngineDisconnect()
		libEDK.EE_EmoStateFree(eState)
		libEDK.EE_EmoEngineEventFree(eEvent)



