from cmu_graphics import *

import math
import random
from PIL import Image
import os, pathlib
import copy

# Define all classes first before using them

class Wonka:
    def __init__(self, app):
        self.row = 0
        self.col = 0
        self.sideSize = app.side
        self.app = app
        self.cellSize = self.getCellSize()
        self.x = app.width/2 - 250 + self.cellSize / 2
        self.y = app.height/2 - 450 + self.cellSize / 2
        self.lives = 5
        self.dead = False
        self.overlapped = False
        # Updated image path
        self.image = Image.open('wonka_character.jpeg')
        self.imageFlipped = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.image = CMUImage(self.imageFlipped)
        self.collectCandy = False
        self.stepSize = 5
        self.targetPosition = None
        self.score = 0
        self.direction = 'right'  # Track direction for animation
        self.animationFrame = 0

    def onCandy(self, app):
        candyPos = self.app.candy.candy_positions
        newX, newY = self.candy.convertCoordsToNode(app, self.x, self.y)
        if (newX, newY) in candyPos:
            self.app.candy_positions.remove((newX, newY))
            
    def updateCoords(self):
        self.x = (self.app.width/2 - 250 + self.col * self.cellSize + 
                  self.cellSize/2)
        self.y = (self.app.height/2 - 250 + self.row * self.cellSize +
                   self.cellSize/2)

    def draw(self):
        # Draw Wonka with some whimsical animation
        wobble = 2 * math.sin(self.app.colorTimer/5)
        drawImage(self.image, self.x-20, self.y-5 + wobble, width=40, height=40)
        
        # Draw a colorful hat or coat effect
        drawRect(self.x-20, self.y-85 + wobble, 40, 10, fill='purple', 
                 align='center')
    
    def getCellLeftTop(self):
        cellSize = self.getCellSize()
        cellLeft = self.app.width/2-250 + self.col * cellSize
        cellTop = self.app.height/2-250 + self.row * cellSize
        return (cellLeft, cellTop)

    def getCellSize(self):
        cellSize = self.sideSize / self.app.rows
        return cellSize
    
    def touchNode(self):
        colTest = ((self.x-(self.app.width/2 -250 + self.cellSize / 2))
                   /self.cellSize)
        rowTest = ((self.y-(self.app.height/2 -250 + self.cellSize / 2))
                   /self.cellSize)
        return (rowTest, colTest) in self.app.nodes

    def extractNode(self):
        col = ((self.x-(self.app.width/2 -250 + self.cellSize / 2))
                /self.cellSize)
        row = ((self.y-(self.app.height/2 -250 + self.cellSize / 2))
               /self.cellSize)
        return (row, col)

# Golden Ticket (previously Powerup)
class GoldenTicket:
    def __init__(self, app):
        self.app = app
        self.sideSize = app.side
        self.cellSize = self.getCellSize()
        self.x = app.width / 2 - 250 + app.wonka.cellSize / 2
        self.y = app.height / 2 - 250 + app.wonka.cellSize / 2
        # Updated image path
        self.image = Image.open('golden_ticket.jpeg')
        self.image = CMUImage(self.image)
        self.poweredUp = False
        self.randomizePosition()
        self.wobble = 0

    def randomizePosition(self):
        self.row = random.randint(0, self.app.rows - 1)
        self.col = random.randint(0, self.app.cols - 1)

    def collided(self):
        wonka_node = self.app.wonka.extractNode()
        if wonka_node == (self.row, self.col):
            # Create candy particle effect when collected
            createCandyParticles(self.app, self.app.wonka.x, self.app.wonka.y, 20)
            return True
            
    def drawGoldenTicket(self, x, y):
        # Animated golden ticket with sparkle effect
        self.wobble = 5 * math.sin(self.app.colorTimer/10)
        drawImage(self.image, x - 20, y - 40 + self.wobble, width=35, height=35)
        
        # Draw sparkles around the ticket
        if self.app.colorTimer % 5 == 0:
            angle = self.app.colorTimer / 5
            sparkleX = x - 20 + 25 * math.cos(angle)
            sparkleY = y - 40 + self.wobble + 25 * math.sin(angle)
            drawStar(sparkleX, sparkleY, 5, 5, fill='yellow')

    def getCellLeftTop(self):
        cellSize = self.getCellSize()
        cellLeft = self.app.width / 2 - 250 + self.col * cellSize
        cellTop = self.app.height / 2 - 250 + self.row * cellSize
        return (cellLeft, cellTop)

    def getCellSize(self):
        cellSize = self.sideSize / self.app.rows
        return cellSize

