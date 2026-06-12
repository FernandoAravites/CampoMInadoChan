import os
import math
import sys
import random


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
            if matrizOriginal[i][j] == 1: matrizCampo[i][j] = -1
            else: matrizCampo[i][j] = contarBombaVizinha(matrizOriginal, i, j, ordem)
    
    return matrizCampo

def main():

    ordem = 5
    dificuldade = 2 * ordem
    matrizMapa = [[0 for coluna in range(ordem)] for linha in range(ordem)]
    quantidadeBombas = random.randint(0, dificuldade)

    for _ in range(quantidadeBombas):
        bombaLinha, bombaColuna = random.randint(0, ordem -1 ), random.randint(0, ordem - 1)
        matrizMapa[bombaLinha][bombaColuna] = 1 # LUGAR ALEATÓRIO QUE TEM BOMBA
    
    matrizCampo = criarMatrizCampo(matrizMapa, ordem)

    print('\n'.join(f'{str(elemento)}' for elemento in matrizCampo))

if __name__ == '__main__': main()