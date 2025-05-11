import pygame
import math
import time
import random
import os


def jumpingGameMain():

    gameDisplay = pygame.display.set_mode((1000, 500))

    class Arena():

        artChance = 0.3

        arena = None
        rightWallImages = []
        leftWallImages = []
        groundImages = []
        skyImages = []

        for i in range(3):
            image = pygame.image.load(os.path.join("jumpingGameFiles","wall"+str(i+1)+".png"))
            image = pygame.transform.scale(image, (400, 500))
            leftWallImages.append(image)
            rightWallImages.append(pygame.transform.flip(image, True, False))

        for i in range(2):
            image = pygame.image.load(os.path.join("jumpingGameFiles","ground"+str(i+1)+".png"))
            image = pygame.transform.scale(image, (1000, 200))
            groundImages.append(image)

        rightWallImage = random.choice(rightWallImages)
        leftWallImage = random.choice(leftWallImages)
        groundImage = random.choice(groundImages)
        leftAbove = random.randint(0,1)
        rightAbove = random.randint(0,1)
        light = random.random()
        skyColor = (random.randint(100,200)*light,random.randint(150,200)*light,random.randint(200,255)*light)

        def __init__(self):
            self.firstFrame = True
            self.radius=400
            if random.random()<self.artChance:
                Arena.rightWallImage = random.choice(self.rightWallImages)
                Arena.rightAbove = random.randint(0,1)
            if random.random()<self.artChance:
                Arena.leftWallImage = random.choice(self.leftWallImages)
                Arena.leftAbove = random.randint(0,1)
            if random.random()<self.artChance:
                Arena.groundImage = random.choice(self.groundImages)
            if random.random()<self.artChance:
                light = random.random()
                print(Arena.skyColor)
                Arena.skyColor = (random.randint(50,150)*light,random.randint(150,200)*light,random.randint(200,255)*light)

        def update(self):
            if self.radius>100:
                self.radius-=0.5

        def draw(self):
            pygame.draw.rect(gameDisplay, Arena.skyColor, (0, 0, 1000, 500), 0)
            if not self.leftAbove:
                gameDisplay.blit(self.leftWallImage, (100-self.radius, 0))
            if not self.rightAbove:
                gameDisplay.blit(self.rightWallImage, (500+self.radius, 0))
            gameDisplay.blit(self.groundImage, (0, 300))
            if self.leftAbove:
                gameDisplay.blit(self.leftWallImage, (100-self.radius, 0))
            if self.rightAbove:
                gameDisplay.blit(self.rightWallImage, (500+self.radius, 0))

    class Character():

        radius = 10

        def __init__(self, x, y):
            self.x = x-self.radius
            self.y = y-self.radius
            self.xv=0
            self.yv=0

        def update(self):

            if(self.x+self.radius)>(500+Arena.arena.radius):
                self.x=500+Arena.arena.radius-self.radius
                self.xv=-1
                self.yv-=0.1
            if(self.x-self.radius)<(500-Arena.arena.radius):
                self.x=500-Arena.arena.radius+self.radius
                self.xv=1
                self.yv-=0.1

    class Player(Character):

        players = []

        blueImages = []
        redImages = []

        for i in range(2):
            image = pygame.image.load(os.path.join("jumpingGameFiles","blue"+str(i+1)+".png"))
            image = pygame.transform.scale(image, (40, 40))
            blueImages.append(image)
        for i in range(1):
            image = pygame.image.load(os.path.join("jumpingGameFiles","red"+str(i+1)+".png"))
            image = pygame.transform.scale(image, (40, 40))
            redImages.append(image)

        def __init__(self,x,y,side, controls, colors, AI):
            super().__init__(x,y)
            self.side = side
            self.controls = controls
            self.color = colors[0]
            self.lineColor = colors[1]
            self.AI = AI
            self.facing=1#random.randint(0,1)
            if colors[2]=="blue":
                self.image = random.choice(self.blueImages)
            if colors[2]=="red":
                self.image = random.choice(self.redImages)

        def move(self, pressed):

            if(self.y<400-self.radius):
                self.yv+=0.025
            
            self.xv=self.xv*0.975
            self.x+=self.xv*5
            self.y+=self.yv*5

            if self.AI:
                """
                opponent = Player.players[0] #usually
                if random.randint(0,20)==0:
                    if opponent.y+opponent.yv*10==self.y+self.yv*10:
                        self.facing = random.randint(0,1)
                    self.facing=opponent.y+opponent.yv*10>self.y+self.yv*10
                """
                if random.randint(0,20)==0:
                    self.facing =random.randint(0,1)
                #"""
            if(pressed[self.controls[0]] or (self.AI and self.facing)):
                self.xv-=0.025
            if(pressed[self.controls[2]] or (self.AI and not self.facing)):
                self.xv+=0.025
            if(pressed[self.controls[3]]):
                self.yv+=0.025
            if(self.y>=400-self.radius):
                self.yv=0
                self.y=400-self.radius
                if(pressed[self.controls[1]] or (self.AI and random.randint(1,50)==1)):
                    self.yv=-1.5

        def update(self):
            super().update()

            for player in Player.players:
                if not player.side==self.side:
                    if(self.x-self.radius<player.x+player.radius and self.x+self.radius>player.x-player.radius):
                        if(self.y-self.radius<player.y+player.radius and self.y+self.radius>player.y-player.radius):
                            if self.xv>player.xv:
                                self.xv=1
                                player.xv=-1
                            else:
                                self.xv=1
                                player.xv=-1
                        elif(self.y>player.y+self.radius):
                            Player.players.remove(self)
                            Ball.ball.score+=player.side*10
                        elif(self.y<player.y-self.radius):
                            Player.players.remove(player)
                            Ball.ball.score+=self.side*10

        def draw(self):
            pygame.draw.rect(gameDisplay, self.lineColor, (self.x-0.5-9.5*self.side, self.y, 1, -self.y+400), 0)
            #pygame.draw.rect(gameDisplay, self.color, (self.x-self.radius, self.y-self.radius, self.radius*2, self.radius*2), 0)
            gameDisplay.blit(self.image, (self.x-self.radius*2, self.y-self.radius*2))

    class Ball():
        def __init__(self):
            self.score = 0
            
        def draw(self):
            pygame.draw.rect(gameDisplay, (250+max(min(self.score,0),-250), 250-min(250,abs(self.score)), 250-min(250,max(0,self.score))), (490+self.score, 440, 20, 20), 0)

    def restart():
        Arena.arena=Arena()
        Player.players=[]
        colors1 = [(0,0,255),(0,255,255),"blue"]
        colors2 = [(255,0,0),(255,255,0),"red"]
        Player.players.append(Player(200+Character.radius,400,-1,[pygame.K_a,pygame.K_w,pygame.K_d,pygame.K_s], colors=colors1, AI=0))
        Player.players.append(Player(800+Character.radius,400,1,[pygame.K_LEFT,pygame.K_UP,pygame.K_RIGHT,pygame.K_DOWN], colors=colors2, AI=0))

    clock = pygame.time.Clock()
    Ball.ball = Ball()

    restart()
    victoryFrames=0

    jump_out = False
    while jump_out == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jump_out = True
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_ESCAPE]: #pygame.K_q
                    jump_out = True

        clock.tick(120)

        if Arena.arena.firstFrame == True:
            time.sleep(0.1)
        if len(Player.players)<2 and not victoryFrames:
            victoryFrames = 20
        if victoryFrames:
            victoryFrames-=1
            time.sleep(0.2/(victoryFrames+1))
            if victoryFrames==0:
                restart()

        pressed = pygame.key.get_pressed()
        for player in Player.players:
            player.move(pressed)
        Arena.arena.update()
        for player in Player.players:
            player.update()

        Arena.arena.draw()
        Ball.ball.draw()
        for player in Player.players:
            player.draw()

        pygame.display.update()
        Arena.arena.firstFrame = False


    return


if __name__ == "__main__":
    jumpingGameMain()