class Candy:
    def __init__(self, app):
        self.app = app
        self.treats = set()
        self.sideSize = app.side
        # Updated image path
        self.image = Image.open('candy.jpeg')
        self.image = CMUImage(self.image)
        self.cellSize = self.getCellSize()
        self.x = app.width/2 -250 + self.cellSize / 2
        self.y = app.height/2 -250 + self.cellSize / 2
        # Create different candy colors
        self.candyColors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']

    def drawCandy(self, x, y):
        # Draw colorful candy with animation
        wobble = 2 * math.sin(self.app.colorTimer/10 + x/50)
        drawImage(self.image, x-20, y-40 + wobble, width=30, height=30)

    def convertNodeToCoords(self, node):
        row, col = node
        x = (self.app.width // 2 - 250 + col * self.app.wonka.cellSize +
                self.app.wonka.cellSize // 2)
        y = (self.app.height // 2 - 250 + row * self.app.wonka.cellSize + 
                self.app.wonka.cellSize // 2)
        return x, y
    
    def convertCoordsToNode(self, row, col):
        col = ((self.x-(self.app.width//2 -250 + self.cellSize // 2))
               //self.cellSize)
        row = ((self.y-(self.app.height//2 -250 + self.cellSize // 2))
                //self.cellSize)
        return (row, col)
        
    def getCellLeftTop(self):
        cellSize = self.getCellSize()
        cellLeft = self.app.width/2-250 + self.col * cellSize
        cellTop = self.app.height/2-250 + self.row * cellSize
        return (cellLeft, cellTop)

    def getCellSize(self):
        cellSize = self.sideSize / self.app.rows
        return cellSize

class Maze:
    def __init__(self, app):
        self.app = app
        self.rows = 8
        self.cols = 8
        self.shiftX = app.width/2 - 250
        self.shiftY = app.height/2 - 250
        self.table = dict()
        for row in range(self.rows):
            for col in range(self.cols):
                self.addNode((row, col))
        self.genMaze()
        # Maze colors for Wonka theme
        self.mazeColors = ['pink', 'purple', 'gold', 'coral', 'cyan']
        self.currentMazeColor = self.mazeColors[0]
        self.colorIndex = 0

    def addNode(self, node):
        self.table[node] = set()

    def addEdge(self, node1, node2):
        self.table[node1].add(node2)
        self.table[node2].add(node1)

    def genMaze(self):
        visited = set()
        return self.backtrack((0,0), visited)

    def backtrack(self, node, visited):
        r, c = node
        visited.add(node)
        neighbors = [(r,c-1), (r-1, c),(r,c+1),(r+1,c)]
        random.shuffle(neighbors)
        for neighbor in neighbors:
            nR, nC = neighbor
            if (0 <= nR < self.rows and 
                0 <= nC < self.cols and 
                neighbor not in visited):
                self.addEdge(node, neighbor)
                self.backtrack(neighbor, visited)

    def updateMazeColors(self):
        # Cycle through colors for the maze walls
        if self.app.colorTimer % 30 == 0:  # Change color every 30 steps
            self.colorIndex = (self.colorIndex + 1) % len(self.mazeColors)
            self.currentMazeColor = self.mazeColors[self.colorIndex]
        return self.currentMazeColor

    def draw(self, x, y, side):
        a = side/self.rows
        
        # Update the wall color
        wallColor = self.updateMazeColors()
        
        # Draw a fancy candy border around the maze
        borderWidth = 15
        borderOffset = 10
        for i in range(4):
            offset = i * 2
            color = ['pink', 'purple', 'gold', 'cyan'][i % 4]
            drawRect(
                self.shiftX - borderOffset - offset, 
                self.shiftY - borderOffset - offset,
                side + (borderOffset + offset) * 2, 
                side + (borderOffset + offset) * 2,
                fill=None, border=color, borderWidth=borderWidth/4
            )
            
        # Draw candy factory elements in the background
        for i in range(5):
            x = self.shiftX + random.randint(0, int(side))
            y = self.shiftY + random.randint(0, int(side))
            if (i % 2 == 0):
                # Draw candy machinery
                drawRect(x, y, 20, 15, fill='silver', opacity=0.2, align='center')
                drawRect(x, y-10, 5, 5, fill='red', opacity=0.2, align='center')
            else:
                # Draw candy bubbles
                size = 8 + 4*math.sin(self.app.colorTimer/10 + i)
                drawCircle(x, y, size, fill='pink', opacity=0.15)
        
        # Draw candy patterns at the corners
        cornerSize = 30
        for cx, cy in [(self.shiftX, self.shiftY), 
                      (self.shiftX + side, self.shiftY),
                      (self.shiftX, self.shiftY + side),
                      (self.shiftX + side, self.shiftY + side)]:
            starColor = ['gold', 'pink', 'purple', 'cyan'][int(cx + cy) % 4]
            drawStar(cx, cy, cornerSize, 5, fill=starColor)
        
        # Draw maze walls with animated colors
        for row in range(self.rows):
            for col in range(self.cols):
                node = (row, col)
                neighbors = self.table[node]
                leftN, topN, rightN, bottomN = [(row, col-1), (row-1, col),
                                               (row, col+1), (row+1, col)]

                # Create some pattern on the maze walls
                glowEffect = 2 * math.sin(self.app.colorTimer/10 + row + col)
                
                # Draw the walls with animated effects
                if topN not in neighbors:
                    drawLine(col*a + self.shiftX, row*a + self.shiftY, 
                             col*a + a + self.shiftX, row*a + self.shiftY, 
                             fill=wallColor, lineWidth=5 + glowEffect)
                    
                    # Add candy decorations on some walls
                    if (row + col) % 4 == 0:
                        candyX = col*a + a/2 + self.shiftX
                        candyY = row*a + self.shiftY
                        drawCircle(candyX, candyY, 3, fill='white')
                        
                if bottomN not in neighbors:
                    drawLine(col*a + self.shiftX, row*a + a + self.shiftY, 
                             col*a + a + self.shiftX, row*a + a + self.shiftY, 
                             fill=wallColor, lineWidth=5 + glowEffect)
                    
                    # Add candy decorations on some walls
                    if (row + col) % 4 == 1:
                        candyX = col*a + a/2 + self.shiftX
                        candyY = row*a + a + self.shiftY
                        drawCircle(candyX, candyY, 3, fill='white')
                        
                if leftN not in neighbors:
                    drawLine(col*a + self.shiftX, row*a + self.shiftY, 
                             col*a + self.shiftX, row*a + a + self.shiftY, 
                             fill=wallColor, lineWidth=5 + glowEffect)
                    
                    # Add candy decorations on some walls
                    if (row + col) % 4 == 2:
                        candyX = col*a + self.shiftX
                        candyY = row*a + a/2 + self.shiftY
                        drawCircle(candyX, candyY, 3, fill='white')
                        
                if rightN not in neighbors:
                    drawLine(col*a + a + self.shiftX, row*a + self.shiftY, 
                             col*a + a + self.shiftX, row*a + a + self.shiftY, 
                             fill=wallColor, lineWidth=5 + glowEffect)
                    
                    # Add candy decorations on some walls
                    if (row + col) % 4 == 3:
                        candyX = col*a + a + self.shiftX
                        candyY = row*a + a/2 + self.shiftY
                        drawCircle(candyX, candyY, 3, fill='white')

class OompaLoompa:
    def __init__(self, app):
        self.row = 5
        self.col = 5
        self.app = app
        # Updated to use Wonka character image temporarily for Oompa Loompa
        # (since we don't have a specific Oompa Loompa image)
        self.image = Image.open('oompa.png')
        self.image = CMUImage(self.image)
        self.animationFrame = 0
        self.animationTimer = 0
        
    def draw(self):
        # Animate the Oompa Loompa
        self.animationTimer += 1
        if self.animationTimer % 10 == 0:
            self.animationFrame = (self.animationFrame + 1) % 4
        
        # Add a bouncing effect
        bounce = 3 * math.sin(self.animationTimer/5)
        
        # Draw with slight size variation for "pulsing" effect
        scale = 1.0 + 0.1 * math.sin(self.animationTimer/10)
        width = 35 * scale
        height = 35 * scale
        
        drawImage(self.image, self.app.oompaLoompa_x, self.app.oompaLoompa_y + bounce, 
                  width=width, height=height, align='center')
        
        # Draw a colorful aura around the Oompa Loompa
        glowColors = ['orange', 'red', 'magenta']
        
        # Draw the glow effect
        for i in range(3):
            size = 8 + i*4
            opacity = 0.2 - i*0.05
            drawCircle(self.app.oompaLoompa_x, self.app.oompaLoompa_y + bounce, 
                       width/2 + size, fill=glowColors[i], opacity=opacity)

# Utility functions
def rightLeft(app):
    newDict = dict()
    for node in app.nodes:
        newDict[node] = set()
        for nodeValues in app.nodes[node]:
            nRow, nCol = node
            row, col = nodeValues
            dRow = row - nRow
            dCol = col - nCol
            if dRow == 0 and dCol == 1:
                newDict[node].add('right')
            elif dRow == 0 and dCol == -1:
                newDict[node].add('left')
            elif dRow == -1 and dCol == 0:
                newDict[node].add('up')
            elif dRow == 1 and dCol == 0:
                newDict[node].add('down')
    return newDict

def convertCoordsToNode(self, x, y):
    """This function converts screen coordinates to grid coordinates"""
    col = int((x - (self.app.width//2 - 250 + self.cellSize // 2)) // self.cellSize)
    row = int((y - (self.app.height//2 - 250 + self.cellSize // 2)) // self.cellSize)
    return (row, col)

# onAppStart initializes values every time the game restarts
def onAppStart(app):
    app.setMaxShapeCount(50000)  # or whatever number you need
    app.width = 1500
    app.height = 900
    app.rows = 8
    app.cols = 8
    app.side = 500
    app.maze = Maze(app)
    app.wonka = Wonka(app)  # Renamed from Scotty to Wonka
    app.stepsPerSecond = 70
    app.score = 0
    app.begin = False
    # Updated image path
    app.image = Image.open('wonka_splash.jpeg')
    app.image = CMUImage(app.image)
    app.nodes = app.maze.table
    app.newDict = rightLeft(app)
    app.canUp = False
    app.canDown = False
    app.canRight = False
    app.canLeft = False
    app.stepSize = 1
    app.stepsPerSecond = 30
    app.candy = Candy(app)  # Renamed from Treat to Candy
    app.goldenTicket = GoldenTicket(app)  # Renamed from Powerup to GoldenTicket
    # Vibrant Wonka background colors
    app.backgroundColors = ['lightpink', 'lightblue', 'orange', 'lightgreen', 'lavender']
    app.background = random.choice(app.backgroundColors)
    app.candyList = [[True,True,True,True,True,True, True, True],
                     [True,True,True,True,True,True, True, True],
                     [True,True,True,True,True,True, True, True],
                     [True,True,True,True,True,True, True, True],
                     [True,True,True,True,True,True, True, True],
                     [True,True,True,True,True,True, True, True],
                     [True,True,True,True,True,True, True, True],
                     [True,True,True,True,True,True, True, True]]
    app.updateScore = False
    app.win = False
    app.oompaLoompa = OompaLoompa(app)  # Renamed from Bagpipe to OompaLoompa
    app.tracker = dict()
    app.gameMode = 'Pause'
    app.oompaLoompa_web = generate_oompaLoompa_web(8,8)
    app.web_node = 64
    x,y = getGraphCoords(app.web_node)
    app.oompaLoompa_x = x
    app.oompaLoompa_y = y
    app.oompaLoompaSpeed = 2
    app.path = getWonkaPath(app,app.oompaLoompa_web,app.web_node)
    app.wonka_row, app.wonka_col = app.wonka.extractNode()
    # New Wonka-themed properties                                                    
    app.colorTimer = 0
    app.colorChangeFrequency = 30  # Change background every 30 steps
    app.chocolateRiverY = app.height - 50
    app.chocolateDrops = []
    app.candyParticles = []
    app.showSplashText = False
    app.splashTextTimer = 0
    
  #  app.wonkaQuotes = [
  #      "A little nonsense now and then is relished by the wisest men.",
  #      "We are the music makers, and we are the dreamers of dreams.",
  #     "So much time and so little to do. Wait a minute. Strike that. Reverse it.",
  #      "Invention, my dear friends, is 93% perspiration, 6% electricity, 4% evaporation, and 2% butterscotch ripple.",
 #       "The suspense is terrible... I hope it'll last!"
#  ]
  #  app.currentQuote = random.choice(app.wonkaQuotes)
    app.quoteTimer = 0
    
#### OOMPA LOOMPA ENEMY (Previously Bagpipe) #####

def generate_oompaLoompa_web(rows, cols):
    oompaLoompa_web = dict()
    for r in range(rows):
        for c in range(cols):
            key = r * 10 + c
            neighbors = []
            if c > 0:
                neighbors.append(key - 1)
            if c < cols - 1:
                neighbors.append(key + 1)
            if r > 0:
                neighbors.append(key - 10)
            if r < rows - 1:
                neighbors.append(key + 10)
            oompaLoompa_web[key] = sorted(neighbors)
    return oompaLoompa_web

def move_oompaLoompa(app, start, end):
    if app.win == False:
        if start == end:
            return
        dx = 1 if start < end and start // 10 == end // 10 else -1
        dy = 1 if start < end and start % 10 == end % 10 else -1
        if start // 10 == end // 10:
            app.oompaLoompa_x += dx * app.oompaLoompaSpeed
        if start % 10 == end % 10:
            app.oompaLoompa_y += dy * app.oompaLoompaSpeed

def getWonkaPath(app, graph, currNode):
    endNode = findWonkaNode(app, graph, app.wonka.x, app.wonka.y)
    path = bfs(currNode, endNode, [(currNode, [currNode],)], graph)
    return path

def findWonkaNode(app, graph, sX, sY):
    bestDistance = None
    bestNode = None
    if ((abs(app.oompaLoompa_x - app.wonka.x)) < 40 and 
        (abs(app.oompaLoompa_y - app.wonka.y)) < 40):
        app.gameMode = 'End'

    for parent in graph:
        for node in graph[parent]:
            x, y = getGraphCoords(node)
            length = distance(x, y, sX, sY)
            if bestDistance == None or length < bestDistance:
                bestDistance = length
                bestNode = node
    return bestNode

# BFS algorithm from Wikipedia
def bfs(start, end, queue, graph):
    newQueue = copy.deepcopy(queue)  
    visited = set() 
    while newQueue:
        node, path = newQueue.pop(0)
        if node == end:
            return path + [end]  
        if node not in visited:
            visited.add(node)  
            for neighbour in graph[node]:
                if neighbour not in path:
                    newQueue.append((neighbour, path + [neighbour]))
    return [start] if start != end else [end]

def getGraphCoords(node):
    x = 93.75 + 62.5*((node%10)+1) + 1500//4
    y = 62.5*((node//10)+1) + 125 + 62.5
    if node == 0:
        pass
    return (x, y)

def distance(x0, y0, x1, y1):
    return ((x0-x1)**2+(y0-y1)**2)**0.5

def update_position_and_path(app, path_index):
    x, y = getGraphCoords(app.path[path_index])
    app.web_node = app.path[path_index]
    app.oompaLoompa_x = x
    app.oompaLoompa_y = y
    app.path = getWonkaPath(app, app.oompaLoompa_web, app.web_node)

def chaseWonka(app):
    if len(app.path) == 1:
        update_position_and_path(app, 0)
    else:
        next_x, next_y = getGraphCoords(app.path[1])
        if abs(app.oompaLoompa_x - next_x) < 1 and abs(app.oompaLoompa_y - next_y) < 1:
            update_position_and_path(app, 1)
        else:
            move_oompaLoompa(app, app.path[0], app.path[1])

# Wonka-themed visual effects
def createChocolateDrop(app):
    if random.random() < 0.1:  # 10% chance each step
        app.chocolateDrops.append({
            'x': random.randint(0, app.width),
            'y': 0,
            'size': random.randint(10, 25),
            'speed': random.randint(3, 8)
        })

def updateChocolateDrops(app):
    for drop in app.chocolateDrops[:]:
        drop['y'] += drop['speed']
        if drop['y'] > app.chocolateRiverY:
            app.chocolateDrops.remove(drop)
            # Create splash effect
            createCandyParticles(app, drop['x'], app.chocolateRiverY, random.randint(3, 8))

def createCandyParticles(app, x, y, count):
    for _ in range(count):
        app.candyParticles.append({
            'x': x,
            'y': y,
            'dx': random.uniform(-3, 3),
            'dy': random.uniform(-8, -3),
            'size': random.randint(3, 8),
            'color': random.choice(['pink', 'purple', 'yellow', 'cyan', 'lime']),
            'life': random.randint(20, 40)
        })

def updateCandyParticles(app):
    for particle in app.candyParticles[:]:
        particle['x'] += particle['dx']
        particle['y'] += particle['dy']
        particle['dy'] += 0.3  # gravity
        particle['life'] -= 1
        if particle['life'] <= 0:
            app.candyParticles.remove(particle)

def drawWonkaEffects(app):
    # Draw chocolate river
    drawRect(0, app.chocolateRiverY, app.width, app.height - app.chocolateRiverY, 
             fill='brown')
             
    # Draw ripples on chocolate river
    for i in range(15):
        x = (app.chocolateRiverY + app.colorTimer/2) % app.width
        drawOval(x + i*100, app.chocolateRiverY + 10, 80, 20, 
                 fill='saddlebrown')
    
    # Draw falling chocolate drops
    for drop in app.chocolateDrops:
        drawOval(drop['x'], drop['y'], drop['size'], drop['size']*1.5, 
                 fill='brown')
    
    # Draw candy particles
    for particle in app.candyParticles:
        drawCircle(particle['x'], particle['y'], particle['size'], 
                   fill=particle['color'])
    
    # Draw rainbow mist at the top
    for i in range(30):
        opacity = 0.1 + 0.05 * math.sin(app.colorTimer/20 + i/5)
        colors = ['pink', 'purple', 'blue', 'cyan', 'green', 'yellow', 'orange', 'red']
        drawRect(i*60, 0, 50, 100, 
                 fill=colors[i % len(colors)],
                 opacity=opacity)
    
    # Display Wonka quote
    if app.begin and app.quoteTimer < 150:
        drawRect(app.width/2, 250, app.width*0.7, 80, 
                 fill='purple', opacity=0.8, align='center')
        #drawLabel(app.currentQuote, app.width/2, 250, size=20, 
         #         font='cursive', fill='white', bold=True)







# Draw fun Wonka-themed splash text
def drawSplashText(app):
    if app.showSplashText:
        # Create a background for the text
        drawRect(app.width/2, app.height/2 - 100, 500, 100, 
                 fill='purple', 
                 opacity=0.9, align='center', border='gold', borderWidth=3)
                 
        # Draw stars around the text
        for i in range(8):
            angle = app.splashTextTimer/10 + i * math.pi/4
            x = app.width/2 + 280 * math.cos(angle)
            y = app.height/2 - 100 + 70 * math.sin(angle)
            colors = ['gold', 'pink', 'purple', 'cyan', 'magenta', 'yellow', 'orange', 'red']
            drawStar(x, y, 15, 5, fill=colors[i % len(colors)])
            
        # Draw the text with a slight wobble
    #    wobble = 2 * math.sin(app.splashTextTimer/5)
    #    phrases = ["Pure Imagination!", "Golden Ticket Found!", 
    #               "Scrumdiddlyumptious!", "Candy Bonanza!", "Wonka Magic!"]
        
       # phrase = phrases[app.splashTextTimer % len(phrases)]
        #drawLabel(phrase, app.width/2 + wobble, app.height/2 - 100 + wobble, 
        #          size=40, font='cursive', fill='white', bold=True)

def drawGraph(graph):
    for parent in graph:
        for node in graph[parent]:
            x,y = getGraphCoords(node)
            # Draw with Wonka colors
            colors = ['pink', 'purple', 'gold', 'cyan', 'magenta']
            color = colors[node % len(colors)]
            drawOval(x, y, 10, 10, fill=color)

def redrawAll(app):
    # Draw background with candy-stripe pattern
    drawRect(0, 0, app.width, app.height, fill=app.background)
    
    for i in range(20):
        stripeWidth = 40
        opacity = 0.2 + 0.1 * math.sin(app.colorTimer/20 + i)
        colors = ['pink', 'purple', 'gold', 'cyan', 'magenta']
        drawRect(i*stripeWidth*2, 0, stripeWidth, app.height, 
                 fill=colors[i % len(colors)], opacity=opacity)
    
    # Wonka-themed visual effects
    drawWonkaEffects(app)
    
    # Draw splash text if needed
    if app.showSplashText:
        drawSplashText(app)
        
    # Game title with candy-colored text
    for i in range(5):
        offset = 3 * math.sin(app.colorTimer/10 + i)
        colors = ['magenta', 'purple', 'cyan', 'gold', 'red']
        drawLabel('WONKA-MAN!', app.width/2 + offset, 50 + offset, size=70, 
                  fill=colors[i], font='cursive', bold=True)
    
    drawLabel('WONKA-MAN!', app.width/2, 50, size=65, 
              fill='gold', font='cursive', bold=True)

    if app.gameMode == 'End':
        drawRect(app.width/2, 800, 700, 100, fill='purple', 
                 opacity=0.8, align='center')
        drawLabel('Oh no! Caught by an Oompa Loompa! Press r to restart.', 
                  app.width/2, 800, size=40, fill='white', font='cursive')

    if app.begin:
        # Score display with candy styling
        drawRect(app.width/2, 150, 300, 60, 
                 fill='purple', 
                 opacity=0.8, align='center', border='gold', borderWidth=3)
        drawLabel(f'SCORE: {app.wonka.score}', app.width/2, 150, size=35, 
                  font='cursive', fill='white', bold=True)
        
        # Maze with candy border
        app.maze.draw(app.width/2, app.height/2, app.side)
        app.wonka.draw()
        app.oompaLoompa.draw()
        
        if app.win == True:
            drawRect(app.width/2, 800, 800, 100, 
                     fill='purple', 
                     opacity=0.9, align='center')
            drawLabel('Pure Imagination! You Win! Press r to play again.', 
                      app.width/2, 800, size=45, font='cursive', fill='white', bold=True)
        
        # Draw candies and golden tickets
        for row in range(app.rows):
            for col in range(app.cols):
                app.candyList[0][0] = False
                if app.wonka.extractNode() == (row, col):
                    app.candyList[row][col] = False

                if app.candyList[row][col] == True:
                    app.candy.drawCandy(app.candy.x + col * 62.5, 31.25 + 
                                      app.candy.y + row * 62.5)

                if app.goldenTicket.collided():
                    app.goldenTicket.poweredUp = True

                if app.goldenTicket.poweredUp == False:
                    # Only draw the golden ticket at its current position
                    if (app.goldenTicket.row, app.goldenTicket.col) == (row, col):
                        app.goldenTicket.drawGoldenTicket(app.goldenTicket.x + col * 62.5, 
                                                       31.25 + app.goldenTicket.y + row * 62.5)

    else:
        # This is the start screen section
        try:
            # Try to draw the image, but have a fallback if it fails
            drawImage(app.image, app.width/2, app.height/2, align='center')
        except:
            # Fallback in case image loading fails
            drawRect(app.width/2, app.height/2, 400, 300, fill='purple', opacity=0.6, align='center')
            drawLabel('Wonka', app.width/2, app.height/2, size=50, fill='gold', font='cursive', bold=True)
        
        # Start button with candy styling
        buttonColor = 'magenta'
        drawRect(app.width/2, 120, 400, 60, fill=buttonColor, 
                 opacity=0.9, align='center', border='gold', borderWidth=3)
        drawLabel('Click Wonka to Enter the Factory!', app.width/2, 120, size=30, 
                  fill='white', font='cursive', bold=True)
                  
        # Add spacebar instruction
        drawRect(app.width/2, app.height - 100, 400, 60, fill='purple', 
                 opacity=0.9, align='center', border='gold', borderWidth=3)
        drawLabel('Press SPACEBAR to Start!', app.width/2, app.height - 100, size=30, 
                  fill='white', font='cursive', bold=True)

def onKeyPress(app, key):
    # Add space bar to start the game
    if key == 'space' and not app.begin:
        app.begin = True
        app.wonka.updateCoords()
        app.gameMode = 'Start'
        app.quoteTimer = 0
     #   app.currentQuote = random.choice(app.wonkaQuotes)
        return

    # Original movement controls
    app.canUp = False
    app.canDown = False
    app.canLeft = False
    app.canRight = False

    if app.wonka.touchNode():
        dirs = app.newDict[app.wonka.extractNode()]
        app.canUp = 'up' in dirs
        app.canDown = 'down' in dirs
        app.canLeft = 'left' in dirs
        app.canRight = 'right' in dirs

    if key == 'right' and app.canRight:
        app.wonka.col += 1
        app.wonka.direction = 'right'
        # Create candy dust effect when moving
        createCandyParticles(app, app.wonka.x - 10, app.wonka.y, 2)
    if key == 'up' and app.canUp:
        app.wonka.row -= 1
        app.wonka.direction = 'up'
        createCandyParticles(app, app.wonka.x, app.wonka.y + 10, 2)
    if key == 'down' and app.canDown:
        app.wonka.row += 1
        app.wonka.direction = 'down'
        createCandyParticles(app, app.wonka.x, app.wonka.y - 10, 2)
    if key == 'left' and app.canLeft:
        app.wonka.col -= 1
        app.wonka.direction = 'left'
        createCandyParticles(app, app.wonka.x + 10, app.wonka.y, 2)
    
    # Reset game when 'r' is pressed
    if key == 'r':
        onAppStart(app)
   
    # Change background color with 'c' key
    if key == 'c':
        app.background = random.choice(app.backgroundColors)
    
    # Change Oompa Loompa speed with 's' key
    if key == 's':
        app.oompaLoompaSpeed = (app.oompaLoompaSpeed % 5) + 1
    
    # Update player position
    app.wonka.updateCoords()

def onMousePress(app, mouseX, mouseY):
    if (app.width/2 - 220 < mouseX < app.width/2 + 200 and app.height/2 - 
        150 < mouseY < app.height/2 + 150):
        app.begin = True
        app.wonka.updateCoords()
        app.gameMode = 'Start'
        app.quoteTimer = 0
    #    app.currentQuote = random.choice(app.wonkaQuotes)

def onStep(app):
    # Update animation timers and effects
    app.colorTimer += 1
    
    # Cycle background colors
    if app.colorTimer % app.colorChangeFrequency == 0:
        app.background = random.choice(app.backgroundColors)
    
    # Update quote timer
  #  if app.begin:
   #     app.quoteTimer += 1
  #      if app.quoteTimer > 300:  # Change quote every 10 seconds (at 30fps)
   #         app.currentQuote = random.choice(app.wonkaQuotes)
    #        app.quoteTimer = 0
    
    # Create and update visual effects
    createChocolateDrop(app)
    updateChocolateDrops(app)
    updateCandyParticles(app)
    
    # If player wins, create a celebration effect
    if app.win:
        if app.colorTimer % 5 == 0:
            createCandyParticles(app, random.randint(0, app.width), 
                               random.randint(0, app.height), 
                               random.randint(3, 8))
    
    # Update score
    app.wonka.score = -1

    if app.goldenTicket.poweredUp == True:
        app.wonka.score += 2
        
    for row in range(app.rows):
        for col in range(app.cols):
            if app.candyList[row][col] == False:
                app.wonka.score += 1
    
    # Check for win condition
    if app.wonka.score >= 65:
        app.win = True

    # Update enemy AI
    if app.gameMode == 'Start':
        chaseWonka(app)
        
    app.wonka_row, app.wonka_col = app.wonka.extractNode()
                                                    
    # Show splash text randomly
    if random.random() < 0.001 and not app.showSplashText:  # Approx once every 30 seconds
        app.showSplashText = True
        app.splashTextTimer = 0
        
    if app.showSplashText:
        app.splashTextTimer += 1
        if app.splashTextTimer > 60:  # Show for 2 seconds
            app.showSplashText = False

def main():
    # The function that starts our Wonka-Man game!
    runApp()

main()

cmu_graphics.run()





# 'r' - restart the game
# 'c' - change the background color
# 's' - adjust the Oompa Loompa's speed
# Arrow keys - move Wonka through the maze