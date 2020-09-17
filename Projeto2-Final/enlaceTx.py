#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Threads
import threading

# Class
class TX(object):
 
    def __init__(self, fisica):
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.transLen    = 0
        self.empty       = True
        self.threadMutex = False
        self.threadStop  = False


    def thread(self):  #fica acontecendo constantemente fora do SW
        while not self.threadStop:
            if(self.threadMutex):
                self.transLen    = self.fisica.write(self.buffer)  #Manda o que tá na variável Buffer (compartilhada com o SW) pro chip
                self.threadMutex = False

    def threadStart(self):  #inicia uma tarefa desvinculada do SW
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        self.threadStop = True

    def threadPause(self):
        self.threadMutex = False

    def threadResume(self):
        self.threadMutex = True

    def sendBuffer(self, data):
        self.transLen   = 0
        self.buffer = data
        self.threadMutex  = True  #Quando é true envia o que tá no buffer

    def getBufferLen(self):
        return(len(self.buffer))

    def getStatus(self):
        return(self.transLen)
        

    def getIsBussy(self):
        return(self.threadMutex)

