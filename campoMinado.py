import os
import math
import sys
import random
from colorama import Fore, Back, Style, init
#pip install colorama terminal

debug_mode=1

def limpar():

    os.system('cls' if os.name == 'nt' else 'clear')

limpar()

def contarBombaVizinha(matriz, linha, coluna, ordem):
    
    bombas = 0

    for i in range(-1, 2): # VAI DA CASA DE ANTES ATÉ A QUE VEM DEPOIS
        for j in range(-1,2):

            if i == 0 and j == 0: continue # IGNORA O CENTRO
                
            novaLinha, novaColuna = linha + i, coluna + j
            
            if 0 <= novaLinha < ordem and 0 <= novaColuna < ordem:

                if matriz[novaLinha][novaColuna] == 1: bombas += 1

    return bombas

def criarMatrizCampo(matrizOriginal, ordem):
    matrizCampo = [[0 for _ in range(ordem)] for _ in range(ordem)]
    
    for i in range(ordem):
        for j in range(ordem):
            if matrizOriginal[i][j] == 1: matrizCampo[i][j] = 'B'
            else: matrizCampo[i][j] = contarBombaVizinha(matrizOriginal, i, j, ordem)
    
    return matrizCampo

def main():
    #perguntar a ordem
    ordem = 4
    matrizFalsa = [['x' for coluna in range(ordem)] for linha in range(ordem)] #matriz falsa só com x
    for coluna in matrizFalsa:
        for elemento in coluna:
            print(elemento, end=" ")
        print()
    linhaEscolha, colunaEscolha = map(int, input("Digite a posição para escolha (linha coluna): ").split())
    linhaEscolha -= 1
    colunaEscolha -= 1

    dificuldade = 2 * ordem
    matrizMapa = [[0 for coluna in range(ordem)] for linha in range(ordem)]
    quantidadeBombas = 1 #random.randint(dificuldade//2, dificuldade+1)

    posicoesSagradas=[]

    for i in range(-1, 2): #-1 é acima
        for j in range(-1,2): #-1 é esquerda
            coordenadas = (linhaEscolha + i, colunaEscolha + j)
            posicoesSagradas.append(coordenadas)
            
    quantidadeBombas_agora=quantidadeBombas
    while quantidadeBombas_agora>0:
        bombaLinha, bombaColuna=random.randint(0, ordem - 1 ), random.randint(0, ordem - 1)
        coordenadaBomba = (bombaLinha, bombaColuna)
        if coordenadaBomba not in posicoesSagradas:
            matrizMapa[bombaLinha][bombaColuna] = 1
            quantidadeBombas_agora-=1
    
    matrizCampo = criarMatrizCampo(matrizMapa, ordem)

    matrizJogador = [['x' for coluna in range(ordem)] for linha in range(ordem)]
    primeira_vez=1
    
    while True:
        if not primeira_vez:
            linhaEscolha, colunaEscolha = map(int, input("Digite a posição para escolha (linha coluna): ").split())
            linhaEscolha -= 1
            colunaEscolha -= 1
    
        matrizJogador[linhaEscolha][colunaEscolha] = matrizCampo[linhaEscolha][colunaEscolha]

        #-1:-1 I -1:0 I -1:1
        #0:-1 I 0:0 I 0:1
        #1:-1 I 1:0 I 1:1
        for i in range(-1, 2): #-1 é acima
            for j in range(-1,2): #-1 é esquerda

                if i == 0 and j == 0: continue # IGNORA O CENTRO
                    
                novaLinha, novaColuna = linhaEscolha + i, colunaEscolha + j
                
                if 0 <= novaLinha < ordem and 0 <= novaColuna < ordem:
                    if i!=0 and j!=0: #checa os cantos
                        if (matrizCampo[linhaEscolha + i][colunaEscolha] == 0 or matrizCampo[linhaEscolha][colunaEscolha + j] == 0) and matrizCampo[linhaEscolha + i][colunaEscolha + j] == 0:
                            matrizJogador[novaLinha][novaColuna] = matrizCampo[novaLinha][novaColuna]
                    elif matrizCampo[novaLinha][novaColuna] == 0: matrizJogador[novaLinha][novaColuna] = matrizCampo[novaLinha][novaColuna]

                    if primeira_vez:
                        matrizJogador[novaLinha][novaColuna] = matrizCampo[novaLinha][novaColuna]


        x_sobrando=0
        for coluna in matrizJogador:
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
                        x_sobrando+=1
            print(Style.RESET_ALL)
            
        if debug_mode:
            print("Debug matriz / x's sobrando:")
            for coluna in matrizCampo:
                for elemento in coluna:
                    
                    match elemento:
                        case 'B': print(Fore.RED + "B", end=" ")
                        case 0: print(Fore.WHITE + str(elemento), end=" ")
                        case 1: print(Fore.BLUE + str(elemento), end=" ")
                        case 2: print(Fore.GREEN + str(elemento), end=" ")
                        case 3: print(Fore.RED + str(elemento), end=" ")
                        case 4: print(Fore.BLACK + str(elemento), end=" ")
                        case 'x': print(Fore.WHITE + elemento, end=" ")
                print(Style.RESET_ALL)
            print(x_sobrando)
        primeira_vez=0

        if matrizCampo[linhaEscolha][colunaEscolha] == 'B':
            print()
            print(Fore.RED + "Perdeu seu merdinha >:)", end=" ")
            break
        elif x_sobrando==quantidadeBombas:
            print(Fore.GREEN + "Você ganhou yayyy :D", end=" ")
            break

            

while True:
    if __name__ == '__main__':
        main()
        print(Style.RESET_ALL)
        resposta= input("Gostaria de encerrar a sessão? (Digite ''sim'' caso seja sua vontade) \n").lower()
        if resposta=="sim":
            print("Como quiser")
            break