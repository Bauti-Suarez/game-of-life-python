import pygame
import numpy as np
import time
# iniciamos pygame
pygame.init()
# ancho y alto
width, height = 500, 500
screen = pygame.display.set_mode((height, width))
# fondo
bg = (25, 25, 25)
screen.fill(bg)
# num cell
nxC, nyC = 50, 50
# dimenciones de la celda
dimCW = width / nxC
dimCH = height / nyC
# estado de las celdas.
gameState = np.zeros((nxC, nyC))

gameState[5, 5] = 1
gameState[5, 6] = 1
gameState[5, 7] = 1
# control de la ejecucion
pauseExect = False
# bucle
while True:
    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.2)

    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()
        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY/dimCH))
            newGameState[celX,celY] = not mouseClick[2]

    for x in range(0, nxC):
        for y in range(0, nyC):

            if not pauseExect:
                # num vecinos
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
                     gameState[(x) % nxC, (y - 1) % nyC] + \
                     gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                     gameState[(x - 1) % nxC, (y) % nyC] + \
                     gameState[(x + 1) % nxC, (y) % nyC] + \
                     gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                     gameState[(x) % nxC, (y + 1) % nyC] + \
                     gameState[(x + 1) % nxC, (y + 1) % nyC]
                

                # regla 1: una celula muerta con 3 celulas vivas al rededor, revive
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # regla 2: una celula viva con menos de 2 o mas de 3 vecinas vivas, mueren
                elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0
            # poligonos de cada celda
            poly = [
                ((x) * dimCW, y * dimCH),
                ((x + 1) * dimCW, y * dimCH),
                ((x + 1) * dimCW, (y + 1) * dimCH),
                ((x) * dimCW, (y + 1) * dimCH),
            ]
            # dibujamos la celda para cada par de x e y.
            if newGameState[x, y] == 0:
                 pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 0)

    # actualizamos el estado del juego.
    gameState = np.copy(newGameState)

    # actualiza la pantalla
    pygame.display.flip()
