import os, sys, random, msvcrt, time
from colorama import Fore, Style
#pip install colorama terminal
#Feito por Andrey Rigo e Fernando Aravites

debugMode = 0

def limpar(): 
    
    os.system('cls' if os.name == 'nt' else 'clear')

limpar()

def contarBombaVizinha(matriz, linha, coluna, ordem):
    
    bombas = 0

    # -1:-1 I -1:0 I -1:1
    # 0:-1  I 0:0  I 0:1
    # 1:-1  I 1:0  I 1:1
    # VAI DA CASA DE ANTES ATÉ A QUE VEM DEPOIS (TANTO VERTICAL, HORIZONTAL E NOS CANTOS)
    for i in range(-1, 2): #-1 é acima
        for j in range(-1,2): #-1 é esquerda

            if i == 0 and j == 0: continue # IGNORA O CENTRO
                
            novaLinha, novaColuna = linha + i, coluna + j # NOVAS POSIÇÕES PARA CHECAR SE TEM BOMBA
            
            if 0 <= novaLinha < ordem and 0 <= novaColuna < ordem: # LIMITA DENTRO DA ORDEM DA MATRIZ

                if matriz[novaLinha][novaColuna] == 1: bombas += 1

    return bombas # BOMBAS PRESENTES AO REDOR DA CASA ESCOLHIDA

def criarMatrizCampo(matrizOriginal, ordem): # MATRIZ QUE POSSUI TODAS AS INFORMAÇÕES DE JOGO

    matrizCampo = [[0 for _ in range(ordem)] for _ in range(ordem)] #CRIA UMA MATRIZ SÓ COM ZERO (TEMPORÁRIO)
    
    for i in range(ordem):
        for j in range(ordem):
            if matrizOriginal[i][j] == 1: matrizCampo[i][j] = 'B' # TROCA O VALOR 1 POR UM B ONDE TIVER BOMBA
            else: matrizCampo[i][j] = contarBombaVizinha(matrizOriginal, i, j, ordem) # TROCA PELO VALOR DE BOMBAS NA VIZINHANÇA (CASO NÃO TENHA BOMBA NA CASA ESPECIFICAMENTE)
    
    return matrizCampo

def escolherDificuldade(dificuldadeEntrada):

    match dificuldadeEntrada:
        case 1: return 5
        case 2: return 10
        case 3: return 15

def criarMatrizFalsa(ordem):

    return [['x' for coluna in range(ordem)] for linha in range(ordem)] # matriz falsa só com x

def coordenadasSagradas(linhaEscolha, colunaEscolha): #DEFINE POSIÇÕES ONDE NÃO PODE TER BOMBA

    posicoesSagradas = []

    # -1:-1 I -1:0 I -1:1
    # 0:-1  I 0:0  I 0:1
    # 1:-1  I 1:0  I 1:1
    # VAI DA CASA DE ANTES ATÉ A QUE VEM DEPOIS (TANTO VERTICAL, HORIZONTAL E NOS CANTOS)
    for i in range(-1, 2): # -1 é acima
        for j in range(-1,2): # -1 é esquerda
            coordenadas = (linhaEscolha + i, colunaEscolha + j)
            posicoesSagradas.append(coordenadas)

    return posicoesSagradas

def revelarCasasProximas(linhaEscolha, colunaEscolha, ordem, matrizCampo, matrizJogador, primeiraVez): #REVELA AS CASAS PRÓXIMAS QUE POSSUEM ZERO BOMBAS AO REDOR
    # -1:-1 I -1:0 I -1:1
    # 0:-1  I 0:0  I 0:1
    # 1:-1  I 1:0  I 1:1
    # VAI DA CASA DE ANTES ATÉ A QUE VEM DEPOIS (TANTO VERTICAL, HORIZONTAL E NOS CANTOS)
    for i in range(-1, 2): #-1 é acima
        for j in range(-1,2): #-1 é esquerda

            if i == 0 and j == 0: continue # IGNORA O CENTRO
                
            novaLinha, novaColuna = linhaEscolha + i, colunaEscolha + j
            
            if 0 <= novaLinha < ordem and 0 <= novaColuna < ordem:
                if i!=0 and j!=0: # checa os cantos
                    if (matrizCampo[linhaEscolha + i][colunaEscolha] == 0 or matrizCampo[linhaEscolha][colunaEscolha + j] == 0) and matrizCampo[linhaEscolha + i][colunaEscolha + j] == 0:
                        matrizJogador[novaLinha][novaColuna] = matrizCampo[novaLinha][novaColuna]
                elif matrizCampo[novaLinha][novaColuna] == 0: matrizJogador[novaLinha][novaColuna] = matrizCampo[novaLinha][novaColuna]

    
    if primeiraVez: # CHECAR UMA SEGUNDA CAMADA E SÓ REVELAR ONDE NÃO TEM BOMBA PARA FACILITAR O JOGO
        for i in range(-2, 3): #-2 é duas vezes acima
            for j in range(-2, 3): #-2 é duas vezes a esquerda

                if i == 0 and j == 0: continue # IGNORA O CENTRO
                
                novaLinha, novaColuna = linhaEscolha + i, colunaEscolha + j
            
                if 0 <= novaLinha < ordem and 0 <= novaColuna < ordem and matrizCampo[novaLinha][novaColuna] != "B": # CHECA SE TEM BOMBA, CASO SIM, NÃO REVELA

                    matrizJogador[novaLinha][novaColuna] = matrizCampo[novaLinha][novaColuna]

