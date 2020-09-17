#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################

from enlace import *
import time


serialName = "COM2"                  


def main():
    try:
        
        com = enlace(serialName)

        com.enable()
    
        print("a comunicação foi aberta com sucesso")
        
        imageR="./imgs/imagem.jpg"

        print("carregando imagem para transmissão:")
        print(" - {}" .format(imageR))
        print("------------------------")

        txBuffer = open(imageR,'rb').read()  #rb=read byte


#lista do head
        head = bytes(10)

#Handshake
        payload0=bytes(114)
        fim = 'FIMM'
        EOP = end.encode() 
        package0 = head + payload0 + EOP
        print("fez o package0")

        com.sendData(package0)

#Fragmentando a imagem e separando em pacotes    
        tamanhoTx=int(len(txBuffer))
        npacotes = tamanhoTx//114
        if tamanhoTx % 114 == 0:
            q_pac=npacotes
            ultimo_payload = 114
        else:
            q_pac = npacotes+1
            ultimo_payload = (tamanhoTx % 114) 

        pacote_atual = 1
        pacotes_enviados = 0
        while pacote_atual <= npacotes:
            if pacote_atual == npacotes:
                pl = ultimo_payload
            else:
                pl = 114
            
            head[1]= q_pac #quantidade de pacotes
            head[2]=pacote_atual
            head[3]=pacotes_enviados+1
            head[4]=len(pacote_atual)

            

            ############
            ########
            pacote_atual+=1


        #tamanhoTx=0
        print("Tamanho da imagem: {}".format(tamanhoTx))
        
       # bytesTamanhoTx = (tamanhoTx).to_bytes(4, byteorder='big')############################################
       # print((int.from_bytes(bytesTamanhoTx,'big')))



        com.sendData(txBuffer)
        print("A transmissão de dados irá começar")


        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # Tente entender como esse método funciona e o que ele retorna
        time.sleep(2)  #intervalo pra dar tempo de terminar o envio
        txSize = com.tx.getStatus()  #O quanto de bytes foi enviado (tamanho de fato)
        #Se vc não tiver o tamanho que enviou, entra em loop infinito no enlaceRX getNData
        time.sleep(2)
        print("Tamanho enviado: {}".format(len(txBuffer)))
        
       
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.

        print("A recepção de dados irá começar agora")
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        txLen = len(txBuffer)  #Tamanho que deveria ter sido enviado
        rxBuffer, nRx = com.getData(txLen)  #função que confere o que enviou (tamanho)
    
    
        print ("recebeu {} bytes".format(len(rxBuffer)))

        #Salva imagem recebida no arquivo
        print("Salvando dados no arquivo")
        print("- {}".format(imageW))
        f = open(imageW,'wb')  #write byte
        f.write(rxBuffer)

        #fecha arquivo de imagem
        f.close()
    
        
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()
    except:
        print("ops! :-\\")
        com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
