import pyxel
import math


class Game():

    def __init__(self):

        pyxel.init(128,128,"NDC 2023",60)

        self.posx,self.posy = 64,64
        self.velx,self.vely = 0,0
        self.hp_max = 100
        self.hp = self.hp_max
        self.hp_percent = 1

        self.shoot_cd = 0
        self.shoot_rate = 2
        self.spread = 30
        self.amount_bullet = 4

        self.list_bullet = []
        self.boss = Boss(16,64,1)
        self.scene = 1

        pyxel.run(self.update,self.draw)

    def update(self):
        
        if self.scene == 1:
            self.player()
            self.boss_shoot()
            self.boss.update()
            for bullet in self.list_bullet:
                bullet.update()
                if bullet.posx > self.boss.cordX and bullet.posx < self.boss.cordX + self.boss.largeur and bullet.posy > self.boss.cordY and bullet.posy < self.boss.cordY + self.boss.hauteur and bullet.type == 0:
                    self.boss.hp += -1
                    bullet.alive = False
                if bullet.posx > self.posx and bullet.posx < self.posx + 6 and bullet.posy > self.posy and bullet.posy < self.posy + 6 and bullet.type == 1:
                    self.hp += -1
                    bullet.alive = False
                if not bullet.alive:
                    self.list_bullet.remove(bullet)

    def draw(self):

        pyxel.cls(0)

        if self.scene == 0:
            pass

        if self.scene == 1:
            for bullet in self.list_bullet:
                bullet.draw()
            pyxel.rect(self.posx,self.posy,6,6,1)
            self.boss.draw()
            pyxel.rect(120,2,6,124,13)
            pyxel.rect(120,2+124*(1-self.boss.hp_percent),6,124*self.boss.hp_percent,8)
            pyxel.rect(2,66,6,60,13)
            pyxel.rect(2,66+60*(1-self.hp_percent),6,60*self.hp_percent,11)

    
    def player(self):

        self.velx,self.vely = (pyxel.btn(pyxel.KEY_RIGHT) - pyxel.btn(pyxel.KEY_LEFT)),(pyxel.btn(pyxel.KEY_DOWN) - pyxel.btn(pyxel.KEY_UP))
        
        if pyxel.btn(pyxel.KEY_SPACE):
            if self.shoot_cd == 0:
                if self.amount_bullet == 1:
                    self.list_bullet += [Bullet(self.posx+3,self.posy+3,-90,1,0,0,0)]
                else:
                    for x in range(int(-self.spread/2),int(self.spread/2)+1,int(self.spread/(self.amount_bullet-1))):
                        self.list_bullet += [Bullet(self.posx+3,self.posy+3,x-90,1,0,0,0)]
                self.shoot_cd = 10/self.shoot_rate
            
        
        self.posx,self.posy = self.posx + self.velx, self.posy + self.vely
        self.shoot_cd = max(0,self.shoot_cd - 1)
        self.hp_percent = self.hp/self.hp_max

    def boss_shoot(self):
        if self.boss.shoot_cd == 0:
            if self.boss.hp_percent > 0.75:
                self.boss.phase = 0
                for x in range(45,135,int(90/10)):
                    self.list_bullet += [Bullet(self.boss.cordX+self.boss.largeur/2,self.boss.cordY+self.boss.hauteur/2,x,1,0,0,1)]
                self.boss.shoot_cd = 20
            if self.boss.hp_percent < 0.75 and self.boss.hp_percent > 0.5:
                self.boss.phase = 1
                self.boss.cordX,self.boss.cordY = 120,16
                for x in range(0,360,int(360/20)):
                    self.list_bullet += [Bullet(self.boss.cordX+self.boss.largeur/2,self.boss.cordY+self.boss.hauteur/2,x+self.boss.shoot_spin,0.2,15,0,1)]
                self.boss.shoot_cd = 60
            if self.boss.hp_percent < 0.5:
                self.boss.phase = 2
                self.boss.cordX,self.boss.cordY = 120,16
                for x in range(0,360,int(360/20)):
                    self.list_bullet += [Bullet(self.boss.cordX+self.boss.largeur/2,self.boss.cordY+self.boss.hauteur/2,x,1,0,0,1)]
                    self.list_bullet += [Bullet(self.boss.cordX+self.boss.largeur/2,self.boss.cordY+self.boss.hauteur/2,x+self.boss.shoot_spin,0.2,15,0,1)]
                self.boss.shoot_cd = 60
        self.boss.shoot_cd = max(0,self.boss.shoot_cd - 1)
        self.boss.shoot_spin += 3

