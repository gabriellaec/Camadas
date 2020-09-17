#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#####################################################
#Carareto
#17/02/2018
####################################################

# Importa pacote de comunicação serial
import serial

# importa pacote para conversão binário ascii
import binascii

#################################
# Interface com a camada física #
#################################
class fisica(object):
    def __init__(self, name):
        self.name        = name
        self.port        = None  #porta de comunicação
        #self.baudrate    = 115200
        self.baudrate    = 9600
        self.bytesize    = serial.EIGHTBITS #um byte
        self.parity      = serial.PARITY_NONE  #nao usa
        self.stop        = serial.STOPBITS_ONE  #usa um só
        self.timeout     = 0.1  
        self.rxRemain    = b""
        #start bit não precisa configurar pq é obrigatório

    def open(self):  #inicia a porta e faz a comunicação com o que foi configurado acima
        self.port = serial.Serial(self.name,
                                  self.baudrate,
                                  self.bytesize,
                                  self.parity,
                                  self.stop,
                                  self.timeout)


    def close(self):  #função para fechar a porta
        self.port.close()

    def flush(self):
        self.port.flushInput()
        self.port.flushOutput()

    def encode(self, data):  #transforma bin em hexa
        encoded = binascii.hexlify(data)
        return(encoded)

    def decode(self, data):
        """ RX ASCII data after reception
        """
        decoded = binascii.unhexlify(data)
        return(decoded)

    def write(self, txBuffer):
        """ Write data to serial port

        This command takes a buffer and format
        it before transmit. This is necessary
        because the pyserial and arduino uses
        Software flow control between both
        sides of communication.
        """
        nTx = self.port.write(self.encode(txBuffer))
        self.port.flush()
        return(nTx/2)

    def read(self, nBytes):  #função pra ler o que chega para passar pro Rx
        """ Read nBytes from the UART com port

        Nem toda a leitura retorna múltiplo de 2
        devemos verificar isso para evitar que a funcao
        self.decode seja chamada com números ímpares.
        """
        rxBuffer = self.port.read(nBytes)
        rxBufferConcat = self.rxRemain + rxBuffer
        nValid = (len(rxBufferConcat)//2)*2
        rxBufferValid = rxBufferConcat[0:nValid]
        self.rxRemain = rxBufferConcat[nValid:]
        try :
            """ As vezes acontece erros na decodificacao
            fora do ambiente linux, isso tenta corrigir
            em parte esses erros. Melhorar futuramente."""
            "muitas vezes um flush no inicio resolve!"
            rxBufferDecoded = self.decode(rxBufferValid)
            nRx = len(rxBuffer)
            return(rxBufferDecoded, nRx)
        except :
            print("[ERRO] interfaceFisica, read, decode. buffer : {}".format(rxBufferValid))
            return(b"", 0)

