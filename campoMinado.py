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
    ordem = 5
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
    quantidadeBombas = random.randint(dificuldade//2, dificuldade+1)

    posicoesSagradas=[]

    for i in range(-1, 2): #-1 é acima
        for j in range(-1,2): #-1 é esquerda
            coordenadas = (linhaEscolha + i, colunaEscolha + j)
            posicoesSagradas.append(coordenadas)
            

    while quantidadeBombas>0:
        bombaLinha, bombaColuna=random.randint(0, ordem - 1 ), random.randint(0, ordem - 1)
        coordenadaBomba = (bombaLinha, bombaColuna)
        if coordenadaBomba not in posicoesSagradas:
            matrizMapa[bombaLinha][bombaColuna] = 1
            quantidadeBombas-=1
    
    matrizCampo = criarMatrizCampo(matrizMapa, ordem)

    
    matrizJogador = [['x' for coluna in range(ordem)] for linha in range(ordem)]
    nao_rodar_da_primeira_vez=0
    
    while True:
        if nao_rodar_da_primeira_vez:
            linhaEscolha, colunaEscolha = map(int, input("Digite a posição para escolha (linha coluna): ").split())
            linhaEscolha -= 1
            colunaEscolha -= 1
        nao_rodar_da_primeira_vez=1
        matrizJogador[linhaEscolha][colunaEscolha] = matrizCampo[linhaEscolha][colunaEscolha]

        #-1:-1 I -1:0 I -1:1
        #0:-1 I 0:0 I 0:1
        #1:-1 I 1:0 I 1:1
        for i in range(-1, 2): #-1 é acima
            for j in range(-1,2): #-1 é esquerda

                if i == 0 and j == 0: continue # IGNORA O CENTRO
                    
                novaLinha, novaColuna = linhaEscolha + i, colunaEscolha + j
                
                if 0 <= novaLinha < ordem and 0 <= novaColuna < ordem:
                    if i!=0 and j!=0: #chac os cantos
                        if (matrizCampo[linhaEscolha + i][colunaEscolha] == 0 or matrizCampo[linhaEscolha][colunaEscolha + j] == 0) and matrizCampo[linhaEscolha + i][colunaEscolha + j] == 0:
                            matrizJogador[novaLinha][novaColuna] = matrizCampo[novaLinha][novaColuna]
                    elif matrizCampo[novaLinha][novaColuna] == 0: matrizJogador[novaLinha][novaColuna] = matrizCampo[novaLinha][novaColuna] 

    
        for coluna in matrizJogador:
            for elemento in coluna:

                match elemento:
                    case 'B': print(Fore.RED + "BOOM!", end=" ")
                    case 0: print(Fore.WHITE + str(elemento), end=" ")
                    case 1: print(Fore.BLUE + str(elemento), end=" ")
                    case 2: print(Fore.GREEN + str(elemento), end=" ")
                    case 3: print(Fore.RED + str(elemento), end=" ")
                    case 4: print(Fore.BLACK + str(elemento), end=" ")
                    case 'x': print(Fore.WHITE + elemento, end=" ")
            print(Style.RESET_ALL)

        if debug_mode:
            print()
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
        
        if matrizCampo[linhaEscolha][colunaEscolha] == 'B':
            print()
            print("Perdeu seu merdinha")
            break


if __name__ == '__main__': main()