from re import X
from tkinter import E
import pyxel
from random import * 
from enum import Enum

# frame_count % x zeit
# pyxel edit Spiel.pyxres
# git pull
class LiveState(Enum):
    ALIVE = 0
    DYING = 1
    DEAD  = 2

class Live:
    def __init__(self) -> None:
        pass

    def update(self):
        pass
    def draw(self):
        pyxel.blt(20, 110, 1, 0, 32, 16, 16, 2)

class Enemy:
    def __init__(self, img):
        self.x = randint(100,150)
        self.y = randint(0,110)
        self.img = img
        self.direction = True
        self.speedx = 0.5
        self.speedy = 0.5
        self.anim = 0
        self.state = LiveState.ALIVE
        self.deadtime = 0
    
    # Hitbox
    def hitbox(self):
        return [self.x, self.y, 16, 16]

    def handle_death(self):
        if self.state == LiveState.DEAD:
            return True
        elif self.state == LiveState.DYING:
            if self.deadtime == 0:
                self.deadtime = pyxel.frame_count
                self.img += 16 
            if pyxel.frame_count > self.deadtime + 10:
                self.state = LiveState.DEAD
            return True
        return False

    def update(self, playerx, playery):
        if self.handle_death():
            return
        
        if self.y - playery > 0:
            self.y = self.y - self.speedy
        if playery - self.y > 0:
            self.y = self.y + self.speedy

        if abs(self.y - playery) <= self.speedy:
            if self.x - playerx > 0:
                self.x = self.x - self.speedx
            if playerx - self.x > 0:
                self.x = self.x + self.speedx
        
        self.face_player(playerx)

    def face_player(self, playerx):
        # Face player
        if self.x < playerx:
            self.direction = True
        else:
            self.direction = False

    def draw(self):

        if self.state == LiveState.DEAD:
            return

        # Hitbox
        #x, y, h, w = self.hitbox()
        #pyxel.rectb(x, y, h, w, 8)

        enemy_frames = [0,16,32,48,64,80,96,112,128,144,160,176,192,208,224,240]

        if  pyxel.frame_count % 2 == 0:
            self.anim = self.anim + 1
        if self.anim == 16:
            self.anim = 0

        if self.direction:
            pyxel.blt(self.x, self.y, 2, enemy_frames[self.anim] , self.img, 16, 16, 2) 
        else:
            pyxel.blt(self.x, self.y, 2, enemy_frames[self.anim], self.img,-16, 16, 2)
    
class Slime(Enemy):

    def __init__(self):
        super().__init__(32)
        self.img = 0
        self.speedx = 1
        self.speedy = 1

    def hitbox(self):
        return [self.x + 2, self.y + 6, 11, 8]

class Fireslime(Enemy):
    def __init__(self, add_shot):
        super().__init__(16)
        self.img = 96
        self.speedx = 0.5
        self.speedy = 0.5
        self.add_shot = add_shot
        self.last_shot = 0

    def hitbox(self):
        return [self.x + 3, self.y + 1, 10, 12]
    
    def update(self, playerx, playery):
        if self.handle_death():
            return

        if self.y - playery > 0:
            self.y = self.y - self.speedy
        if playery - self.y > 0:
            self.y = self.y + self.speedy

        if self.y == playery:
            distance = self.x - playerx
            
            if self.last_shot + 50< pyxel.frame_count:
                shot = Fireball()
                shot.shoot(self.x, self.y, self.direction)
                self.add_shot(shot)
                self.last_shot = pyxel.frame_count


            if abs(distance) < 50:
                if distance > 0:
                    self.x = self.x + self.speedx
                else:
                    self.x = self.x - self.speedx
            elif abs(distance) > 55:
                if distance > 0:
                    self.x = self.x - self.speedx
                else:
                    self.x = self.x + self.speedx

        self.face_player(playerx)


        if self.x < 0:
            self.x = 0
        if self.x > 145:
            self.x = 145

class Waterslime(Enemy):
    def __init__(self):
        super().__init__(32)
        self.img = 32
        self.speedy = 0.25
        self.speedx = 1.5

    # Hitbox
    def hitbox(self):
        return [self.x, self.y + 7, 16, 7]

class Bomber(Enemy):
    def __init__(self):
        super().__init__(48)
        self.img = 64
        self.speedx = 1
        self.speedy =1
        self.anim = 0

    def update(self, playerx, playery):
        if self.handle_death():
            return
        
        if self.y - playery > 0:
            self.y = self.y - self.speedy
        elif self.y - playery < 0:
            self.y = self.y + self.speedy
        if playerx - self.x > 0:
            self.x = self.x + self.speedx
        elif playerx - self.x < 0:
            self.x = self.x - self.speedx
        
        self.face_player(playerx)
    # Hitbox
    def hitbox(self):
        return [self.x + 3, self.y + 4, 10, 8]
    

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