class Bullet:

    def __init__(self,x,y,angle,vel,rot_speed,spin_speed,type) -> None:
        
        self.posx,self.posy = x,y
        self.angle = angle
        self.vel = vel
        self.rot_speed = rot_speed
        self.spin_speed = spin_speed
        self.type = type
        self.alive = True

    def update(self):

        self.posx,self.posy = self.posx + math.cos(math.radians(self.angle))*self.vel,self.posy + math.sin(math.radians(self.angle))*self.vel
        self.angle += self.rot_speed
        self.rot_speed = self.rot_speed*0.98
        if self.posx > 192 or self.posx < -64 or self.posy > 192 or self.posy < -64:
            self.alive = False

    def draw(self):

        if self.type == 0:
            pyxel.circ(self.posx,self.posy,1,10)
        if self.type == 1:
            pyxel.circ(self.posx,self.posy,1,3)
        
class Boss:

    def __init__(self,x,y,hp_percent) -> None:

        self.max_hp = 1000
        self.hp = self.max_hp*hp_percent
        self.hp_percent = hp_percent
        self.shoot_cd = 0
        self.shoot_spin = 1

        self.hauteur = 0
        self.largeur = 0
        self.cordY = y
        self.cordX = x
        self.anim = False
        self.anim_boss= False
        self.amplitude = 15
        self.amplitude_var = 15
        self.phase = 0
        self.patern = [[(110, 50), (10, 50)], [(10, 10), (110, 10), (110, 30), (10, 30)], [(10, 10), (110, 30), (40, 60), (90, 60), (300, 200), (100, 100)]]
        self.baseX = 64
        self.baseY = 64
        self.point = 0
        self.arrive = 30
        self.compteur = 0

        #1er triangle
        self.trig_angle_x_1 = 5*math.pi/6
        self.trig_angle_y_1 = 5*math.pi/6
        self.trig_angle_x_2 = math.pi/6
        self.trig_angle_y_2 = math.pi/6
        self.trig_angle_x_3 = 3*math.pi/2
        self.trig_angle_y_3 = 3*math.pi/2
        self.trig1 = [self.trig_angle_x_1,
        self.trig_angle_y_1,
        self.trig_angle_x_2,
        self.trig_angle_y_2,
        self.trig_angle_x_3,
        self.trig_angle_y_3]

        #2eme triangle
        self.trig2_angle_x_1 = 5*math.pi/6
        self.trig2_angle_y_1 = 5*math.pi/6
        self.trig2_angle_x_2 = math.pi/6
        self.trig2_angle_y_2 = math.pi/6
        self.trig2_angle_x_3 = 3*math.pi/2
        self.trig2_angle_y_3 = 3*math.pi/2
        self.trig2 = [self.trig2_angle_x_1,
        self.trig2_angle_y_1,
        self.trig2_angle_x_2,
        self.trig2_angle_y_2,
        self.trig2_angle_x_3,
        self.trig2_angle_y_3]

        #3eme triangle
        self.trig3_angle_x_1 = 5*math.pi/6
        self.trig3_angle_y_1 = 5*math.pi/6
        self.trig3_angle_x_2 = math.pi/6
        self.trig3_angle_y_2 = math.pi/6
        self.trig3_angle_x_3 = 3*math.pi/2
        self.trig3_angle_y_3 = 3*math.pi/2
        self.trig3 = [self.trig3_angle_x_1,
        self.trig3_angle_y_1,
        self.trig3_angle_x_2,
        self.trig3_angle_y_2,
        self.trig3_angle_x_3,
        self.trig3_angle_y_3]




        

    def update(self):

        self.hp_percent = self.hp/self.max_hp
        if self.hauteur >= 15 and self.largeur >= 15:
            self.anim = True
        elif self.hauteur <= 5 and self.largeur <= 5:
            self.anim = False

        if self.anim == False:
            self.hauteur += 0.5
            self.largeur += 0.5
            self.cordY -= 0.25 
            self.cordX -= 0.25
            self.amplitude_var -= 0.25
        elif self.anim == True:
            self.hauteur -= 0.5
            self.largeur -= 0.5
            self.cordY += 0.25
            self.cordX += 0.25
            self.amplitude_var += 0.25

        

        for i in range(len(self.trig1)):
            self.trig1[i] += math.pi/24
        
        for i in range(len(self.trig2)):
            self.trig2[i] += math.pi/48

        for i in range(len(self.trig3)):
            self.trig3[i] += math.pi/12

        if self.phase == 0:
            self.cordY = 10
            if self.cordX > 110:
                self.anim_boss = True
            elif self.cordX < 10:
                self.anim_boss = False

            if self.anim_boss == False:
                self.cordX += 1
            elif self.anim_boss == True:
                self.cordX -= 1
        else:

            if self.phase == 2:
                self.arrive = 3
            elif self.phase == 1:
                self.arrive = 20
            self.vectX = (self.patern[self.phase][self.point][0] - self.baseX)/self.arrive
        
            self.vectY = (self.patern[self.phase][self.point][1] - self.baseY)/self.arrive

            
            
            if self.compteur < self.arrive:
                self.cordX += self.vectX
                self.cordY += self.vectY
                self.compteur += 1
            else:
                self.compteur = 0
                self.baseX = self.patern[self.phase][self.point][0]
                self.baseY = self.patern[self.phase][self.point][1]
                if self.point == len(self.patern[self.phase])-1:
                    self.point = 0
                else:
                    self.point += 1
                
                




    def draw(self):
        pyxel.rect(self.cordX,self.cordY,self.largeur,self.hauteur,1)
        
        pyxel.trib(self.cordX + self.largeur/2 + math.cos(self.trig1[0])*self.amplitude, self.cordY + self.hauteur/2 + math.sin(self.trig1[1])*self.amplitude, self.cordX+ self.largeur/2 + math.cos(self.trig1[2])*self.amplitude, self.cordY + self.hauteur/2 + math.sin(self.trig1[3])*self.amplitude, self.cordX + self.largeur/2 + math.cos(self.trig1[4]) * self.amplitude, self.cordY + self.hauteur/2 +  math.sin(self.trig1[5]) *self.amplitude, 2)
        pyxel.trib(self.cordX + self.largeur/2 + math.cos(self.trig2[0])*self.amplitude, self.cordY + self.hauteur/2 + math.sin(self.trig2[1])*self.amplitude, self.cordX+ self.largeur/2 + math.cos(self.trig2[2])*self.amplitude, self.cordY + self.hauteur/2 + math.sin(self.trig2[3])*self.amplitude, self.cordX + self.largeur/2 + math.cos(self.trig2[4]) * self.amplitude, self.cordY + self.hauteur/2 +  math.sin(self.trig2[5]) *self.amplitude, 2)
        pyxel.trib(self.cordX + self.largeur/2 + math.cos(self.trig3[0])*self.amplitude, self.cordY + self.hauteur/2 + math.sin(self.trig3[1])*self.amplitude, self.cordX+ self.largeur/2 + math.cos(self.trig3[2])*self.amplitude, self.cordY + self.hauteur/2 + math.sin(self.trig3[3])*self.amplitude, self.cordX + self.largeur/2 + math.cos(self.trig3[4]) * self.amplitude, self.cordY + self.hauteur/2 +  math.sin(self.trig3[5]) *self.amplitude, 2)

Game()