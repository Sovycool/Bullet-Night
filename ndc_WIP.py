import pyxel
import math
import random


class Game():

    def __init__(self):

        pyxel.init(128,128,"NDC 2023",60)
        pyxel.mouse(True)

        self.posx,self.posy = 64,64
        self.velx,self.vely = 0,0
        self.hp_max = 100
        self.hp = self.hp_max
        self.hp_percent = 1

        self.shoot_cd = 0
        self.shoot_rate = 2
        self.spread = 30
        self.amount_bullet = 3

        self.list_bullet = []
        self.boss = Boss(64,16,1,2,3)
        self.scene = 1

        self.triangle = Triangle(5,6)

        pyxel.run(self.update,self.draw)

    def update(self):
        
        if self.scene == 1:
            self.player()
            self.boss.update()
            for bullet in self.list_bullet:
                bullet.update()
                if bullet.posx > self.boss.posx - 12 and bullet.posx < self.boss.posx + 12 and bullet.posy > self.boss.posy - 12 and bullet.posy < self.boss.posy + 12 and bullet.type == 0:
                    self.boss.hp += -1
                    bullet.alive = False
                if bullet.posx > self.posx - 3 and bullet.posx < self.posx + 3 and bullet.posy > self.posy - 3 and bullet.posy < self.posy + 3 and bullet.type != 0: 
                    if bullet.type == 1:
                        self.hp += -1
                    elif bullet.type == 2:
                        self.hp += -5
                    elif bullet.type == 3:
                        self.hp += -10
                    bullet.alive = False

                if not bullet.alive:
                    self.list_bullet.remove(bullet)
            
            self.triangle.update(64,64)

    def draw(self):

        pyxel.cls(0)

        if self.scene == 0:
            pass

        if self.scene == 1:
            for bullet in self.list_bullet:
                bullet.draw()
            pyxel.rect(self.posx - 3,self.posy - 3,7,7,1)
            pyxel.pset(self.posx,self.posy,7)
            self.boss.draw()
            pyxel.rect(120,2,6,124,13)
            pyxel.rect(120,2+124*(1-self.boss.hp_percent),6,124*self.boss.hp_percent,8)
            pyxel.rect(2,66,6,60,13)
            pyxel.rect(2,66+60*(1-self.hp_percent),6,60*self.hp_percent,11)

        self.triangle.draw()

        

    
    def player(self):

        self.velx,self.vely = (pyxel.btn(pyxel.KEY_D) - pyxel.btn(pyxel.KEY_Q)),(pyxel.btn(pyxel.KEY_S) - pyxel.btn(pyxel.KEY_Z))
        
        if pyxel.btn(pyxel.KEY_SPACE) or pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT) or pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                vector = [pyxel.mouse_x - self.posx,pyxel.mouse_y - self.posy]
                if vector[0] == 0:
                    if vector[1] > 0:
                        angle = 90
                    else:
                        angle = 270
                else:
                    if vector[1] > 0:
                        if vector[0] > 0:
                            angle = math.degrees(math.atan(vector[1]/vector[0]))
                        elif vector[0] < 0:
                            angle = math.degrees(math.atan(vector[1]/vector[0])) + 180
                    else:
                        if vector[0] > 0:
                            angle = math.degrees(math.atan(vector[1]/vector[0])) + 360
                        elif vector[0] < 0:
                            angle = math.degrees(math.atan(vector[1]/vector[0])) + 180
            
            else:
                vector = [self.boss.posx - self.posx,self.boss.posy - self.posy]
                if vector[0] == 0:
                    if vector[1] > 0:
                        angle = 90
                    else:
                        angle = 270
                else:
                    if vector[1] > 0:
                        if vector[0] > 0:
                            angle = math.degrees(math.atan(vector[1]/vector[0]))
                        elif vector[0] < 0:
                            angle = math.degrees(math.atan(vector[1]/vector[0])) + 180
                    else:
                        if vector[0] > 0:
                            angle = math.degrees(math.atan(vector[1]/vector[0])) + 360
                        elif vector[0] < 0:
                            angle = math.degrees(math.atan(vector[1]/vector[0])) + 180

            if self.shoot_cd == 0:
                if self.amount_bullet == 1:
                    self.list_bullet += [Bullet(self.posx,self.posy,angle,1,0,0)]
                else:
                    for x in range(int(-self.spread/2),int(self.spread/2)+1,int(self.spread/(self.amount_bullet-1))):
                        self.list_bullet += [Bullet(self.posx,self.posy,angle+x,1,0,0)]
                self.shoot_cd = 10/self.shoot_rate
            
        
        self.posx,self.posy = self.posx + self.velx, self.posy + self.vely
        self.shoot_cd = max(0,self.shoot_cd - 1)
        self.hp_percent = self.hp/self.hp_max