def imprimirMatrizColorida(matriz):

    for coluna in matriz:
        for elemento in coluna:
            
            match elemento:
                case 'B': print(Fore.RED + "B", end=" ")
                case 0: print(Fore.WHITE + str(elemento), end=" ")
                case 1: print(Fore.BLUE + str(elemento), end=" ")
                case 2: print(Fore.GREEN + str(elemento), end=" ")
                case 3: print(Fore.RED + str(elemento), end=" ")
                case 4: print(Fore.BLACK + str(elemento), end=" ")
                case 'x': print(Fore.WHITE + elemento, end=" ")
        print()

def tempoJogado(tempoInicio):

    tempoFinal = time.time() - tempoInicio #tempoFinal está em segundos

    minutos, segundos = int(tempoFinal // 60), int(tempoFinal % 60) # SEPARA O TEMPO TOTAL EM MINUTOS E SEGUNDOS

    if minutos <= 0: print(f"Tempo Registrado: {segundos} segundos.")
    else: print(f"Tempo Registrado: {minutos} minutos e {segundos} segundos.")


def main():

    ordem = 5

    print("=== SIGMA SWEEPER ===\n")

    print("Pressione Enter para continuar...", end="", flush=True)

    while True: # LIMPA O "Pressione Enter para continuar..."
        if msvcrt.getch() == b'\r':
            break

    limpar()

    dificuldadeEntradaPlayer = int(input("""Escolha a dificuldade:
1 - fácil (5 x 5)
2 - médio (10 x 10)
3 - difícil (15 x 15)
                                         
"""))
    ordem = escolherDificuldade(dificuldadeEntradaPlayer) # ordem da matriz quadrada do jogo

    limpar()

    debugMode = int(input("Ativar debug mode?\n0 - Não\n1 - Sim\n\n"))

    limpar()

    matrizFalsa = criarMatrizFalsa(ordem) #matriz falsa só com x

    imprimirMatrizColorida(matrizFalsa)

    linhaEscolha, colunaEscolha = map(int, input("Digite a posição para escolha (linha coluna): ").split()) # coordenada (x, y) escolhida
    linhaEscolha -= 1 # COMPUTADOR COMEÇA A CONTAGEM NO 0, QUEREMOS QUE SEJA NO 1 PARA FICAR MAIS INTUITÍVO
    colunaEscolha -= 1

    tempoInicio = time.time() # COMEÇA A CRONOMETRAR O TEMPO

    dificuldade = 2 * ordem #DIFICULDADE LIMITE

    matrizMapa = [[0 for coluna in range(ordem)] for linha in range(ordem)] # MATRIZ COM 0s ONDE ESTIVER LIVRE E 1s ONDE TIVER BOMBA

    quantidadeBombas = random.randint(dificuldade // 2, dificuldade + 1)

    posicoesSagradas = coordenadasSagradas(linhaEscolha, colunaEscolha) # LISTA COM COORDENADAS ONDE NÃO PODE TER BOMBA (ONDE O JOGADOR CLICA E NOS ARREDORES QUE SERÃO REVELADOS)

    quantidadeBombasAgora = quantidadeBombas # PRECISA EXISTIR O "AGORA", POIS POSTERIORMENTE A quantidadeBombas será utilizada para confirmar a win do player

    while quantidadeBombasAgora > 0:
        bombaLinha, bombaColuna = random.randint(0, ordem - 1 ), random.randint(0, ordem - 1) # ESCOLHE UM LUGAR ALEATÓRIO PARA A BOMBA
        coordenadaBomba = (bombaLinha, bombaColuna) # CRIA UMA COORDENADA PARA TAL LUGAR
        if coordenadaBomba not in posicoesSagradas: # TESTA SE O FORMATO COORDENADA DA BOMBA NÃO ESTÁ PRESENTE NA LISTA DE POSIÇÕES SAGRADAS
            matrizMapa[bombaLinha][bombaColuna] = 1 # COLOCA UMA BOMBA NO LUGAR 
            quantidadeBombasAgora-=1
    
    matrizCampo = criarMatrizCampo(matrizMapa, ordem) # MATRIZ QUE POSSUI TODAS AS INFORMAÇÕES DE JOGO
    matrizJogador = criarMatrizFalsa(ordem) # MATRIZ QUE SÓ O PLAYER VAI VER
    primeiraVez = 1 # IMPEDIR QUE ELE PERGUNTE NOVAMENTE AS POSIÇÕES
    
    while True:
        if not primeiraVez:
            linhaEscolha, colunaEscolha = map(int, input("Digite a posição para escolha: ").split())
            linhaEscolha -= 1
            colunaEscolha -= 1

        limpar()

        matrizJogador[linhaEscolha][colunaEscolha] = matrizCampo[linhaEscolha][colunaEscolha] # TROCA O X DA MATRIZ JOGADOR PELO VALOR QUE EXISTE NA matrizCampo

        revelarCasasProximas(linhaEscolha, colunaEscolha, ordem, matrizCampo, matrizJogador, primeiraVez) # FUNÇÃO QUE REVELA AS CASAS PRÓXIMAS DA ESCOLHIDA

        x_sobrando = 0 # VARIÁVEL QUE DEFINE O AVANÇO DO PLAYER NA PARTIDA (QUANTIDADE DE LUGARES NÃO DESCOBERTOS)
        for coluna in matrizJogador: # IMPRIMIR matrizJogador COM CORES INDICATIVAS
            for elemento in coluna:

                match elemento:
                    case 'B': print(Fore.RED + "BOOM!", end=" ")
                    case 0: print(Fore.WHITE + str(elemento), end=" ")
                    case 1: print(Fore.BLUE + str(elemento), end=" ")
                    case 2: print(Fore.GREEN + str(elemento), end=" ")
                    case 3: print(Fore.RED + str(elemento), end=" ")
                    case 4: print(Fore.BLACK + str(elemento), end=" ")
                    case 'x':
                        print(Fore.WHITE + elemento, end=" ")
                        x_sobrando += 1 # AUMENTA PARA CADA RETIRADA DE x
            print(Style.RESET_ALL) # TROCA A COR GERAL
            
        if debugMode:
            print("Debug matriz / x's sobrando:")
            imprimirMatrizColorida(matrizCampo) #FUNÇÃO GENÉRICA UTILIZADA PARA EVITAR LINHA DE CÓDIGO NO MEIO DO main()
            print(Style.RESET_ALL)
            print(x_sobrando)
        primeiraVez = 0

        if matrizCampo[linhaEscolha][colunaEscolha] == 'B': # CONDIÇÃO DE DERROTA -> ESCOLHEU POSIÇÃO COM BOMBA
            print()
            print(Fore.RED + "Você perdeu. Como a matriz era:")
            imprimirMatrizColorida(matrizCampo)
            break
        elif x_sobrando == quantidadeBombas: # CONDIÇÃO DE VITÓRIA -> LUGARES NÃO DESCOBERTOS = QUANTIDADE DE BOMBAS, OU SEJA, SABE O LOCAL DE TODAS AS BOMBAS
            print(Fore.GREEN + "Você ganhou yayyy :D", end=" ")
            break
    print()
    tempoJogado(tempoInicio) # MOSTRA O TEMPO QUE O JOGADOR DEMOROU PARA TERMINAR A PARTIDA (VITÓRIA OU DERROTA)

while True:

    if __name__ == "__main__":
        try: # TENTA RODAR O CÓDIGO NORMALMENTE (RESETANDO A FONTE)
            main()

            print(Style.RESET_ALL)

            resposta = input(
                "Gostaria de encerrar a partída? (digite 'sim')\n"
            ).lower()

            os.system("cls")

            if resposta == "sim": sys.exit()

        except: sys.exit() # ENCERRA O PROGRMA SE DER ERRO