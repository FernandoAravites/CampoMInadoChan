import os
import math
import sys
import random
from colorama import Fore, Back, Style, init
#pip install colorama terminal

def limpar(): #Apaga o que está escrito no terminal. Facilita os testes

    os.system('cls' if os.name == 'nt' else 'clear')

limpar()
    
def contarBombaVizinha(matriz, linha, coluna, ordem): #retorna quantas bombas tem ao redor de um ponto
    
    bombas = 0

    for i in range(-1, 2): # i é como o a posição x, checa se tem bomba no lado esquerdo (-1) e direito (1)
        for j in range(-1,2): # j é como o a posição y, checa se tem bomba abaixo (-1) e acima (1)

            if i == 0 and j == 0: continue # ignora o centro (ponto), queremos saber se tem bombas ao redor
                
            novaLinha, novaColuna = linha + i, coluna + j #ponto onde será checado se tem bomba
            
            if 0 <= novaLinha < ordem and 0 <= novaColuna < ordem: #Cuida para não checarem pontos fora da matriz

                if matriz[novaLinha][novaColuna] == 1: bombas += 1

    return bombas

def criarMatrizCampo(matrizOriginal, ordem):
    matrizCampo = [[0 for _ in range(ordem)] for _ in range(ordem)] #cria uma matriz apenas com 0
    
    for i in range(ordem):
        for j in range(ordem):
            if matrizOriginal[i][j] == 1: matrizCampo[i][j] = 'B'
            else: matrizCampo[i][j] = contarBombaVizinha(matrizOriginal, i, j, ordem)
    
    return matrizCampo

def main():
    #ordem = int(input("Digite o tamanho do campo minado: "))
    ordem=5

    dificuldade = 2 * ordem
    matrizMapa = [[0 for coluna in range(ordem)] for linha in range(ordem)] #cria uma matriz apenas com 0
    quantidadeBombas = random.randint(0, dificuldade) #escolhe o numero de bombas no campo

    for _ in range(quantidadeBombas): #escolhe aleatoriamente um espaço para ter bomba
        bombaLinha, bombaColuna = random.randint(0, ordem -1 ), random.randint(0, ordem - 1)
        matrizMapa[bombaLinha][bombaColuna] = 1
    
    matrizCampo = criarMatrizCampo(matrizMapa, ordem)

    #matrizMapa= matriz apenas com 0 e 1, 0 significa que o ponto não tem bomba, caso 1, então tem
    #matrizCampo= matriz onde cada ponto reflete o numero de bombas ao redor, se o lugar tem bomba então é -1
    #matrizJogador= Matriz com X onde o jagador interage

    interagido=[]



    for coluna in matrizCampo:
        for elemento in coluna:
            if coluna==1:
                print("x")
            else:
                match elemento:
                    case 'B': print(Fore.WHITE + str(elemento), end=" ")
                    case 0: print(Fore.WHITE + str(elemento), end=" ")
                    case 1: print(Fore.BLUE + str(elemento), end=" ")
                    case 2: print(Fore.GREEN + str(elemento), end=" ")
                    case 3: print(Fore.RED + str(elemento), end=" ")
                    case 4: print(Fore.BLACK + str(elemento), end=" ")
        print()

if __name__ == '__main__': main()