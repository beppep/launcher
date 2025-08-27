import pygame
import time
import random
import os
import math


def blastGameMain():

    clock = pygame.time.Clock()
    pygame.init()
    infoObject = pygame.display.Info()
    screenResolution = (infoObject.current_w, infoObject.current_h)
    gameDisplay = pygame.display.set_mode(screenResolution,) # idk if i need this

    pygame.font.init() # you have to call this at the start, 
    myfont = pygame.font.SysFont('Calibri', 100)
    myfont2 = pygame.font.SysFont('Calibri', 200)

    class Sound():
        v = 0.1
        pygame.mixer.init(buffer=32)
        laserSound = pygame.mixer.Sound(os.path.join(filepath,"sounds", "pew.wav"))
        laserSound.set_volume(0.2*v)
        hitSound = pygame.mixer.Sound(os.path.join(filepath,"sounds", "hit1.wav"))
        hitSound.set_volume(v)
        blastSound = pygame.mixer.Sound(os.path.join(filepath,"sounds", "blast.wav"))
        blastSound.set_volume(v)
        
        pygame.mixer.music.load(os.path.join(filepath,"sounds", "music.mp3")) #must be wav 16bit and stuff?
        pygame.mixer.music.set_volume(v)
        pygame.mixer.music.play(-1)

    def signedAngleDiff(a,b):
        diff = b - a
        return (diff + math.pi) % math.tau - math.pi

    class Game():

        #bgImage = pygame.image.load(os.path.join(filepath, "space.png"))
        #bgImage = pygame.transform.scale(bgImage, (screenResolution[0]//2, screenResolution[1]//2))

        def __init__(self):
            self.over = False
            self.totalKills = 0
            self.camera = Camera()
            self.player = Player(0,0)
            self.enemies = []
            self.bullets = []
            self.items = []
            self.particles = []

        def update(self):
            self.player.update()
            for enemy in self.enemies:
                enemy.update()
            for bullet in self.bullets:
                bullet.update()
            for item in self.items:
                item.update()
            for particle in self.particles:
                particle.update()
            self.camera.update()

            if random.random()<0.01:
                cls = random.choices([Scout, Cruiser],[10,1], k=1)[0]
                a = random.random()*math.tau
                self.enemies.append(cls(self.player.x++math.cos(a)*500,self.player.y+math.sin(a)*500))

        def draw(self):
            gameDisplay.fill((0,0,0))
            self.camera.drawBg()
            for particle in self.particles:
                particle.draw()
            for item in self.items:
                item.draw()
            for enemy in self.enemies:
                enemy.draw()
            for bullet in self.bullets:
                bullet.draw()
            self.player.draw()
            self.camera.display()

            if self.over:
                textsurface = myfont2.render("GAME OVER", True, (220,220,220))
                textsurface2 = myfont.render("Score: "+str(self.totalKills), True, (110,110,110))
                gameDisplay.blit(textsurface,(screenResolution[0]//2 -500,0))
                gameDisplay.blit(textsurface2,(screenResolution[0]//2 -200,screenResolution[1]-100))
            

    class Camera():

        def __init__(self):
            self.x = 0
            self.y = 0
            self.shake = 0
            self.shakeX = 0
            self.shakeY = 0
            self.colorflash = [0,0,0]
            self.canvas = pygame.Surface((screenResolution[0]//2,screenResolution[1]//2))
            self.starPositions = []
            for i in range(100):
                raw = random.expovariate(3) # 2 to 5 is cool. higher is more distant stars.
                scaled = raw / (1 + raw) # want speed distributed with more 0 spd than 1 spd paralax
                self.starPositions.append((random.randint(0,screenResolution[0]//2),random.randint(0,screenResolution[1]//2),scaled)) #x,y,"z" ie spd

        def update(self):
            lerp = 0.2
            self.x = game.player.x*lerp + self.x*(1-lerp)
            self.y = game.player.y*lerp + self.y*(1-lerp)
            if self.shake>0:
                self.shakeX = random.randint(-self.shake, self.shake)
                self.shakeY = random.randint(-self.shake, self.shake)
                self.shake-=2
            elif 1:
                self.shakeX = 0
                self.shakeY = 0

        def setShake(self, n):
            self.shake = max(self.shake, n)

        def setColorflash(self, color):
            for i in range(3):
                self.colorflash[i] = max(self.colorflash[i],color[i])

        def drawLine(self, color, pos1, pos2, width):
            pos1 = (screenResolution[0]//4-self.x-self.shakeX+pos1[0], screenResolution[1]//4-self.y-self.shakeY+pos1[1])
            pos2 = (screenResolution[0]//4-self.x-self.shakeX+pos2[0], screenResolution[1]//4-self.y-self.shakeY+pos2[1])
            pygame.draw.line(self.canvas, color, pos1, pos2, width)

        def blitImage(self, image, pos, originPos):
            # calculate the upper left origin of the rotated image
            origin = (int(screenResolution[0]//4-self.x-self.shakeX + pos[0] - originPos[0]), int(screenResolution[1]//4-self.y-self.shakeY + pos[1] - originPos[1]))
            self.canvas.blit(image, origin)

        def blitRotate(self, image, pos, originPos, angle):

            #ifx rad ddeg
            angle = -angle*180/math.pi +180 #-?

            # calcaulate the axis aligned bounding box of the rotated image
            w, h       = image.get_size()
            box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
            box_rotate = [p.rotate(angle) for p in box]
            min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
            max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

            # calculate the translation of the pivot 
            pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
            pivot_rotate = pivot.rotate(angle)
            pivot_move   = pivot_rotate - pivot

            # calculate the upper left origin of the rotated image
            origin = (int(screenResolution[0]//4-self.x-self.shakeX + pos[0] - originPos[0] + min_box[0] - pivot_move[0]), int(screenResolution[1]//4-self.y-self.shakeY + pos[1] - originPos[1] - max_box[1] + pivot_move[1]))
            # get a rotated image
            rotated_image = pygame.transform.rotate(image, angle+180)
            self.canvas.blit(rotated_image, origin)
        
        def drawBg(self):
            bgColor = [0,0,20]
            for i in range(3):
                if self.colorflash[i]>0:
                    bgColor[i]+=self.colorflash[i]*2
                    self.colorflash[i]-=2
            self.canvas.fill(bgColor)

            width = 18
            pygame.draw.rect(self.canvas, (20,100,20), (0,screenResolution[1]//2-width, screenResolution[0]//2*game.player.hp/100, width), 0)
            for pos in self.starPositions:
                paralax = pos[2]
                pos1 = (int(pos[0]-self.x*paralax-self.shakeX)%(screenResolution[0]//2), int(pos[1]-self.y*paralax-self.shakeY)%(screenResolution[1]//2))
                lightspeedEffect = pos[2]
                pygame.draw.line(self.canvas, (255,255,250), pos1, (pos1[0]+game.player.xv*lightspeedEffect, pos1[1]+game.player.yv*lightspeedEffect), 1)
            #self.canvas.blit(game.bgImage, (0,0))

        def display(self):
            screen = pygame.transform.scale(self.canvas, screenResolution)
            gameDisplay.blit(screen, (0,0))

    class Ship():

        hasTurret = True
        originPos = (32,32)
        bubbleImage = pygame.image.load(os.path.join(filepath, "ship", "bubble.png"))
        fireImages = []
        for i in [1,2,3]:
            img = pygame.image.load(os.path.join(filepath, "scout", f"fire{i}.png"))
            fireImages.append(img)
            fireImages.append(pygame.transform.flip(img,False,True))

        def __init__(self,x,y):
            self.hp = 100
            self.x = x
            self.y = y
            self.xv = 0
            self.yv = 0
            self.a = 0 #rotates clockwise because y is down :/
            self.shootAngle = 0
            self.shotCd = 0

            self.shield = 0
            self.drawFire = 0

        def update(self):
            if self.drawFire and random.random()<0.8:
                dustspd = 2
                dust = Dust(self.x-math.cos(self.a)*16,self.y-math.sin(self.a)*16,self.xv-math.cos(self.a)*dustspd,self.yv-math.sin(self.a)*dustspd, a=random.random()*math.tau, av=random.random()-0.5)
                game.particles.append(dust)

            self.x+=self.xv
            self.y+=self.yv
            self.xv*=0.99
            self.yv*=0.99

            if self.shotCd>0:
                self.shotCd-=1

            if self.shield:
                self.shield-=1

            if self.hp<=0:
                self.die()

        def draw(self):
            if self.drawFire:
                game.camera.blitRotate(random.choice(self.fireImages), (self.x,self.y), self.originPos, self.a)
            game.camera.blitRotate(self.image, (self.x,self.y), self.originPos, self.a)
            if self.hasTurret:
                game.camera.blitRotate(self.turretImage, (self.x,self.y), self.originPos, self.shootAngle)
            if self.shield and random.random()<self.shield/300+0.5:
                game.camera.blitRotate(self.bubbleImage, (self.x,self.y), (32,32), self.a)

    class Player(Ship):

        image = pygame.image.load(os.path.join(filepath, "scout", "normal1.png"))
        turretImage = pygame.image.load(os.path.join(filepath, "scout", "turret.png"))

        def update(self):
            if stickNum>0:
                dx = joysticks[0].get_axis(0)
                dy = joysticks[0].get_axis(1)
                rightDx = joysticks[0].get_axis(2)
                rightDy = joysticks[0].get_axis(3)
            else:
                pressed = pygame.key.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                dx = pressed[pygame.K_d] - pressed[pygame.K_a]
                dy = pressed[pygame.K_s] - pressed[pygame.K_w]
                rightDx = - screenResolution[0]//2 - self.x + game.camera.x + mouse_pos[0]
                rightDy = - screenResolution[1]//2 - self.y + game.camera.y + mouse_pos[1]
                #print(rightDx, rightDy)

            if -0.1<dx<0.1 and -0.1<dy<0.1:
                idle = True
            else:
                idle = False
            if -0.1<rightDx<0.1 and -0.1<rightDy<0.1:
                rightIdle = True
            else:
                rightIdle = False
            
            if not idle:
                angle = math.atan2(dy, dx)
                angleDiff = signedAngleDiff(self.a, angle)
                self.a+=angleDiff*0.05 #maybe should be linear?
                #self.shootAngle+=angleDiff*0.05 #it is attached physically #kinda annoying tho
                
                self.xv+=math.cos(self.a)*0.15
                self.yv+=math.sin(self.a)*0.15
                self.xv*=0.99
                self.yv*=0.99

                self.drawFire = 1
            else:
                self.drawFire = 0

            if not rightIdle:
                angle = math.atan2(rightDy, rightDx)
                angleDiff = signedAngleDiff(self.shootAngle, angle)
                self.shootAngle+=angleDiff*0.1

                if self.shotCd==0:
                    self.shotCd = 4
                    bulletSpd = 8
                    beam = Beam(self, self.xv+math.cos(self.shootAngle)*bulletSpd, self.yv+math.sin(self.shootAngle)*bulletSpd, self.shootAngle, (250,20,20))
                    game.bullets.append(beam)
                    self.xv+=math.cos(self.shootAngle)*-0.05
                    self.yv+=math.sin(self.shootAngle)*-0.05
                    game.camera.setShake(1)
                    Sound.laserSound.play()

            super().update()

        def hurt(self, bullet):
            if self.shield:
                factor = 0.2
            else:
                factor = 1
            self.hp-=bullet.damage*factor
            self.xv+=bullet.xv*0.1
            self.yv+=bullet.yv*0.1
            game.camera.setShake(16)
            game.camera.setColorflash((32,0,0))
            Sound.hitSound.play()
            game.camera.setShake(16)
            if stickNum:
                joysticks[0].rumble(0.5,0.5,100)

        def die(self):
            game.over += 1
            
    class Enemy(Ship):

        def __init__(self,x,y):
            super().__init__(x,y)
            if random.random()<0.1:
                self.shield = 300

        def targetAngleDiff(self):
            distanceFactor = (0.1*random.random()+0.2)*((game.player.x-self.x)**2 + (game.player.x-self.x)**2)**0.5
            targetPosX = game.player.x + (game.player.xv-self.xv)*distanceFactor
            targetPosY = game.player.y + (game.player.yv-self.yv)*distanceFactor
            angle = math.atan2(targetPosY - self.y, targetPosX - self.x)
            return signedAngleDiff(self.a, angle)

        def update(self):
            if not (self.x==game.player.x and self.y==game.player.y):
                
                angleDiff = self.targetAngleDiff()
                rotation = angleDiff*0.1 + (random.random()-0.5)*0.1
                self.a+=rotation
                self.shootAngle+=rotation #it is attached physically
                
                self.xv+=math.cos(self.a)*0.1
                self.yv+=math.sin(self.a)*0.1

                self.drawFire = 1
            else:
                self.drawFire = 0

            super().update()

        def hurt(self, bullet):
            if self.shield:
                factor = 0.4
            else:
                factor = 1
            self.hp-=bullet.damage*factor
            game.camera.setShake(2)
            if stickNum:
                joysticks[0].rumble(20,800,20)

        def die(self):
            game.totalKills+=1
            if stickNum:
                joysticks[0].rumble(0.2,8,100)
            game.camera.setShake(8)
            game.enemies.remove(self)
            game.particles.append(BigExplosion(self.x,self.y,self.xv,self.yv))
            Sound.blastSound.play()
            for i in range(random.randint(3,5)):
                a = random.random()*math.tau
                spd = 2
                game.bullets.append(Debris(self, self.xv+math.cos(a)*spd, self.yv+math.sin(a)*spd, random.random()*math.tau))
            if random.random()<0.2:
                game.items.append(random.choice([Heal,Shield])(self.x,self.y,self.xv,self.yv))
        """
        def draw(self):
            if self.x-game.player.x !=0 or self.y-game.player.y != 0:
                dx = (self.x-game.player.x)
                dy = (self.y-game.player.y)
                hyp = math.sqrt(dx**2 + dy**2)
                game.camera.drawLine((40,50,50),(game.player.x,game.player.y),(game.player.x+dx/hyp*100,game.player.y+dy/hyp*100),random.randint(1,2))
            super().draw()
        """

    class Scout(Enemy):
        
        image = pygame.image.load(os.path.join(filepath, "scout", "normal1.png"))
        turretImage = pygame.image.load(os.path.join(filepath, "scout", "turret.png"))

        def update(self):
            if not (self.x==game.player.x and self.y==game.player.y):
                angleDiff = self.targetAngleDiff()
                rotation = angleDiff*0.1 + (random.random()-0.5)*0.2
                self.shootAngle+=rotation

                if self.shotCd==0:
                    self.shotCd = 40
                    bulletSpd = 4
                    beam = Beam(self, self.xv+math.cos(self.shootAngle)*bulletSpd, self.yv+math.sin(self.shootAngle)*bulletSpd, self.shootAngle, (20,250,20))
                    self.xv+=math.cos(self.shootAngle)*-0.1
                    self.yv+=math.sin(self.shootAngle)*-0.1
                    game.bullets.append(beam)

            super().update()
    class Cruiser(Enemy):
        
        image = pygame.image.load(os.path.join(filepath, "cruiser", "normal1.png"))
        hasTurret = False
        originPos = (64,64)
        fireImages = [
        pygame.image.load(os.path.join(filepath, "cruiser", "fire1.png")),
        pygame.transform.flip(pygame.image.load(os.path.join(filepath, "cruiser", "fire1.png")),False,True)
        ]

        def __init__(self,x,y):
            super().__init__(x,y)
            self.hp = 300

        def update(self):
            if not (self.x==game.player.x and self.y==game.player.y):

                if self.shotCd==0:
                    self.shotCd = 20
                    bulletSpd = 4
                    offset = 20
                    beam = Beam(self, self.xv+math.cos(self.shootAngle)*bulletSpd, self.yv+math.sin(self.shootAngle)*bulletSpd, self.shootAngle, (20,250,20))
                    beam.x+=math.cos(self.a+math.pi/2)*offset
                    beam.y+=math.sin(self.a+math.pi/2)*offset
                    beam2 = Beam(self, self.xv+math.cos(self.shootAngle)*bulletSpd, self.yv+math.sin(self.shootAngle)*bulletSpd, self.shootAngle, (20,250,20))
                    beam2.x+=math.cos(self.a-math.pi/2)*offset
                    beam2.y+=math.sin(self.a-math.pi/2)*offset
                    self.xv+=math.cos(self.shootAngle)*-0.1
                    self.yv+=math.sin(self.shootAngle)*-0.1
                    game.bullets.append(beam)
                    game.bullets.append(beam2)

            super().update()


    class Projectile():

        def __init__(self, owner, xv, yv, a):
            self.owner = owner
            self.x = self.owner.x
            self.y = self.owner.y
            self.xv = xv
            self.yv = yv
            self.a = a #AESTHETIC
            self.damage = 10

        def update(self):
            self.x+=self.xv
            self.y+=self.yv
            k = 250
            if not (-2*k<self.x-game.camera.x<2*k and -k<self.y-game.camera.y<k):
                game.bullets.remove(self)
            else:
                for enemy in game.enemies+[game.player]:
                    if enemy == self.owner:
                        continue
                    if abs(self.x - enemy.x) + abs(self.y - enemy.y) < 20:
                        game.bullets.remove(self)
                        game.particles.append(Explosion(self.x,self.y,0,0))
                        enemy.hurt(self)
                        break

    class Beam(Projectile):

        def __init__(self, owner, xv, yv, a, color):
            super().__init__(owner, xv, yv, a)
            self.color = color

        def draw(self):
            game.camera.drawLine(self.color,(self.x,self.y),(self.x+math.cos(self.a)*8,self.y+math.sin(self.a)*8),random.randint(2,4))
    class Debris(Projectile):

        images = []

        for i in [1,2]:
            current = pygame.image.load(os.path.join(filepath, "cruiser", f"debris{i}.png"))
            images.append(current)
            images.append(pygame.transform.flip(current, False, True))

        def __init__(self, owner, xv, yv, a):
            super().__init__(owner, xv, yv, a)
            self.av = random.random()-random.random()
            self.image = random.choice(self.images)

        def update(self):
            self.a+=self.av
            super().update()

        def draw(self):
            game.camera.blitRotate(self.image, (self.x,self.y), (32,32), self.a)

    class Particle():

        def __init__(self, x, y, xv, yv, a=0, av=0):
            self.x = x
            self.y = y
            self.xv = xv
            self.yv = yv
            self.a = a #AESTHETIC
            self.av = av
            self.age = 0

        def update(self):
            self.x+=self.xv
            self.y+=self.yv
            self.xv*=0.99
            self.yv*=0.99
            self.a+=self.av
            self.age+=1

        def draw(self):
            game.camera.blitRotate(self.image, (self.x,self.y), (32,32), self.a)
    class Dust(Particle):

        image = pygame.image.load(os.path.join(filepath, "ship", "dust1.png")).convert_alpha()
        image1 = pygame.image.load(os.path.join(filepath, "ship", "dust1.png")).convert_alpha()
        image2 = pygame.image.load(os.path.join(filepath, "ship", "dust2.png")).convert_alpha()
        
        def update(self):
            if random.random()<0.1:
                if self.age<4:
                    self.image = self.image1
                else:
                    self.image = self.image2

            super().update()
            if self.age>4+random.random()*60: #
                game.particles.remove(self)
    class BigExplosion(Particle):

        image = pygame.image.load(os.path.join(filepath, "ship", "bigexplosion1.png")).convert_alpha()
        image1 = pygame.image.load(os.path.join(filepath, "ship", "bigexplosion1.png")).convert_alpha()
        image2 = pygame.image.load(os.path.join(filepath, "ship", "bigexplosion2.png")).convert_alpha()
        image3 = pygame.image.load(os.path.join(filepath, "ship", "explosion2.png")).convert_alpha()
        
        def update(self):
            if self.age<4:
                self.image = self.image1
            elif self.age<12:
                self.image = self.image2
            else:
                self.image = self.image2

            super().update()
            if self.age>8+random.random()*60: #
                game.particles.remove(self)
    class Explosion(Particle):

        image = pygame.image.load(os.path.join(filepath, "ship", "explosion1.png")).convert_alpha()
        image1 = pygame.image.load(os.path.join(filepath, "ship", "explosion1.png")).convert_alpha()
        image2 = pygame.image.load(os.path.join(filepath, "ship", "explosion2.png")).convert_alpha()
        
        def update(self):
            if self.age<4:
                self.image = self.image1
            else:
                self.image = self.image2

            super().update()
            if self.age>8+random.random()*30: #
                game.particles.remove(self)

    class Item():

        def __init__(self, x, y, xv, yv):
            self.x = x
            self.y = y
            self.xv = xv
            self.yv = yv

        def update(self):
            if 1:
                angle = math.atan2(game.player.y - self.y, game.player.x - self.x)
                self.xv+=math.cos(angle)*0.5 +random.randint(-1,1)*0.2
                self.yv+=math.sin(angle)*0.5 +random.randint(-1,1)*0.2

                self.x+=self.xv
                self.y+=self.yv
                self.xv*=0.95
                self.yv*=0.95

            if abs(self.x - game.player.x) + abs(self.y - game.player.y) < 40:
                game.items.remove(self)
                self.pickup()

        def draw(self):
            game.camera.blitImage(self.image, (self.x,self.y), (32,32))

    class Heal(Item):

        image = pygame.image.load(os.path.join(filepath, "items", "heal.png"))

        def pickup(self):
            game.player.hp = min(100, game.player.hp+50)
            game.camera.setColorflash((0,32,0))
    class Shield(Item):

        image = pygame.image.load(os.path.join(filepath, "items", "shield.png"))

        def pickup(self):
            game.player.shield = min(600, game.player.shield+300)
            game.camera.setColorflash((0,0,32))

    pygame.joystick.init()
    stickNum = pygame.joystick.get_count()
    joysticks=[]
    for i in range(stickNum):
        joysticks.append(pygame.joystick.Joystick(i))
        joysticks[-1].init()
        print("joystick nummer ",i)

    game = Game()


    jump_out = False
    while jump_out == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                jump_out = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    jump_out = True

        if game.over == False:
            game.update()
        else:
            game.over += 1
            if game.over == 500:
                jump_out = True
        game.draw()

        pygame.display.flip()

        clock.tick(60)

    print(f"[Finished with {game.totalKills} kills]")


if __name__=="__main__":
    filepath=os.path.join("blastGameFiles")
    blastGameMain()
else:
    filepath=os.path.join("launcherFiles","blastGameFiles")
    import sys
    if hasattr(sys, '_MEIPASS'):
        filepath = os.path.join(sys._MEIPASS, filepath)


"""
b
[Finished with 178 kills]
[Finished in 304.0s]
"""