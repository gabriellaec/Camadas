#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################

from enlace import *
import time
import threading 

serialName = "COM2"             

def define_pacotes(tamanhoTx, payload_total):   #retorna uma lista com os payloads
    npacotes = tamanhoTx//114
    if tamanhoTx % 114 == 0:
        q_pac=npacotes
        ultimo_payload = 114
    else:
        q_pac = npacotes+1
        ultimo_payload = (tamanhoTx % 114) 

    p=bytes([])
    lista_payloads=[]

    pacote_atual = 1
    while pacote_atual <= q_pac:
        if pacote_atual == npacotes+1:
            tamanho_payload = ultimo_payload
        else:
            tamanho_payload = 114
        for i in range (0,tamanho_payload):
            p += bytes([payload_total[i]])
        
        lista_payloads.append(p)
        pacote_atual+=1
        p=bytes([])
    print("Tamanho da lista payloads {}".format(len(lista_payloads)))

    return lista_payloads



def cria_pacotes(lista_payloads):   #retorna os pacotes prontos
        header = [0]*10
        eop = bytes([4])*4
        tamanho_msg=int(len(lista_payloads))
        #print("tamanho msg: {}".format(tamanho_msg))
        quantPac= (tamanho_msg) #quantidade de pacotes
        header[1]=quantPac
        pacotes = []
        for i in range(0, tamanho_msg):
            header[2]=(i)   #numero do pacote

            ############################################################teste qnd da ruim nos pacotes
            # print("-"*30)
            # print("*******  SIMULAÇÃO COM ERRO NO NÚMERO DO PACOTE  *******")
            # print("-"*30)
            # if i == 2:
            #    header[2]=4 
            ###################################################################SIMULAÇÃO COM TUDO CERTO
            tamanho_p=len(lista_payloads[i])
            header[4]=(tamanho_p)   #114

           ############################################################teste qnd da ruim nos bytes
            # print("-"*30)
            # print("*******  SIMULAÇÃO COM ERRO NO TAMANHO DO PACOTE  *******")
            # print("-"*30)
            # if i == 2:
            #      header[4]=4
            #      header[2]=2
            #      print(list(header))
            # else:
            #      tamanho_p=len(lista_payloads[i])
            #      header[4]=(tamanho_p)   #114
            ###################################################################

            head = bytes(header)
            pacote=bytes(header) + lista_payloads[i] + eop
            print("Criou pacote de tamanho {}".format(len(pacote)))
            tamanho_p=0
            pacotes.append(pacote)
         
        print("-"*30)

        header[2]=bytes([0])
        header[4]=bytes([114])
        return pacotes, head, eop
    
def handshake(com):
    eop = bytes([4])*4
    msg=bytes([255])*3
    header=[0]*10
    header[4]=3
    header=bytes(header)
    check = bytes(header)+msg+(eop)
    ok=False
    dt=0
    tentativa = 0
    com.sendData(check)
    t0=time.time()
    esperou=False

    while not ok:

        print("Enviou handshake")
        while not esperou:
            header, n = com.getDataHandshake(10)
            nint=int.from_bytes(header, byteorder='big')
            print("Pegou dados do server")
            
            if nint ==0:
                retry=input("Servidor inativo. Tentar novamente? S/N: ")
                if retry == "n" or retry =="N":
                    ok=False
                    esperou=True
                    print("-------------------------")
                    print("Comunicação encerrada")
                    print("-------------------------")
                    com.disable()
                    
                elif retry == "s" or retry =="S":
                    time.sleep(1)
                    header=0
                    n=0
                    com.sendData(check)
            
            else:
                esperou=True

       
        head = list(header)
        pacote, tamanho_pacote = com.getData(head[4])
        print("Pegou payload")
        eop, tamanho_eop = com.getData(4) 
        print("Recebeu resposta do Handshake")
    
        if head[0]==1 or head[0]==2:
            ok = True
               
        tentativa+=1
    print("Handshake funconou!! Vamos começar =)")





def status_check(header):
    head=list(header)
    status = int(head[0])
    if status == 1 or status == 2:
        resposta = True
    else:
        resposta = False
    return resposta



def main():
    try:
        
        com = enlace(serialName)

        com.enable()
        print("A comunicação foi aberta com sucesso")
        print("-"*30)
        print("COMEÇANDO...")
        print("-"*30)

        txBuffer = bytes(500)

        imageR="./imgs/imagem.jpg"
        imageW="./imgs/recebidaCopia.png"

        print("carregando imagem para transmissão:")
        print(" - {}" .format(imageR))
        print("------------------------")

        txBuffer = open(imageR,'rb').read() 

        tamanhoTx=int(len(txBuffer))
        print("Tamanho da imagem: {}".format(tamanhoTx))

        print("-"*30)
        print("CRIANDO PACOTES")
        print("-"*30)

        lista_payloads = define_pacotes(tamanhoTx, txBuffer)
        print("Criou a lista com {} payloads". format(len(lista_payloads)))

        time.sleep(0.1)
        pacotes,header,eop = cria_pacotes(lista_payloads)
        print("Criou os pacotes")

        print("-"*30)
        print("HANDSHAKE")
        print("-"*30)
        handshake(com)
        
        
        print("-"*30)
        print("FIM DO HANDSHAKE")
        print("-"*30)
        print("-"*30)

        print("COMEÇO TRANSMISSÃO DATAGRAMAS")
        print("Vai começar a pegar os pacotes")
        print("-"*30)


        count = 0
        jatentou=False
        while count < len(pacotes):
            p=pacotes[count]
            #print(list(p))
            print("Tamanho do pacote: {}".format(len(p)))
            com.sendData(p)
            print("Enviou pacote {}" . format(count))
            time.sleep(0.1)


            header, nRx = com.getData(10)
            head=list(header)
            pacote, tamanho_pacote = com.getData(head[4])
            eop, tamanho_eop = com.getData(4) 

            print("Pegando a confirmação de recebimento do server")
            time.sleep(0.1)
            print("-"*30)
            count+=1
            if not status_check(header) and count >1:
                if jatentou:
                    print("ALGO DEU ERRADO!!!")
                    print("Não deu certo enviar o pacote novamente")
                    print("Reinicie a aplicação")
                    break
                else:
                    print("ALGO DEU ERRADO!!!")
                    print("Enviando pacote novamente...")
                    jatentou=True
                    count-=1
           
        time.sleep(1)
        header , nRx = com.getData(10)
        head=list(header)
        pacote, tamanho_pacote = com.getData(head[4])
        eop, tamanho_eop = com.getData(4) 
        tamanho_recebido = int.from_bytes(pacote, byteorder='big')
      
        print("-"*30)
        print("CONFERINDO SE IMAGEM CHEGOU INTEIRA")
        print("-"*30)

        if int(tamanho_recebido) == tamanhoTx:
            print("Todos os bytes chegaram!")
            print(f"Recebido: {tamanho_recebido} e Enviado: {tamanhoTx}")
        else:
            print("Imagem não chegou inteira")
            print(f"Recebido: {tamanho_recebido} e Enviado: {tamanhoTx}")

        print("-"*30)

        print("-"*30)

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com.disable()
    except:
        print("ops! :-\\")
        com.disable()

if __name__ == "__main__":
    main()