class Bullet:

    def __init__(self,x,y,angle,vel,rot_speed,type) -> None:
        
        self.posx,self.posy = x,y
        self.angle = angle
        self.vel = vel
        self.rot_speed = rot_speed
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

    def __init__(self,x,y,hp_percent,rotation_speed, cubes) -> None:

        self.max_hp = 5000
        self.hp = self.max_hp*hp_percent
        self.hp_percent = hp_percent
        self.speed = 0.5
        self.vel = self.speed

        self.posx = x
        self.posy = y

        self.cubes = [[Cube(15,1),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(cubes)]
        self.cubes += [[Cube(25,2),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(int(cubes/2))]

        self.target = [64,64]
        self.pattern = [[64,16]]
        self.phase = 0

    def update(self):
        
        self.deplacements()
        self.patterns()

        for cube in self.cubes:
            cube[0].update(self.posx,self.posy)
        
        self.hp_percent = self.hp/self.max_hp

    def draw(self):
        for cube in self.cubes:
            cube[0].anglex += cube[1]
            cube[0].angley += cube[1]
            cube[0].anglez += cube[1]
            cube[0].draw()
        pyxel.pset(self.posx,self.posy,7)
        pyxel.pset(*self.target,6)
    
    def deplacements(self):

        vector = [self.target[0] - self.posx,self.target[1] - self.posy]
        if vector[0] == 0:
            if vector[1] > 0:
                angle = 90
            else:
                angle = 270
        else:
            if vector[1] > 0:
                if vector[0] > 0:
                    angle = math.degrees(math.atan(vector[1]/vector[0]))
                elif vector[0] < 0:
                    angle = math.degrees(math.atan(vector[1]/vector[0])) + 180
            else:
                if vector[0] > 0:
                    angle = math.degrees(math.atan(vector[1]/vector[0])) + 360
                elif vector[0] < 0:
                    angle = math.degrees(math.atan(vector[1]/vector[0])) + 180

        self.posx += min((math.cos(math.radians(angle))*self.vel, self.target[0] - self.posx),key=lambda x:abs(x))
        self.posy += min((math.sin(math.radians(angle))*self.vel, self.target[1] - self.posy),key=lambda x:abs(x))

    def patterns(self):

        self.phases()

        self.target = self.pattern[0]
        
        if self.posx == self.target[0] and self.posy == self.target[1]:
            if self.phase == 4:
                self.pattern.append([random.uniform(16,112),random.uniform(16,32)])
                self.pattern.pop(0)
            else:
                self.pattern.append(self.pattern[0])
                self.pattern.pop(0)
    
    def phases(self):

        if self.phase == 0:
            self.pattern = [[16,16],[112,16]]
            self.vel = self.speed
            self.phase = 1
        elif self.phase == 1 and self.hp_percent < 0.75:
            self.pattern = [[64,64]]
            self.vel = self.speed * 0.5
            self.phase = 2
        elif self.phase == 2 and self.hp_percent < 0.5:
            self.pattern = [[16,16],[112,16],[112,112],[16,112]]
            self.vel = self.speed
            self.phase = 3
        elif self.phase == 3 and self.hp_percent < 0.25:
            self.pattern = [[random.uniform(16,112),random.uniform(16,32)]]
            self.vel = self.speed * 0.25
            self.phase = 4

class Cube:

    def __init__(self,size,color) -> None:

        self.corners = [
            [[-1],[-1],[1]],
            [[1],[-1],[1]],
            [[1],[1],[1]],
            [[-1],[1],[1]],
            [[-1],[-1],[-1]],
            [[1],[-1],[-1]],
            [[1],[1],[-1]],
            [[-1],[1],[-1]]
            ]
        self.anglex = 0
        self.angley = 0
        self.anglez = 0
        self.size = size
        self.color = color

        self.posx = 64
        self.posy = 64

    def update(self,x,y):

        self.posx,self.posy = x,y

    
    def draw(self):

        rotationx = [
            [1, 0, 0],
            [0, math.cos(math.radians(self.anglex)), -math.sin(math.radians(self.anglex))],
            [0, math.sin(math.radians(self.anglex)), math.cos(math.radians(self.anglex))]
        ]
        rotationy = [
            [math.cos(math.radians(self.angley)), 0, -math.sin(math.radians(self.angley))],
            [0, 1, 0],
            [math.sin(math.radians(self.angley)), 0, math.cos(math.radians(self.angley))]
        ]
        rotationz = [
            [math.cos(math.radians(self.anglez)), -math.sin(math.radians(self.anglez)), 0],
            [math.sin(math.radians(self.anglez)), math.cos(math.radians(self.anglez)), 0],
            [0, 0, 1]
        ]
        figure2d = []
        for corner in self.corners:
            rotated2d = matrix_multiplication(rotationy, corner)
            rotated2d = matrix_multiplication(rotationx, rotated2d)
            rotated2d = matrix_multiplication(rotationz, rotated2d)
            
            distance = 5
            z = 1/(distance - rotated2d[2][0])
            projection_matrix = [
                [z, 0, 0],
                [0, z, 0]
            ]
            projected_2d = matrix_multiplication(projection_matrix, rotated2d)

            figure2d += [[int(projected_2d[0][0] * (self.size*2)) + self.posx,int(projected_2d[1][0] * (self.size*2)) + self.posy]]

        for k in range(4):
            pyxel.line(*figure2d[k], *figure2d[(k+1)%4],self.color)
            pyxel.line(*figure2d[k + 4], *figure2d[(k+1)%4 +4],self.color)
            pyxel.line(*figure2d[k], *figure2d[k + 4],self.color)

class Triangle:
    
    def __init__(self,size,color):

        self.angle = 0
        self.size = size
        self.color = color

        self.posx = 64
        self.posy = 64

        self.points = [
            [self.posx + ((self.size/2) * math.cos(math.radians(self.angle))),self.posy + ((self.size/2) * math.sin(math.radians(self.angle)))],
            [self.posx + ((self.size/2) * math.cos(math.radians(self.angle + (360/3)))),self.posy + ((self.size/2) * math.sin(math.radians(self.angle + (360/3))))],
            [self.posx + ((self.size/2) * math.cos(math.radians(self.angle + ((360/3)*2)))),self.posy + ((self.size/2) * math.sin(math.radians(self.angle + ((360/3)*2))))]
        ]

    def update(self,x,y):

        self.posx,self.posy = x,y

        self.points = [
            [self.posx + ((self.size/2) * math.cos(math.radians(self.angle))),self.posy + ((self.size/2) * math.sin(math.radians(self.angle)))],
            [self.posx + ((self.size/2) * math.cos(math.radians(self.angle + (360/3)))),self.posy + ((self.size/2) * math.sin(math.radians(self.angle + (360/3))))],
            [self.posx + ((self.size/2) * math.cos(math.radians(self.angle + ((360/3)*2)))),self.posy + ((self.size/2) * math.sin(math.radians(self.angle + ((360/3)*2))))]
        ]

    def draw(self):

        pyxel.line(*self.points[0],*self.points[1],self.color)
        pyxel.line(*self.points[1],*self.points[2],self.color)
        pyxel.line(*self.points[2],*self.points[0],self.color)


def matrix_multiplication(a, b):
    columns_a = len(a[0])
    rows_a = len(a)
    columns_b = len(b[0])
    rows_b = len(b)

    result_matrix = [[j for j in range(columns_b)] for i in range(rows_a)]
    if columns_a == rows_b:
        for x in range(rows_a):
            for y in range(columns_b):
                sum = 0
                for k in range(columns_a):
                    sum += a[x][k] * b[k][y]
                result_matrix[x][y] = sum
        return result_matrix

    else:
        return None


Game()