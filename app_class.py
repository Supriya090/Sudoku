import pygame, sys
import requests

from bs4 import BeautifulSoup

from settings import *
from buttonClass import *

class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        #self.grid = finishedBoard
        self.grid = self.getPuzzle("2")
        self.selected = None
        self.mousePos = None
        self.state = "playing"
        self.finished = False
        self.cellChanged = False
        self.playingButtons = []
        self.menuButtons = []
        self.endButtons = []
        self.lockedCells = []
        self.incorrectCells = []
        self.font = pygame.font.SysFont("arial", cellSize//2)
        self.load()
        
        #board = self.getPuzzle("1")
        #print(board)

    def run(self):
        while self.running:
            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()
        sys.exit()

########## PLAYING STATE FUNCTIONS ############
    
    def playing_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            ## User Clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouseOnGrid()
                if selected:
                    self.selected = selected
                else:
                    print("not on Board")
                    self.selected = None

            ## User types a key
            if event.type == pygame.KEYDOWN:
                if (self.selected != None) and (self.selected not in self.lockedCells):
                    if self.isInt(event.unicode):
                        #cell changed
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        self.cellChanged = True

    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButtons:
            button.update(self.mousePos)

        if self.cellChanged:
            self.incorrectCells = []
            if self.allCellsDone():
                # Check if board is correct
                self.checkAllCells()
                if len(self.incorrectCells) == 0:
                    print("Congratulations!")

    def playing_draw(self):
        self.window.fill(WHITE)

        for button in self.playingButtons:
            button.draw(self.window)
        
        if self.selected:
            self.drawSelection(self.window, self.selected)

        self.shadeLockedCells(self.window, self.lockedCells)
        self.shadeIncorrectCells(self.window, self.incorrectCells)

        self.drawNumbers(self.window)

        self.drawGrid(self.window)
        pygame.display.update()
        self.cellChanged = False

########### BOARD CHECKING FUNCTIONS ###########

    def allCellsDone(self):
        for row in self.grid:
            for num in row:
               if num == 0:
                   return False 
        return True

    def checkAllCells(self):
       self.checkRows()
       self.checkCols()
       self.checkSmallGrid() 

    def checkSmallGrid(self):
        for x in range(3):
            for y in range(3):
                possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                #print("resetting possibles")
                for i in range(3):
                    for j in range(3):
                        xIndex = x*3 + i
                        yIndex = y*3 + j
                        if self.grid[yIndex][xIndex] in possibles:
                            possibles.remove(self.grid[yIndex][xIndex])
                        else:
                            if [xIndex, yIndex] not in self.lockedCells and [xIndex, yIndex] not in self.incorrectCells:
                                self.incorrectCells.append[xIndex, yIndex]
                            if [xIndex, yIndex] in self.lockedCells:
                                for k in range(3):
                                    for l in range(3):
                                        xIndex2 = x*3+k
                                        yIndex2 = y*3+l
                                        if self.grid[yIndex2][xIndex2] == self.grid[yIndex][xIndex] and [xIndex2, yIndex2] not in self.lockedCells:
                                            self.incorrectCells.append([xIndex2,yIndex2])

                            


    def checkRows(self):
        for yIndex, row in enumerate(self.grid):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for xIndex in range(9):
                if self.grid[yIndex][xIndex] in possibles:
                    possibles.remove(self.grid[yIndex][xIndex])
                else:
                    if [xIndex, yIndex] not in self.lockedCells and [xIndex, yIndex] not in self.incorrectCells:
                        self.incorrectCells.append([xIndex, yIndex])
                    if [xIndex, yIndex] in self.lockedCells:
                        for k in range(9):
                            if self.grid[yIndex][k] == self.grid[yIndex][xIndex] and [k, yIndex] not in self.lockedCells:
                                self.incorrectCells.append([k, yIndex])

    def checkCols(self):
        for xIndex in range(9):
            possibles = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            for yIndex, row in enumerate(self.grid):
                if self.grid[yIndex][xIndex] in possibles:
                    possibles.remove(self.grid[yIndex][xIndex])
                else:
                    if [xIndex, yIndex] not in self.lockedCells and [xIndex, yIndex] not in self.incorrectCells:
                        self.incorrectCells.append([xIndex, yIndex])
                    if [xIndex, yIndex] in self.lockedCells:
                        for k, row in enumerate(self.grid):
                            if self.grid[k][xIndex] == self.grid[yIndex][xIndex] and [xIndex, k] not in self.lockedCells:
                                self.incorrectCells.append([xIndex, k])

    
########### HELPER FUNCTIONS ###########

    def getPuzzle(self, difficulty):
        # Difficulty needs to be passed in as string with one digit. 1-4  
        html_doc = requests.get("https://nine.websudoku.com/?level=()".format(difficulty)).content 
        soup = BeautifulSoup(html_doc, features="html.parser")
        ids = ['f00', 'f01', 'f02', 'f03', 'f04', 'f05', 'f06', 'f07', 'f08', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f20', 'f21', 'f22', 'f23', 'f24', 'f25', 'f26', 'f27', 'f28', 'f30', 'f31', 'f32', 'f33', 'f34', 'f35', 'f36', 'f37', 'f38', 'f40', 'f41', 'f42', 'f43', 'f44', 'f45', 'f46', 'f47', 'f48', 'f50', 'f51', 'f52', 'f53', 'f54', 'f55', 'f56', 'f57', 'f58', 'f60', 'f61', 'f62', 'f63', 'f64', 'f65', 'f66', 'f67', 'f68', 'f70', 'f71', 'f72', 'f73', 'f74', 'f75', 'f76', 'f77', 'f78', 'f80', 'f81', 'f82', 'f83', 'f84', 'f85', 'f86', 'f87', 'f88']
        data = []
        for cid in ids:
            data.append(soup.find('input', id=cid))
        board = [[0 for x in range(9)] for x in range(9)]
        for index, cell in enumerate(data):
            try:
                board[index//9][index%9] = int(cell['value'])
            except:
                pass
        return board

    def shadeIncorrectCells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, INCORRECTCELLCOLOUR, (cell[0]*cellSize+gridPos[0], cell[1]*cellSize+gridPos[1], cellSize, cellSize))
    
    def shadeLockedCells(self, window, locked):
        for cell in locked: 
            pygame.draw.rect(window, LOCKEDCELLCOLOUR, (cell[0]*cellSize+gridPos[0], cell[1]*cellSize+gridPos[1], cellSize, cellSize))

    def drawNumbers(self, window):
        for yIndex, row in enumerate(self.grid):
            for xIndex, num in enumerate(row):
                if num != 0:
                    pos = [xIndex*cellSize+gridPos[0], yIndex*cellSize+gridPos[1]]
                    self.textToScreen(window, str(num), pos)

    def drawSelection(self, window, pos):
        pygame.draw.rect(window, LIGHTBLUE, ((pos[0]*cellSize)+gridPos[0], (pos[1]*cellSize)+gridPos[1], cellSize, cellSize))

    def drawGrid(self, window):
        pygame.draw.rect(window, BLACK, (gridPos[0], gridPos[1], WIDTH-150, HEIGHT - 150), 2)
        for x in range(9):
            pygame.draw.line(window, BLACK, (gridPos[0] + (x*cellSize), gridPos[1]), (gridPos[0] + (x*cellSize), gridPos[1] + 450), 2 if x % 3 == 0 else 1)
            pygame.draw.line(window, BLACK, (gridPos[0], gridPos[1] + (x*cellSize)), (gridPos[0]+ 450, gridPos[1]+(x*cellSize)), 2 if x % 3 == 0 else 1)

    def mouseOnGrid(self):
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1]:
            return False
        
        if self.mousePos[0] > gridPos[0] + gridSize or self.mousePos[1] > gridPos[1]+gridSize:
            return False
        
        return ((self.mousePos[0]-gridPos[0])//cellSize, (self.mousePos[1]- gridPos[1])//cellSize)

    def loadButtons(self):
        self.playingButtons.append(Button(20, 40, 100, 40))


    def textToScreen(self, window, text, pos):
        font = self.font.render(text, False, BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (cellSize - fontWidth)//2
        pos[1] += (cellSize - fontHeight)//2 
        window.blit(font, pos)

    def load(self):
        self.loadButtons()

        # Setting Locked cells from original Board
        for yIndex, row in enumerate(self.grid):
            for xIndex, num in enumerate(row):
                if num != 0:
                    self.lockedCells.append([xIndex, yIndex]) 

    
    def isInt(self, string):
        try:
            int(string)
            return True
        except:
            return False