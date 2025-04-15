################################################################
###                 M O S T R A   M A Z E                    ###
################################################################
### Neste teste, mostra o labirinto gerado pelo algoritmo de ###
### Aldous-Broder                                            ###
################################################################
### Prof. Filipo Mor, FILIPOMOR.COM                          ###
################################################################

import pygame
import sys
import copy
import random
from random import randint
import heapq
import time

class ArestasFechadas:
    def __init__(self, superior, inferior, esquerda, direita):
        self.superior = superior
        self.inferior = inferior
        self.esquerda = esquerda
        self.direita = direita


class Celula:
    def __init__(self, arestasFechadas, corPreenchimento, corVisitada, corLinha, corAberta, visitada, aberta):
        self.arestasFechadas = arestasFechadas
        self.corPreenchimento = corPreenchimento
        self.corVisitada = corVisitada
        self.corLinha = corLinha
        self.corAberta = corAberta
        self.visited = visitada
        self.aberta = aberta
        self.caminho = False  # faz parte da solução do labirinto?


    def get_corPreenchimento(self):
        return self.corPreenchimento

    def get_arestasFechadas(self):
        return self.arestasFechadas

    def is_visited(self):
        return self.visited

    def desenhar(self, tela, x, y, aresta):
        # x : coluna
        # y : linha

        # calcula as posicoes de desenho das linhas de cada aresta
        arSuperiorIni = (x, y)
        arSuperiorFim = (x + aresta, y)
        arInferiorIni = (x, y + aresta)
        arInferiorFim = (x + aresta, y + aresta)
        arEsquerdaIni = (x, y)
        arEsquerdaFim = (x, y + aresta)
        arDireitaIni = (x + aresta, y)
        arDireitaFim = (x + aresta, y + aresta)

        # preenche a célula com a cor definida - modificado
        if self.caminho:
            pygame.draw.rect(tela, (0, 255, 0), (x, y, aresta, aresta))  # verde para o caminho
        elif self.aberta:
            pygame.draw.rect(tela, self.corAberta, (x, y, aresta, aresta))
        else:
            pygame.draw.rect(tela, self.corPreenchimento, (x, y, aresta, aresta))

        pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)

        '''
        # linha superior
        if (self.arestasFechadas.superior):
            pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        # linha inferior
        if (self.arestasFechadas.inferior):
            pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        # linha esquerda
        if (self.arestasFechadas.esquerda):
            pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        # linha direita
        if (self.arestasFechadas.direita):
            pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)
        '''
        '''
        pygame.draw.line(tela, self.corLinha, arSuperiorIni, arSuperiorFim)
        pygame.draw.line(tela, self.corLinha, arInferiorIni, arInferiorFim)
        pygame.draw.line(tela, self.corLinha, arEsquerdaIni, arEsquerdaFim)
        pygame.draw.line(tela, self.corLinha, arDireitaIni, arDireitaFim)
        '''


class AldousBroder:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.matriz = Malha(qtLinhas, qtColunas, aresta, celulaPadrao)
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        # self.visitados = []

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def resetaLabirinto(self):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna] = copy.deepcopy(self.celulaPadrao)

    def SorteiaCelulaVizinha(self, linhaCelulaAtual, colunaCelulaAtual):
        encontrou = False
        while (encontrou == False):
            linhaVizinha = linhaCelulaAtual + randint(-1, 1)
            colunaVizinha = colunaCelulaAtual + randint(-1, 1)
            if (
                    linhaVizinha >= 0 and linhaVizinha < self.qtLinhas and colunaVizinha >= 0 and colunaVizinha < self.qtColunas):
                encontrou = True

        return linhaVizinha, colunaVizinha

    def GeraLabirinto(self):
        self.resetaLabirinto()

        unvisitedCells = self.qtLinhas * self.qtColunas
        currentCellLine = randint(0, self.qtLinhas - 1)
        currentCellColumn = randint(0, self.qtColunas - 1)

        while unvisitedCells > 0:
            neighCellLine, neighCellColumn = self.SorteiaCelulaVizinha(currentCellLine, currentCellColumn)

            if not self.matriz[neighCellLine][neighCellColumn].visited:
                self.matriz[currentCellLine][currentCellColumn].aberta = True
                self.matriz[neighCellLine][neighCellColumn].visited = True
                unvisitedCells -= 1

            currentCellLine, currentCellColumn = neighCellLine, neighCellColumn

        # Entrada e saida
        self.matriz[1][0].aberta = True
        self.matriz[1][0].visited = True

        self.matriz[self.qtLinhas - 1][self.qtColunas - 1].aberta = True
        self.matriz[self.qtLinhas - 1][self.qtColunas - 1].visited = True


