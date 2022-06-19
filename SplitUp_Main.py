import pygame
import sys
import random
import math


# base setup 
pygame.init()

WIDTH = 1280
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Split up")



# hard setup (class, def)
class Ball: 
    def __init__(self,color,position,movement):
        self.position = position
        self.radius   = 20
        self.movement = movement 
        self.speed = 1.5
        self.color    = color
    def append(self):
        pygame.draw.circle(screen , self.color, (self.position[0],self.position[1]),self.radius)
    def move(self,box):
        global Score
        global Power

        self.position[0] += self.movement[0]*self.speed
        self.position[1] += self.movement[1]*self.speed

        if self.position[0]-self.radius < 0 or self.position[0]+self.radius > box.position[0]+box.size[0]:
            self.movement[0] = -self.movement[0]
            Score+=random.randint(1,25)
            Power+=10+Score*0.05
        if self.position[1]-self.radius < 0 or self.position[1]+self.radius > box.position[1]+box.size[1]:
            self.movement[1] = -self.movement[1]
            Score+=1
            Power+=random.randint(1,50)

class Box():
    def __init__(self,position,size,thick,color):
        self.position = position 
        self.size     = size
        self.thick    = thick
        self.color    = color
    def append(self):
        pygame.draw.rect(screen, self.color, (self.position[0],self.position[1],self.size[0],self.size[1]),self.thick)

class Text:
    def __init__(self,text,position,size,color):
        self.text = text
        self.position = position
        self.size = size
        self.color = color 
        font = pygame.font.SysFont(None,self.size)
        self.text = font.render(self.text,True,self.color)
    def append(self):
        screen.blit(self.text,(self.position[0],self.position[1]))

def ShowBallInfo(box):
    if CheckTHEBALL():

        InfoBox = Box([box.position[0]+20,345],[box.size[0]-40,350-20],5,'yellow')
        BallID = Text(f'ID: {TheBall}',[box.position[0]+45,380],35,'white')
        BallMovement = Text(f'Movement: {round(Balls[TheBall].movement[0],2)} | {round(Balls[TheBall].movement[1],2)}',[box.position[0]+45,415],35,'white')
        BallRadius = Text(f"Radius: {round(Balls[TheBall].radius,2)}",[box.position[0]+45,450],35,'white')

        InfoBox.append()
        BallID.append()
        BallMovement.append()
        BallRadius.append()

        pygame.draw.circle(screen, 'yellow', (Balls[TheBall].position[0],Balls[TheBall].position[1]),Balls[TheBall].radius+3,4)

def ClickBall():
    global TheBall

    for ball in Balls:
        if abs(mouse[0] - Balls[ball].position[0]) <= Balls[ball].radius  and abs(mouse[1] - Balls[ball].position[1]) <= Balls[ball].radius:
            TheBall = ball
            return True
    else:
        return False

def CheckBallCollision():
    global CountBalls

    ResetLoop = False
    for first in Balls:
        for second in Balls:
            if Balls[first].color != Balls[second].color and first != second and abs(Balls[first].position[0]-Balls[second].position[0]) <= Balls[first].radius + Balls[second].radius and abs(Balls[first].position[1]-Balls[second].position[1]) <= Balls[first].radius + Balls[second].radius:
                Balls.pop(first)
                Balls.pop(second)
                CountBalls -= 2
                ResetLoop = True
                CheckGen()
                break

        if ResetLoop == True:
            ResetLoop = False
            break

def ShowBaseInfo(box):

    ScoreText = Text(f'Score: {Score}',[box.position[0]+45,45],45,'white')
    BallsText = Text(f'Balls: {CountBalls} / {MaxBalls}',[box.position[0]+45,80],45,'white')

    ScoreText.append()
    BallsText.append()

def CheckTHEBALL():
    if TheBall != None and TheBall in Balls:
        return True
    else:
        return False

def CreateBall():
    global Balls

    if CountBalls < MaxBalls:
        while True:
            ID = f'{random.randint(0,MaxBalls)}'
            if ID not in Balls:
                Balls.setdefault(ID,Ball(Balls[TheBall].color,[Balls[TheBall].position[0],Balls[TheBall].position[1]],[-Balls[TheBall].movement[0],-Balls[TheBall].movement[1]]))
                break

def BreakAngle():
    global Balls
    if Balls[TheBall].movement[0] != 0 and Balls[TheBall].movement[1] != 0:
        Balls[TheBall].movement[0] = -Balls[TheBall].movement[0]
    else:
        X = Balls[TheBall].movement[0]
        Y = Balls[TheBall].movement[1]
        Balls[TheBall].movement[0] = Y
        Balls[TheBall].movement[1] = X

def CreateBaseGen():
    global BaseGen

    for ball in Balls:
        if Balls[ball].color not in BaseGen:
            BaseGen.setdefault(f"{Balls[ball].color}",0)

def CheckGen():
    global Works
    global Winner

    for gen in BaseGen:
        BaseGen[gen] = 0

    for ball in Balls:
        if Balls[ball].color in BaseGen:
            BaseGen[Balls[ball].color]+=1
    
    for gen in BaseGen:
        if BaseGen[gen] == 0 :
            Works = False
            Winner = 'Bot'
            break
        else:
            Works = True

