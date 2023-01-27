import random
import sys
import pygame
import time

pygame.init()

screen = pygame.display.set_mode((700, 700))

White = pygame.Color(255, 255, 255)
Black = pygame.Color(0, 0, 0)
Red = pygame.Color(255, 0, 0)
Green = pygame.Color(0, 255, 0)
Blue = pygame.Color(0, 0, 255)

width, height = 20, 20
vWalls = [[1 for j in range(height)] for i in range(width+1)]
hWalls = [[1 for j in range(height+1)] for i in range(width)]
cells = [[0 for j in range(height)] for i in range(width)]

def makeMaze(current, cells, vWalls, hWalls):
    cells[current[0]][current[1]] = 1
    drawMaze(current, cells, vWalls, hWalls)
    time.sleep(0.1)

    while True:
        possible = []
        if current[0]-1 >= 0 and cells[current[0]-1][current[1]] == 0:
            possible.append((current[0]-1, current[1]))
        if current[0]+1 < width and cells[current[0]+1][current[1]] == 0:
            possible.append((current[0]+1, current[1]))
        if current[1]-1 >= 0 and cells[current[0]][current[1]-1] == 0:
            possible.append((current[0], current[1]-1))
        if current[1]+1 < height and cells[current[0]][current[1]+1] == 0:
            possible.append((current[0], current[1]+1))

        if len(possible) == 0:
            return (cells, vWalls, hWalls)

        next = random.choice(possible)
        if next[0] == current[0]:
            if next[1] > current[1]:
                hWalls[next[0]][next[1]] = 0
            else:
                hWalls[next[0]][next[1]+1] = 0
        else:
            if next[0] > current[0]:
                vWalls[next[0]][next[1]] = 0
            else:
                vWalls[next[0]+1][next[1]] = 0

        cells, vWalls, hWalls = makeMaze(next, cells, vWalls, hWalls)

def makeExit(vWalls, hWalls):
    array = random.choice([vWalls, hWalls])
    if array == vWalls:
        end = (random.choice([0, width]), random.randint(0, height-1))
        vWalls[end[0]][end[1]] = 0
        array = 'vWalls'
    else:
        end = (random.randint(0, width-1), random.choice([0, height]))
        hWalls[end[0]][end[1]] = 0
        array = 'hWalls'

    return (vWalls, hWalls, end, array)

def fillExit(array, exit):
    if array == 'vWalls':
        vWalls[exit[0]][exit[1]] = 1
    else:
        hWalls[exit[0]][exit[1]] = 1

def drawMaze(current, cells, vWalls, hWalls):
    s = 25 #side length of cell

    screen.fill(White)

    for i in range(len(vWalls)):
        for j in range(len(vWalls[0])):
            if vWalls[i][j] == 1:
                pygame.draw.line(screen, Black, (s*i+100, s*j+100), (s*i+100, s*j+100+s))

    for i in range(len(hWalls)):
        for j in range(len(hWalls[0])):
            if hWalls[i][j] == 1:
                pygame.draw.line(screen, Black, (s*i+100, s*j+100), (s*i+100+s, s*j+100))

    pygame.draw.rect(screen, Blue, (s*current[0]+105, s*current[1]+105, s-10, s-10))

    pygame.display.update()

#BFS to find shortest path
def solveMaze(start, end, cells, vWalls, hWalls):
    active = [start]
    explored = [start]
    path = {}

    while active:
        p = active.pop(0)
        possible = []

        if p == end:
            break

        if p[0]-1 >= 0 and vWalls[p[0]][p[1]] == 0:
            possible.append((p[0]-1, p[1]))
        if p[0]+1 < width and vWalls[p[0]+1][p[1]] == 0:
            possible.append((p[0]+1, p[1]))
        if p[1]-1 >= 0 and hWalls[p[0]][p[1]] == 0:
            possible.append((p[0], p[1]-1))
        if p[1]+1 < height and hWalls[p[0]][p[1]+1] == 0:
            possible.append((p[0], p[1]+1))

        for loc in possible:
            if loc not in explored:
                active.append(loc)
                explored.append(loc)
                path[loc] = p

    moves = 0
    current = end
    shortPath = []
    while True:
        shortPath.insert(0, current)
        if current not in path:
            break
        current = path[current]
        moves += 1
    return (shortPath, moves)

def solveAnim(path):
    for i in range(len(path)):
        if i == 0:
            pygame.draw.rect(screen, Blue, (25 * path[i][0] + 105, 25 * path[i][1] + 105, 15, 15))
        else:
            pygame.draw.line(screen, Red, (path[i-1][0]*25+112, path[i-1][1]*25+112),
                             (path[i][0]*25+112, path[i][1]*25+112), 2)
        if i == len(path) - 1:
            pygame.draw.rect(screen, Green, (25 * path[i][0] + 105, 25 * path[i][1] + 105, 15, 15))
        pygame.display.update()
        time.sleep(0.1)


start = (random.randint(0, width-1), random.randint(0, height-1))
cells, vWalls, hWalls = makeMaze(start, cells, vWalls, hWalls)
while True:
    vWalls, hWalls, end, array = makeExit(vWalls, hWalls)
    save = end
    if end[0] == width:
        end = (end[0]-1, end[1])
    elif end[1] == height:
        end = (end[0], end[1]-1)
    if solveMaze(start, end, cells, vWalls, hWalls)[1] >= 100:
        break
    else:
        fillExit(array, save)

drawMaze(start, cells, vWalls, hWalls)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                path, moves = solveMaze(start, end, cells, vWalls, hWalls)
                solveAnim(path)
                print(moves)

            if event.key == pygame.K_ESCAPE:
                pygame.QUIT