class Arrow:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.shotmove = False
        self.image = 80
        self.state = LiveState.ALIVE
    
    def shoot(self, x, y, direction):
        self.shotmove = True
        self.x = x
        self.y = y
        self.direction = direction

    def update(self):
        # Shot position
        if self.shotmove == True:
            if self.direction:
                self.x = self.x + 4
            else:
                self.x = self.x - 4
        if self.x > 160:
            self.shotmove = False
  
    def draw(self):
        if self.shotmove == True:
            if self.direction:
                pyxel.blt(self.x, self.y, 0, 0, self.image, 16, 16, 2)
            else:
                pyxel.blt(self.x, self.y, 0, 0, self.image, -16, 16, 2)


class Fireball(Arrow):
    def __init__(self):
        super().__init__()
        self.image = 96

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Hello Pyxel")
        pyxel.load('Spiel.pyxres')
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.posx = 10
        self.posy = 20
        self.posS = []
        self.direction = True
        self.anim = 0
        self.state = LiveState.ALIVE
        self.img = 0
        self.score = 0
        self.deadtime = 0

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
        self.enemies = [Slime(), Fireslime(self.add_shot), Waterslime(), Bomber()]
        
        
    # Shot
    def add_shot(self, shot):
        self.shots.append(shot)

    # Hitbox
    def hitbox(self):
        return [self.posx + 5, self.posy + 4, 7, 10]

    def update(self):
        if self.state == LiveState.DEAD:
            self.img = 16
            if not self.deadtime:
                self.deadtime = pyxel.frame_count 
            if pyxel.btn(pyxel.KEY_SPACE) and pyxel.frame_count > self.deadtime + 60:
                self.reset()
            return    

        # Key handling
        if pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
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

            # Hitbox 
            if enemy.state != LiveState.ALIVE:
                continue
            x, y, w, h = enemy.hitbox()
            px, py, pw, ph = self.hitbox()
            if (px < x < px + pw or px < x + w < px + pw) and \
                (py < y < py + ph or py < y + h < py + ph):
                self.state = LiveState.DEAD


        # Pet
        self.pet.update(self.posx, self.posy)

        # Shot
        if pyxel.btnp(pyxel.KEY_SPACE):
            shot = Arrow()
            shot.shoot(self.posx, self.posy, self.direction)
            self.add_shot(shot)
        
        for shot in self.shots:
            shot.update()

            if type(shot) == Arrow:
                for enemy in self.enemies:
                    if enemy.state == LiveState.DEAD:
                        continue
                    x, y, w, h = enemy.hitbox()
                    if x < shot.x + 11 < x + w and y < shot.y + 7 < y + h:
                        enemy.state = LiveState.DYING
                        shot.state = LiveState.DEAD
                        self.score += 1
            else:
                x, y, w, h = self.hitbox()
                if x < shot.x + 11 < x + w and y < shot.y + 7 < y + h:
                    self.state = LiveState.DEAD         

        # Enemy list
        self.enemies = [e for e in self.enemies if e.state != LiveState.DEAD]
        if len(self.enemies) < 4 + self.score // 15:
            newenemy = choice([Slime(), Fireslime(self.add_shot), Waterslime(), Bomber()])
            
            if pyxel.frame_count % 4 == 0:
                newx = 0
                newy = randint(0, 150)
            if pyxel.frame_count % 4 == 1:
                newx = 160
                newy = randint(0, 150)
            if pyxel.frame_count % 4 == 2:
                newx = randint(0, 160)
                newy = 0
            if pyxel.frame_count % 4 == 3:
                newx = randint(0,160)
                newy = 150
            newenemy.x = newx
            newenemy.y = newy
            if random() < 0.2:
                newenemy.speedx *= 1.4
                newenemy.speedy *= 1.4
            elif random() < 0.2:
                newenemy.speedy /= 2
                newenemy.speedy /= 2

            self.enemies.append(newenemy)

        self.shots = [e for e in self.shots if e.state != LiveState.DEAD]

    def draw(self):
        pyxel.cls(11)
        
        for pos in self.posS:
            pyxel.pset(pos[0], pos[1], 13)

        self.pet.draw()
        for enemy in self.enemies:
            enemy.draw()

        for i in self.shots:
            i.draw()
        
        # Hitbox
        #x, y, h, w = self.hitbox()
        #pyxel.rectb(x, y, h, w, 8)

        #if -8 < self.posx - self.enemies.x < 8 and -8 < self.posy - self.enemies.y < 8:
        #    costume = 16

        player_frames = [0,16,32,48,64,80]

        if  pyxel.frame_count % 2 == 0:
            self.anim = self.anim + 1
        if self.anim == 6:
            self.anim = 0
        
        if self.direction:
            pyxel.blt(self.posx, self.posy, 1, player_frames[self.anim], self.img, 16, 16,2)
        else:
            pyxel.blt(self.posx, self.posy, 1, player_frames[self.anim], self.img, -16, 16,2)
 
        if self.state == LiveState.DEAD:
            pyxel.text(55, 55, "Game Over", 1)
            pyxel.text(55, 63, "Score: " + str(self.score), 0)
        else:
            pyxel.text(5, 5, "Score: " + str(self.score), 0)
App()