def NewGame():
    global Balls
    global TheBall
    global Score
    global CountBalls 
    global MaxBalls 
    global BaseGen
    global Works
    global Power
    global Anti

    Balls  = {
    '0':Ball('green',[random.randint(50,int(WIDTH-WIDTH/3-50)),random.randint(50,HEIGHT-50)],[random.choice([1,1,1,1,-1,-1,0]),random.choice([1,-1])]),
    '1':Ball('red',[random.randint(50,int(WIDTH-WIDTH/3-50)),random.randint(50,HEIGHT-50)],[random.choice([1,-1]),random.choice([1,-1])])
    }
    TheBall = None
    Score = 0
    CountBalls = 2
    MaxBalls = 4
    BaseGen = {}
    Power = 100
    Anti = 20
    CreateBaseGen()
    Works = True

def ProcessBar():
    global Anti
    global Works
    global Winner

    if Works == True:
        Anti += random.randint(5,25)/10

    Total = Anti+Power

    Position = [SecondBox.position[0]+45,250]
    PowerBarSize = [(Power/Total)*(SecondBox.size[0]-90),40]
    AntiBarSize = [(Anti/Total)*(SecondBox.size[0]-90),40]

    pygame.draw.rect(screen, 'yellow',(Position[0],Position[1],PowerBarSize[0],PowerBarSize[1]))
    pygame.draw.rect(screen, 'red',(Position[0]+PowerBarSize[0],Position[1],AntiBarSize[0],AntiBarSize[1]))

    if Power/Total >= 0.9:
        Winner = 'Player'
        Works = False
    elif Anti/Total >= 0.9:
        Winner = 'Bot'
        Works = False

# base stats
Clock   = pygame.time.Clock()
Balls  = {
    '0':Ball('green',[random.randint(50,int(WIDTH-WIDTH/3-50)),random.randint(50,HEIGHT-50)],[random.choice([1,1,1,1,-1,-1,0]),random.choice([1,-1])]),
    '1':Ball('red',[random.randint(50,int(WIDTH-WIDTH/3-50)),random.randint(50,HEIGHT-50)],[random.choice([1,-1]),random.choice([1,-1])])
}

FirstBox = Box([0,0],[WIDTH-WIDTH/3,HEIGHT],10,'white') # the bigest box on this game
SecondBox = Box([FirstBox.position[0]+FirstBox.size[0]+10,0],[WIDTH/3-10,HEIGHT],10,'white') # smaller than first box 
TheBall = None
Score = 0
CountBalls = 2
MaxBalls = 4
BaseGen = {}
CreateBaseGen()
Power = 100
Works = True
EndButton = {
    'size':[250,80],
    'position':[WIDTH/2-250/2,HEIGHT/2-40],
    'base_color':'gray',
    'color':'gray',
    'change_color':'yellow'
}
PlayAgain = Text('Play again!',[EndButton['position'][0]+EndButton['size'][0]/2-125/2,EndButton['position'][1]+EndButton['size'][1]/2-8],35,'blue')
Anti = 20

while True:
    
    # control
    CountBalls = len(Balls)
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if Works == True:
            if event.type == pygame.MOUSEBUTTONDOWN and ClickBall():
                pass # just for a click :)

            if event.type == pygame.MOUSEBUTTONDOWN and CheckTHEBALL():
                BreakAngle()
                CreateBall()
        else:
            if mouse[0] >= EndButton['position'][0] and mouse[0] <= EndButton['position'][0]+EndButton['size'][0] and mouse[1] >= EndButton['position'][1] and mouse[1] <= EndButton['position'][1]+EndButton['size'][1] and event.type == pygame.MOUSEBUTTONDOWN:
                NewGame()
            elif mouse[0] >= EndButton['position'][0] and mouse[0] <= EndButton['position'][0]+EndButton['size'][0] and mouse[1] >= EndButton['position'][1] and mouse[1] <= EndButton['position'][1]+EndButton['size'][1]:
                EndButton['color'] = EndButton['change_color']
            else:
                EndButton['color'] = EndButton['base_color'] 
            
        

    # draw
    FirstBox.append()
    SecondBox.append()

    for ball in Balls:
        Balls[ball].append()
        if Works == True:
            Balls[ball].move(FirstBox) # check collision with the first box

    ShowBallInfo(SecondBox)
    ShowBaseInfo(SecondBox)

    CheckBallCollision()
    
    ProcessBar()

    
    if Works == False:
        pygame.draw.rect(screen, EndButton['color'], (EndButton['position'][0],EndButton['position'][1],EndButton['size'][0],EndButton['size'][1]))
        pygame.draw.rect(screen, 'white', (EndButton['position'][0],EndButton['position'][1],EndButton['size'][0],EndButton['size'][1]),5)
        PlayAgain.append()
        Win = Text(f'{Winner} win!',[EndButton['position'][0]+EndButton['size'][0]/2-125/2,EndButton['position'][1]+EndButton['size'][1]/2-90],35,'white')
        Win.append()
    # display
    pygame.display.update()
    screen.fill("black")
    Clock.tick(60)