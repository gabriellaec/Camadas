#####################################################
# Camada Física da Computação
#Gabriella
#Aplicação
####################################################

from enlace import *
import time

serialName = "COM1"  

def faz_pacote(payload, status):
    header =10*[0]
    eop = fim.encode() 
    eop=bytes([4])*4
    tamanhoPayload = len(payload)
    header[4]=(tamanhoPayload)
    if status == 'oi':
        header[0]=1
    elif status == 'ok':
        header[0]=2
    elif status == 'perdeu bytes':
        header[0]=3
    elif status == 'perdeu pacotes':
        header[0]=4
    header = bytes(header)
    pacote = header + (payload) + eop
    return pacote


def status_check(header):
    list(header)
    status = header[0]
    if status == 1 or status == 2:
        resposta = True
    else:
        resposta = False
    return resposta


def fragmenta_header(header):
    head=list(header)
    #print(head)
    status = head[0]
    quantidade_pacotes = head[1]
    pacote_atual = head[2]
    tamanho_pacote_atual = head[4]

    return int(status), int(quantidade_pacotes), int(pacote_atual), int(tamanho_pacote_atual)


def main():
    try:
        com2 = enlace(serialName)
        com2.enable()
        print("-"*30)
        print("A comunicação foi aberta com sucesso")
        print("-"*30)
        imageW="./imgs/recebidaCopia.png"

        print("-"*30)
        print("COMEÇANDO...")
        print("-"*30)

        print("-"*30)
        print("HANDSHAKE")
        print("-"*30)
        header, nRx = com2.getData(10)
        print("Pegou header do client")
        pacote, tamanho_pacote = com2.getData(int(header[4]))
        print("pegou dados do pacote do handshake")
        eop, tamanho_eop = com2.getData(4) 
        print("fez checagem do eop")

        print("Vai responder ao handshake")
        vivomsg=bytes([255])*4
        handshake = faz_pacote(vivomsg, 'oi')
        com2.sendData(handshake)
        print("Enviou o handshake")
        time.sleep(0.1)

        print("-"*30)
        print("FIM DO HANDSHAKE")
        print("-"*30)
        print("-"*30)

        print("COMEÇO TRANSMISSÃO DATAGRAMAS")
        print("Vai começar a pegar os pacotes")
        print("-"*30)
        header, nRx = com2.getData(10)
        pacote, tamanho_pacote = com2.getData(header[4])
        eop, tamanho_eop = com2.getData(4) 
        print("Pegou o primeiro pacote")
        numPacote = header[1]
        nPacoteInt= (int(numPacote))
        print("Quantidade total de pacotes: {}".format(nPacoteInt))
        pacAtual= header[2]
        pacAtualInt= int(pacAtual)
        print("Pacote atual: {}".format(pacAtualInt))
        imagem = bytes([])
        imagem+=pacote
        count = 0
        pacote_anterior=count
        print("-"*30)
        confirm_payload = bytes(8)
        confirm_pacote = faz_pacote(confirm_payload, 'ok')
        com2.sendData(confirm_pacote)
        print("Enviou confirmação de recebimento")

        jatentou=False
        while pacAtualInt < nPacoteInt-1:
            header, nRx = com2.getData(10)
            head=list(header)
            pacote, tamanho_pacote = com2.getData(head[4])
            eop, tamanho_eop = com2.getData(4) 
            status, quantidade_pacotes, pacote_atual, tamanho_pacote_atual = fragmenta_header(header)
            estado = 'ok'
            print("Pacote anterior: {}".format(pacote_anterior))
            print("Pacote atual: {}".format(pacote_atual))
            datagrama= header+pacote+eop
            eop_esperado=bytes([4])*4  

            tdokbytes=True
            tdoksize=True
            if eop != eop_esperado and estado=='ok':
                tdokbytes=False
                if not jatentou:
                    estado = 'perdeu bytes'
                    print("-"*30)
                    print("ERRO")
                    print("-"*30)
                    print("-"*30)
                    print("-"*30)
                    print('PERDEU BYTES!!!')
                    print("O tamanho do pacote não corresponde ao esperado")
                    print('Encerrando a comunicação')
                    print("Tente novamente")
                    print("-"*30)
                    confirm_pacote = faz_pacote(confirm_payload, estado)
                    com2.sendData(confirm_pacote)
                    print("Enviou mensagem requisitando recomeço do envio")
                    jatentou=True
                    com2.sendData(confirm_pacote)
                
                elif jatentou:
                    estado = 'perdeu bytes'
                    print("-"*30)
                    print("ERRO")
                    print("-"*30)
                    print("-"*30)
                    print("-"*30)
                    print('PERDEU BYTES!!!')
                    print("DEU RUIM")
                    print('Encerrando a comunicação')
                    print("Tente novamente")
                    print("-"*30)
                    confirm_pacote = faz_pacote(confirm_payload, estado)
                    com2.sendData(confirm_pacote)
                    print("Enviou mensagem requisitando recomeço do envio")
                    break
            else: 
                print('chegaram todos os bytes')


            if ( pacote_atual == pacote_anterior +1 ) and estado=='ok':
                print("Ordem está correta")
            elif ( pacote_atual != pacote_anterior +1 ) and not jatentou:
                tdoksize=False
                estado = 'perdeu pacotes'
                print("-"*30)
                print("ERRO")
                print("-"*30)
                print("-"*30)
                print("-"*30)
                print('PERDEU PACOTES!!!')
                print("A ordem dos pacotes não corresponde ao esperado")
                print('Encerrando a comunicação')
                print("Tente novamente")
                print("-"*30)
                print("-"*30)
                confirm_pacote = faz_pacote(confirm_payload, estado)
                com2.sendData(confirm_pacote)
                print("Enviou mensagem requisitando recomeço do envio")
                jatentou=True
                com2.sendData(confirm_pacote)
            
            elif ( pacote_atual != pacote_anterior +1 ) and jatentou:
                estado = 'perdeu pacotes'
                print("-"*30)
                print("ERRO")
                print("-"*30)
                print("-"*30)
                print("-"*30)
                print('PERDEU PACOTES!!!')
                print("A ordem dos pacotes não corresponde ao esperado")
                print('Encerrando a comunicação')
                print("DEU RUIM")
                print("-"*30)
                print("-"*30)
                confirm_pacote = faz_pacote(confirm_payload, estado)
                com2.sendData(confirm_pacote)
                
                break
                
          
            confirm_payload = bytes(8)
            confirm_pacote = faz_pacote(confirm_payload, estado)
            com2.sendData(confirm_pacote)
            print("Enviou confirmação de recebimento")
            ##################################################
            
            if tdoksize and tdokbytes:
                pacote_anterior = pacote_atual
                pacAtualInt = pacote_atual
                nPacoteInt= quantidade_pacotes
                count +=1
                imagem += pacote
                print("-"*30)

        print("saiu do loop")
        if pacote_atual+1 != quantidade_pacotes:
            print("Nem todos os pacotes chegaram")
        else:
            print("Chegaram todos os pacotes")

        print("-"*30)
        print("CONFIRMANDO TAMANHO")
        print("-"*30)

        print("-"*30)
        tamanho=int(len(imagem))
        print("Tamanho recebido: {}".format(tamanho))  
        print("Enviando tamanho recebido para o Client")  
        tamanho_bytes=(tamanho).to_bytes(4, byteorder="big")
        img_final=faz_pacote(tamanho_bytes, 'ok')
        com2.sendData(img_final)
        print("Salvando dados no arquivo")
        print("- {}".format(imageW))
        f = open(imageW,'wb')  #write byte
        f.write(img_final)

        f.close()
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com2.disable()
    except:
        print("ops! :-\\")
        com2.disable()

if __name__ == "__main__":
    main()
