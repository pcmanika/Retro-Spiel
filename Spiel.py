import pyxel
from random import * 

# frame_count % x zeit
# pyxel edit Spiel.pyxres
# self!!!!!!
# git pull

class Live:
    def __init__(self) -> None:
        pass

    def update(self):
        pass
    def draw(self):
        pyxel.blt(20, 110, 1, 0, 32, 16, 16, 2)

class Enemy:
    def __init__(self, img):
        self.x = randint(0,150)
        self.y = randint(0,110)
        self.img = img
        self.direction = True
        self.speed = 0.5
        self.anim = 0

    def update(self, playerx, playery):

        if self.y - playery > 0:
            self.y = self.y - self.speed
        if playery - self.y > 0:
            self.y = self.y + self.speed

        if abs(self.y - playery) <= self.speed:
            if self.x - playerx > 10:
                self.x = self.x - self.speed
            if playerx - self.x > 10:
                self.x = self.x + self.speed
        
        self.face_player(playerx)

    def face_player(self, playerx):
        # Face player
        if self.x < playerx:
            self.direction = True
        else:
            self.direction = False

    def draw(self):

        enemy_frames = [0,16,32,48,64,80,96,112,128,144,160,176,192,208,224,240]

        if  pyxel.frame_count % 2 == 0:
            self.anim = self.anim + 1
        if self.anim == 16:
            self.anim = 0

        if self.direction:
            pyxel.blt(self.x, self.y, 2, enemy_frames[self.anim] , self.img, 16, 16, 2) 
        else:
            pyxel.blt(self.x, self.y, 2, enemy_frames[self.anim], self.img,-16, 16, 2)
    
class Fireslime(Enemy):
    def __init__(self, add_shot):
        super().__init__(16)
        self.img = 16
        self.speed = 0.5
        self.add_shot = add_shot
        self.last_shot = 0
    
    def update(self, playerx, playery):

        if self.y - playery > 0:
            self.y = self.y - self.speed
        if playery - self.y > 0:
            self.y = self.y + self.speed

        if self.y == playery:
            distance = self.x - playerx
            
            if self.last_shot + 50< pyxel.frame_count:
                shot = Fireball()
                shot.shoot(self.x, self.y, self.direction)
                self.add_shot(shot)
                self.last_shot = pyxel.frame_count


            if abs(distance) < 50:
                if distance > 0:
                    self.x = self.x + self.speed
                else:
                    self.x = self.x - self.speed
            elif abs(distance) > 55:
                if distance > 0:
                    self.x = self.x - self.speed
                else:
                    self.x = self.x + self.speed

        self.face_player(playerx)


        if self.x < 0:
            self.x = 0
        if self.x > 145:
            self.x = 145

class Waterslime(Enemy):
    def __init__(self):
        super().__init__(32)
        self.img = 32
        self.speed = 0.25

class Bomber(Enemy):
    def __init__(self):
        super().__init__(48)
        self.img = 48
        self.speed = 1.5
        self.anim = 0
    

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
        self.image = 80
    
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
                pyxel.blt(self.shotx, self.shoty, 0, 0, self.image, 16, 16, 2)
            else:
                pyxel.blt(self.shotx, self.shoty, 0, 0, self.image, -16, 16, 2)


class Fireball(Shot):
    def __init__(self):
        super().__init__()
        self.image = 96

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Hello Pyxel")
        pyxel.load('Spiel.pyxres')
        self.posx = 0
        self.posy = 0
        self.posS = []
        self.direction = True
        self.anim = 0

        # Live
        self.live = Live

        # Stones
        for i in range(0, 25):
            self.posS.append([randrange(0,160),randrange(0,120)])
        
        # Shot
        self.shots = []

        # Pet
        self.pet = Pet()

        # Enemy
        self.enemies = [Enemy(0), Fireslime(self.add_shot), Waterslime(), Bomber()]
        
        pyxel.run(self.update, self.draw)
        
    # Shot
    def add_shot(self, shot):
        self.shots.append(shot)



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
        for enemy in self.enemies:
            enemy.update(self.posx, self.posy)

        # Pet
        self.pet.update(self.posx, self.posy)

        # Shot
        if pyxel.btnp(pyxel.KEY_SPACE):
            shot = Shot()
            shot.shoot(self.posx, self.posy, self.direction)
            self.add_shot(shot)
        
        for i in self.shots:
           i.update()
                
    # Shot     
    def draw(self):
        pyxel.cls(11)
        
        for pos in self.posS:
            pyxel.pset(pos[0], pos[1], 13)

        self.pet.draw()
        for enemy in self.enemies:
            enemy.draw()

        for i in self.shots:
            i.draw()
        

        costume = 0
        #if -8 < self.posx - self.enemies.x < 8 and -8 < self.posy - self.enemies.y < 8:
        #    costume = 16

        player_frames = [0,16,32,48,64,80]

        if  pyxel.frame_count % 2 == 0:
            self.anim = self.anim + 1
        if self.anim == 6:
            self.anim = 0
        
        if self.direction:
            pyxel.blt(self.posx, self.posy, 1, player_frames[self.anim], costume, 16, 16,2)
        else:
            pyxel.blt(self.posx, self.posy, 1, player_frames[self.anim], costume, -16, 16,2)
 
App()


