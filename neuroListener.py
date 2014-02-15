# python version >= 2.5
import ctypes
import sys
import os
from ctypes import *
from numpy import *
import time
from ctypes.util import find_library
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
composerPort          = c_uint(1726)
timestamp = c_float(0.0)
option      = c_int(0)
state     = c_int(0)


    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------

def logEmoState(userID,eState):
    print "informacion\n"
    #print ES_GetTimeFromStart(eState),",",            
    print "id Usuario: ",userID.value,"\n",
    #print ES_GetWirelessSignalStatus(eState),",",
    #Cognitiv Suite results
    print "\t\tAccion Current\n"
    print "Accion: ",ES_CognitivGetCurrentAction(eState),"\n"
    if(ES_CognitivGetCurrentAction(eState)==0x0020):
       izquierda()
    if(ES_CognitivGetCurrentAction(eState)==0x0002):
       push()	   
    if(ES_CognitivGetCurrentAction(eState)==0x0040):
       derecha()
    if(ES_CognitivGetCurrentAction(eState)==0x0001):
       neutro()
    print ES_CognitivGetCurrentActionPower(eState)
    print "poder: ",ES_CognitivGetCurrentActionPower(eState),"\n"
    print '\n'
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def izquierda():
	print "izquierda\n"
	
def derecha():
	print "derecha\n"
	
def neutro():
	print "neutral\n"
	
def push():
	print "push\n"




#------------------------------------------------------------------------------------------------------------------------------------------------------------
print "Comienza"

#if libEDK.EE_EngineConnect("Emotiv Systems-5") != 0:
if  libEDK.EE_EngineRemoteConnect("127.0.0.1",3008)!=0:
	print "Emotiv Engine start up failed."
	eProfile  = libEDK.EE_ProfileEventCreate()
	libEDK.EE_GetBaseProfile(eProfile)
	libEDK.EE_GetUserProfile(userID, eProfile)
else:
	print "else else else"
    
while (1):
    state = libEDK.EE_EngineGetNextEvent(eEvent)
    #print "entre al while"
    if state == 0:
        #print "*********"
        eventType = libEDK.EE_EmoEngineEventGetType(eEvent)
        libEDK.EE_EmoEngineEventGetUserId(eEvent, user)
        if eventType == 64: #libEDK.EE_Event_enum.EE_EmoStateUpdated
            libEDK.EE_EmoEngineEventGetEmoState(eEvent,eState)
            timestamp = ES_GetTimeFromStart(eState)
            print "%10.3f New EmoState from user %d ...\r" %(timestamp,userID.value)
            logEmoState(userID,eState)   
    elif state != 0x0600:
        print "Internal error in Emotiv Engine ! "
        time.sleep(0.1)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
desconectar()


def desconectar():
	libEDK.EE_EngineDisconnect()
	libEDK.EE_EmoStateFree(eState)
	libEDK.EE_EmoEngineEventFree(eEvent)






