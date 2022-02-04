import pyxel
from random import * 

# frame_count % x zeit
# pyxel edit Spiel.pyxres
# Img seite
# self!!!!!!
class live:
    def __init__(self) -> None:
        pass

    def update(self):
        pass
    def draw(self):
        pyxel.blt(20, 110, 1, 0, 32, 16, 16, 2)

class Enemy:
    def __init__(self, img):
        self.x = 50
        self.y = 50
        self.img = img
        self.direction = True

    def update(self, playerx, playery):

        if self.y - playery > 0:
            self.y = self.y - 0.5
        if playery - self.y > 0:
            self.y = self.y + 0.5

        if self.y == playery:
            if self.x - playerx > 10:
                self.x = self.x - 0.5
                self.direction = False
            if playerx - self.x > 10:
                self.x = self.x + 0.5
                self.direction = True


    def draw(self):
        if self.direction:
            pyxel.blt(self.x, self.y, 0, self.img, 32, 16, 16, 2) 
        else:
            pyxel.blt(self.x, self.y, 0, self.img, 32, -16, 16, 2)

class Pet:
    def __init__(self):
        self.x = 10
        self.y = 10
        self.direction = True

    def update(self, playerx, playery):
        if self.x - playerx > 10:
            self.x = self.x - 1
            self.direction = False
        if playerx - self.x > 10:
            self.x = self.x + 1
            self.direction = True

        if self.y - playery > 13:
            self.y = self.y - 1
        if playery - self.y > 13:
            self.y = self.y + 1   
        
    
    def draw(self):
        if self.direction:
            pyxel.blt(self.x, self.y, 0, 0, 16, 16, 16,2)
        else:
            pyxel.blt(self.x, self.y, 0, 0, 16, -16, 16,2)



class Shot:
    def __init__(self):
        self.shotx = 0
        self.shoty = 0
        self.shotmove = False
    
    def shoot(self, x, y, direction):
        self.shotmove = True
        self.shotx = x
        self.shoty = y
        self.direction = direction

    def update(self):
        # Shot position
        if self.shotmove == True:
            if self.direction:
                self.shotx = self.shotx + 4
            else:
                self.shotx = self.shotx - 4
        if self.shotx > 160:
            self.shotmove = False
  
    def draw(self):
        if self.shotmove == True:
            if self.direction:
                pyxel.blt(self.shotx, self.shoty, 0, 16, 48, 16, 16, 2)
            else:
                pyxel.blt(self.shotx, self.shoty, 0, 16, 48, -16, 16, 2)



class App:
    def __init__(self):
        pyxel.init(160, 120, title="Hello Pyxel")
        pyxel.load('Spiel.pyxres')
        self.posx = 0
        self.posy = 0
        self.posS = []
        self.direction = True
        #self.time_offset = pyxel.rndi(0,10)

        for i in range(0, 25):
            self.posS.append([randrange(0,160),randrange(0,120)])
        
        self.shots = []
        self.pet = Pet()
        self.enemy = Enemy(48)
        
        pyxel.run(self.update, self.draw)


    def update(self):

        # Key handling
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btn(pyxel.KEY_A):
            self.posx = self.posx - 2
            self.direction = False
        if pyxel.btn(pyxel.KEY_D):
            self.posx = self.posx + 2
            self.direction = True
        if pyxel.btn(pyxel.KEY_W):
            self.posy = self.posy - 2
        if pyxel.btn(pyxel.KEY_S):
            self.posy = self.posy + 2     

        # Player position
        if self.posx <= -2:
            self.posx = -2
        if self.posx >= 147:
            self.posx = 147
        if self.posy >= 104:
            self.posy = 104
        if self.posy <= -2:
            self.posy = -2

        # Enemy
        self.enemy.update(self.posx, self.posy)

        # Pet
        self.pet.update(self.posx, self.posy)

        # Shot
        if pyxel.btnp(pyxel.KEY_SPACE):
            shot = Shot()
            shot.shoot(self.posx, self.posy, self.direction)
            self.shots.append(shot)
        
        for i in self.shots:
           i.update()
                
            
    def draw(self):
        pyxel.cls(11)
        
        for pos in self.posS:
            pyxel.pset(pos[0], pos[1], 13)

        self.pet.draw()
        self.enemy.draw()

        for i in self.shots:
            i.draw()
        

        #pyxel.text(self.posx, self.posy, 'Pixel', 8)
        costume = 0
        if -8 < self.posx - self.enemy.x < 8 and -8 < self.posy - self.enemy.y < 8:
            costume = 16
        if self.direction:
            pyxel.blt(self.posx, self.posy, 1, 0, costume, 16, 16,2)
        else:
            pyxel.blt(self.posx, self.posy, 1, 0, costume, -16, 16,2)
        #for animation in (0,16,32,48):
        #    pyxel.blt(self.posx, self.posy, 1, 0 + animation, costume, -16, 16,2)
        #    self.time_offset = pyxel.rndi(0,10)
App()