class Malha:
    def __init__(self, qtLinhas, qtColunas, aresta, celulaPadrao):
        self.qtLinhas = qtLinhas
        self.qtColunas = qtColunas
        self.aresta = aresta
        self.celulaPadrao = celulaPadrao
        self.matriz = self.GeraMatriz()

    def __len__(self):
        return len(self.matriz)

    def __iter__(self):
        return iter(self.matriz)

    def __getitem__(self, index):
        return self.matriz[index]

    def __setitem__(self, index, value):
        self.matriz[index] = value

    def __aslist__(self):
        return self.matriz

    def GeraMatriz(self):
        matriz = []
        for i in range(self.qtLinhas):
            linha = []
            for j in range(self.qtColunas):
                #newCell = copy.deepcopy(self.celulaPadrao)
                linha.append(copy.deepcopy(self.celulaPadrao))
            matriz.append(linha)
        return matriz

    def DesenhaLabirinto(self, tela, x, y):
        for linha in range(self.qtLinhas):
            for coluna in range(self.qtColunas):
                self.matriz[linha][coluna].desenhar(tela, x + coluna * self.aresta, y + linha * self.aresta, self.aresta)


def main():
    pygame.init()

    ### definição das cores
    azul = (50, 50, 255)
    preto = (0, 0, 0)
    branco = (255, 255, 255)
    vermelho = (255, 0, 0)
    cinza = (128, 128, 128)

    grey = (141, 153, 174)
    navyblue = (43, 45, 66)
    white = (253, 240, 213)
    red = (230, 57, 70)
    yellow = (252, 163, 17)


    # Dimensões da janela
    [largura, altura] = [1000, 800]

    ### Dimensões da malha (matriz NxM)
    N = 60  # número de linhas
    M = 80  # número de colunas
    aresta = 10  # dimensão dos lados das células

    # cores: preenchimento - visitada - linha - aberta
    celulaPadrao = Celula(ArestasFechadas(False, False, False, False), navyblue, grey, navyblue, white, False, False)
    labirinto = AldousBroder(N, M, aresta, celulaPadrao)
    labirinto.GeraLabirinto()
    resolve_labirinto(labirinto.matriz, 1, 0, labirinto.qtLinhas - 1, labirinto.qtColunas - 1)


    # Cria a janela
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption('Mostra Malha')

    #Adiciona um label de Debug
    fonte = pygame.font.Font(None, 36)  # None = fonte padrão do sistema; 36 = tamanho
    texto = fonte.render(str(1), True, navyblue)  # True = antialiasing, cor = PRETO
    posicao = (20, 20)  # Posição onde o texto será desenhado

    ###
    ### Loop principal
    ###
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ### preenche a tela com a cor branca
        tela.fill(white)

        ### centraliza a grade na janela
        [linha, coluna] = ((tela.get_width() - (M * aresta)) // 2,
                           (tela.get_height() - (N * aresta)) // 2)
        # desenhar_grade(tela, linha, coluna, aresta, N, M, matriz)
        labirinto.matriz.DesenhaLabirinto(tela, linha, coluna)

        #Desenha um arquivo de texto para Debug
        tela.blit(texto, posicao)

        ### atualiza a tela
        pygame.display.flip()



def resolve_labirinto(malha, lin_inicio, col_inicio, lin_fim, col_fim):
    linhas = len(malha)
    colunas = len(malha[0])

    def heuristica(a, b):
        # Heurística de distância de Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    aberto = []  # Fila de prioridade
    heapq.heappush(aberto, (0, lin_inicio, col_inicio))  # Começa a fila com o ponto inicial
    veio_de = {}  # Para reconstruir o caminho
    custo_inicio = {}  # Custos para chegar em cada célula
    custo_inicio[(lin_inicio, col_inicio)] = 0

    # Captura o tempo inicial
    inicio_tempo = time.time()

    while aberto:
        _, lin, col = heapq.heappop(aberto)  # Retira o elemento com a menor prioridade (custo + heurística)
        atual = malha[lin][col]

        if (lin, col) == (lin_fim, col_fim):  # Se chegou ao destino
            # Reconstruir o caminho
            while (lin, col) in veio_de:
                atual.caminho = True
                lin, col = veio_de[(lin, col)]
                atual = malha[lin][col]
            atual.caminho = True  # Marca o início

            # Captura o tempo final e calcula o tempo gasto
            fim_tempo = time.time()
            tempo_total = fim_tempo - inicio_tempo
            print(f"Tempo para resolver o labirinto: {tempo_total:.4f} segundos.")
            return

        atual.aberta = False  # Marca a célula como visitada
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Direções: cima, baixo, esquerda, direita
        for dlin, dcol in direcoes:
            viz_lin, viz_col = lin + dlin, col + dcol
            if 0 <= viz_lin < linhas and 0 <= viz_col < colunas:  # Verifica se a célula está dentro dos limites
                vizinha = malha[viz_lin][viz_col]
                if not vizinha.aberta:  # Se a célula não está aberta, ignora
                    continue
                novo_custo = custo_inicio[(lin, col)] + 1  # Custo até a célula vizinha
                if (viz_lin, viz_col) not in custo_inicio or novo_custo < custo_inicio[(viz_lin, viz_col)]:
                    custo_inicio[(viz_lin, viz_col)] = novo_custo
                    prioridade = novo_custo + heuristica((viz_lin, viz_col), (lin_fim, col_fim))  # Cálculo da prioridade
                    heapq.heappush(aberto, (prioridade, viz_lin, viz_col))  # Adiciona a célula na fila
                    veio_de[(viz_lin, viz_col)] = (lin, col)  # Registra de onde veio
                    vizinha.aberta = True  # Marca a célula como explorada

    print("Labirinto sem solução.")  # Caso não haja solução


if __name__ == '__main__':
    main()