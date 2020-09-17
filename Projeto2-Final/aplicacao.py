#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com = enlace(serialName)
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com.enable()
    
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("a comunicação foi aberta com sucesso")
        
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são uma lista de bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        imageR="./imgs/imagem.jpg"
        imageW="./imgs/recebidaCopia.png"

        print("carregando imagem para transmissão:")
        print(" - {}" .format(imageR))
        print("------------------------")

        txBuffer = open(imageR,'rb').read()  #rb=read byte
        #tx buffer com o dado da lista de bytes em que a imagem a ser enviada foi transformada
        #txBuffer = bytes(255)

        
    
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
        #print("quantidade de bytes sendo enviada: {}" .format(com.getBufferLen(txBuffer)))############################
    
            
        #finalmente vamos transmitir os dados. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!

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
