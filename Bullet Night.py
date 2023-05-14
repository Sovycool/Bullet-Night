import pyxel
import math
import random


class Game():

    def __init__(self):

        pyxel.init(128,128,"NDC 2023",60)
        pyxel.mouse(True)
        pyxel.load('res.pyxres')

        self.posx,self.posy = None,None
        self.velx,self.vely = None,None
        self.hp_max = None
        self.hp = None
        self.hp_percent = None
        self.deathcd = None

        self.shoot_cd = None
        self.shoot_rate = None
        self.spread = None
        self.amount_bullet = None
        self.bullets = None

        self.explosions = None

        self.boss = None

        self.menus = None
        self.scoreboard = None
        self.highscore = ["",0]
        self.score = None
        self.time = None
        self.scene = None

        self.menu()

        pyxel.run(self.update,self.draw)

    def menu(self):

        self.menus = [
            [Button(32,64,"Start",self.start),Button(32,80,"Quit game",pyxel.quit)],
            [],
            [],
            [Button(8,112,"Restart",self.menu)]
        ]
        self.scoreboard = ""
        self.score = ["",0]
        self.scene = 0

    def start(self):

        self.posx,self.posy = 64,96
        self.velx,self.vely = 0,0
        self.hp_max = 100
        self.hp = self.hp_max
        self.hp_percent = 1
        self.deathcd = 0

        self.shoot_rate = 2
        self.spread = 10
        self.amount_bullet = 3
        self.bullets = []

        self.explosions = []

        self.boss = Boss(64,16,0.01,2,3)

        self.time = pyxel.frame_count
        self.scene = 2

    def update(self):
        
        if self.scene == 2 or self.scene == 3:
            if self.hp_percent > 0:
                self.player()
            else:
                self.death()
            self.boss.update(self)
            for bullet in self.bullets:
                bullet.update()
                if bullet.posx > self.boss.posx - 12 and bullet.posx < self.boss.posx + 12 and bullet.posy > self.boss.posy - 12 and bullet.posy < self.boss.posy + 12 and bullet.type == 0:
                    self.boss.hp = max(self.boss.hp-1,0)
                    bullet.alive = False
                if bullet.posx > self.posx - 3 and bullet.posx < self.posx + 3 and bullet.posy > self.posy - 3 and bullet.posy < self.posy + 3 and bullet.type != 0: 
                    if bullet.type == 1:
                        self.hp = max(self.hp-1,0)
                    elif bullet.type == 2:
                        self.hp = max(self.hp-5,0)
                    elif bullet.type == 3:
                        self.hp = max(self.hp-10,0)
                    bullet.alive = False

                if not bullet.alive:
                    self.bullets.remove(bullet)
            
            for explosion in self.explosions:
                explosion.update()
                if explosion.tick > 8:
                    self.explosions.remove(explosion)
            
            if self.scene == 3:

                self.score = ["",int(1000*self.hp_percent) + int(1000*(1-self.boss.hp_percent)) + int((min(1000*(self.boss.hp_percent == 0),20000/self.time)))]

                self.highscore = [self.highscore[0],max(self.highscore[1],self.score[1])]

                self.scoreboard = "You won the battle !\n\nHealth left : " + str(int(self.hp_percent*100)) + "%\nHealth boss lost : " + str(int((1-self.boss.hp_percent)*100)) + "%\nTimer : " + str(self.time) + " seconds\nScore : " + str(int(1000*self.hp_percent)) + "+" + str(int(1000*(1-self.boss.hp_percent))) + "+" + str(int((min(1000*(self.boss.hp_percent == 0),20000/self.time)))) + "\n      = " + str(self.score[1]) +"\n\nHighscore : " + str(self.highscore[1])

        for button in self.menus[self.scene]:
            button.update(self)

    def draw(self):

        pyxel.cls(0)

        if self.scene == 0:
            pyxel.bltm(0,0,0,0,0,128,128,0)

        if self.scene == 2 or self.scene == 3:
            for bullet in self.bullets:
                bullet.draw()
            self.boss.draw()
            pyxel.rect(self.posx - 3,self.posy - 3,7,7,1+(12*(self.hp_percent == 0)))
            pyxel.pset(self.posx,self.posy,7)
            if self.scene == 2:
                pyxel.rect(120,2,6,124,13)
                pyxel.rect(120,2+124*(1-self.boss.hp_percent),6,124*self.boss.hp_percent,8)
                pyxel.rect(2,66,6,60,13)
                pyxel.rect(2,66+60*(1-self.hp_percent),6,60*self.hp_percent,11)
            else:
                pyxel.bltm(0,0,0,128,0,128,128,0)
                pyxel.text(16,16,self.scoreboard,15)

            for explosion in self.explosions:
                explosion.draw()

        for button in self.menus[self.scene]:
                button.draw()
    
    def player(self):

        self.velx,self.vely = (pyxel.btn(pyxel.KEY_D) - pyxel.btn(pyxel.KEY_Q))/2,(pyxel.btn(pyxel.KEY_S) - pyxel.btn(pyxel.KEY_Z))/2
        
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
                pyxel.play(0,1)
                if self.amount_bullet == 1:
                    self.bullets += [Bullet(self.posx,self.posy,angle,1,0,0)]
                else:
                    for x in range(int(-self.spread/2),int(self.spread/2)+1,int(self.spread/(self.amount_bullet-1))):
                        self.bullets += [Bullet(self.posx,self.posy,angle+x,1,0,0)]

                self.shoot_cd = 10/self.shoot_rate

        if self.posx + self.velx - 3 > 0 and self.posx + self.velx + 3 < 128:
            self.posx = self.posx + self.velx
        if self.posy + self.vely - 3 > 0 and self.posy + self.vely + 3 < 128:
            self.posy = self.posy + self.vely
        self.shoot_cd = max(0,self.shoot_cd - 1)
        self.hp_percent = self.hp/self.hp_max

    def death(self):

        if self.scene == 2:
            self.deathcd += 1
            print(self.deathcd)
            if self.deathcd < 20:
                self.explosions += [Explosion(random.uniform(self.posx-6,self.posx+6),random.uniform(self.posy-6,self.posy+6))]
            if self.deathcd >= 30:
                self.bullets = [x for x in self.bullets if x.type != 0]
                self.time = int((pyxel.frame_count - self.time)/60)
                self.scene = 3



class Bullet:

    def __init__(self,x,y,angle,vel,rot_speed,type) -> None:
        
        self.posx,self.posy = x,y
        self.angle = angle
        self.graphic_angle = 0
        self.vel = vel
        self.rot_speed = rot_speed
        self.type = type
        self.alive = True

    def update(self):

        self.posx,self.posy = self.posx + math.cos(math.radians(self.angle))*self.vel,self.posy + math.sin(math.radians(self.angle))*self.vel
        self.angle += self.rot_speed
        self.graphic_angle += 3
        self.rot_speed = self.rot_speed*0.98
        if self.posx > 192 or self.posx < -64 or self.posy > 192 or self.posy < -64:
            self.alive = False

    def draw(self):

        if self.type == 0:
            pyxel.circ(self.posx,self.posy,1,10)
        if self.type == 1:
            pyxel.circ(self.posx,self.posy,1,6)
        if self.type == 2:
            triangle(self.posx,self.posy,self.graphic_angle,5,11)
        if self.type == 3:
            square(self.posx,self.posy,self.graphic_angle,4,3)



class Boss:

    def __init__(self,x,y,hp_percent,rotation_speed, cubes) -> None:

        self.hp_max = 5000
        self.hp = self.hp_max*hp_percent
        self.hp_percent = hp_percent
        self.speed = 0.5
        self.vel = self.speed

        self.posx = x
        self.posy = y

        self.cubes = [[Cube(15,1),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(cubes)]
        self.cubes += [[Cube(25,2),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(int(cubes/2))]

        self.target = [64,64]
        self.pattern = [[64,16]]
        #posx,posy,angle,vel,rot_speed,type,cd,cd_max,spread,amount,spin?
        self.shooting_pattern = []
        if self.hp_percent == 1:
            self.phase = 0
        elif self.hp_percent > 0.75:
            self.phase = 1
        elif self.hp_percent > 0.5:
            self.phase = 2
        elif self.hp_percent > 0.25:
            self.phase = 3
        else:
            self.phase = 4

        self.deathcd = 0

    def update(self,game):

        self.phases()
        self.deplacements()
        self.shoot(game)
        self.death(game)

        for cube in self.cubes:
            cube[0].update(self.posx,self.posy)
        
        self.hp_percent = self.hp/self.hp_max

    def draw(self):
        for cube in self.cubes:
            if self.phase < 6:
                cube[0].anglex += cube[1]
                cube[0].angley += cube[1]
                cube[0].anglez += cube[1]
            else:
                cube[0].color = 13
            cube[0].draw()
        #pyxel.pset(self.posx,self.posy,7)
        #pyxel.pset(*self.target,6)
    
    def deplacements(self):

        self.patterns()

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

    def shoot(self,game):

        for pattern in self.shooting_pattern:
            bullet = [x for x in pattern]
            if len(bullet) > 0:
                if bullet[0] == None:
                    bullet[0] = self.posx
                if bullet[1] == None:
                    bullet[1] = self.posy

                if bullet[6] == 0:
                    if bullet[9] == 1:
                        game.bullets += [Bullet(*bullet[0:6])]
                    elif bullet[8] == 360:
                        for x in range(int(-bullet[8]/2),int(bullet[8]/2)+1,int(bullet[8]/(bullet[9]))):
                            game.bullets += [Bullet(*bullet[0:2],bullet[2]+x,*bullet[3:6])]
                    else:
                        for x in range(int(-bullet[8]/2),int(bullet[8]/2)+1,int(bullet[8]/(bullet[9]-1))):
                            game.bullets += [Bullet(*bullet[0:2],bullet[2]+x,*bullet[3:6])]

                    pattern[6] = bullet[7]

                if bullet[10]:
                    pattern[2] -= bullet[3]/2            
                pattern[6] = max(0,pattern[6] - 1)
                

    def patterns(self):

        self.target = self.pattern[0]
        
        if self.posx == self.target[0] and self.posy == self.target[1]:
            if self.phase == 4:
                self.pattern.append([random.uniform(16,112),random.uniform(16,112)])
                self.pattern.pop(0)
            else:
                self.pattern.append(self.pattern[0])
                self.pattern.pop(0)
    
    def phases(self):

        #shooting pattern : posx,posy,angle,vel,rot_speed,type,cd,cd_max,spread,amount,spin?

        if self.phase == 0:
            self.pattern = [[16,16],[112,16]]
            self.shooting_pattern = [[None,None,90,1,0,1,100,20,45,3,False],[0,34,0,1,0,3,0,10,0,1,False]]
            self.vel = self.speed
            self.phase = 1
        elif self.phase == 1 and self.hp_percent < 0.75:
            self.pattern = [[64,64]]
            self.shooting_pattern = [[None,None,0,0.5,5,2,100,10,360,3,True],[None,None,0,0.25,0,1,100,100,360,18,False]]
            self.vel = self.speed * 1.5
            self.phase = 2
        elif self.phase == 2 and self.hp_percent < 0.5:
            self.pattern = [[16,16],[112,16],[112,112],[16,112]]
            self.shooting_pattern = [[None,None,0,0.25,0,1,100,100,360,20,False],[None,None,0,0.5,0,2,100,200,360,15,False],[None,None,0,0.75,0,3,100,200,360,10,False]]
            self.vel = self.speed
            self.phase = 3
        elif self.phase == 3 and self.hp_percent < 0.25:
            self.pattern = [[random.uniform(16,112),random.uniform(16,112)]]
            self.shooting_pattern = [[None,None,0,0.25,0,1,0,100,360,20,False],[None,None,0,0.5,0,2,0,100,360,15,False],[None,None,0,0.75,0,3,0,100,360,10,False]]
            self.vel = self.speed * 0.25
            self.phase = 4
        elif self.phase == 4 and self.hp_percent <= 0:
            self.pattern = [[self.posx,self.posy]]
            self.shooting_pattern = [[]]
            self.phase = 5

    def death(self,game):

        if self.phase == 5:
            self.deathcd += 1
            if self.deathcd < 30:
                game.explosions += [Explosion(random.uniform(self.posx-12,self.posx+12),random.uniform(self.posy-12,self.posy+12))]
            if self.deathcd >= 30:
                self.phase = 6
                game.bullets = [x for x in game.bullets if x.type != 0]
                game.time = int((pyxel.frame_count - game.time)/60)
                game.scene = 3



class Button:

    def __init__(self,x,y,text,function) -> None:
        self.posx,self.posy = x,y
        self.text = text
        self.function = function
        self.hover = False

    def update(self,game):
        self.hover = pyxel.mouse_x > self.posx and pyxel.mouse_x < self.posx + 64 and pyxel.mouse_y > self.posy and pyxel.mouse_y < self.posy + 16

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.hover:
            game.shoot_cd = 10
            self.function()

    def draw(self):
        pyxel.blt(self.posx,self.posy,0,0,32+(8*self.hover),64,8,0)
        pyxel.text(self.posx + 10 ,self.posy,self.text,15-(8*self.hover))



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



class Explosion:

    def __init__(self,x,y):
        self.posx,self.posy = x,y
        self.tick = 0
        self.full = random.choice((0,1))

    def update(self):
        self.tick += 0.5

    def draw(self):
        if self.full:
            pyxel.circ(self.posx,self.posy,self.tick,9+(int(self.tick)%2))
        else:
            pyxel.circb(self.posx,self.posy,self.tick,9+(int(self.tick)%2))



def triangle(x,y,angle,size,color):

    points = [
            [x + ((size/2) * math.cos(math.radians(angle))),y + ((size/2) * math.sin(math.radians(angle)))],
            [x + ((size/2) * math.cos(math.radians(angle + 120))),y + ((size/2) * math.sin(math.radians(angle + 120)))],
            [x + ((size/2) * math.cos(math.radians(angle + 240))),y + ((size/2) * math.sin(math.radians(angle + 240)))]
        ]

    pyxel.trib(*points[0],*points[1],*points[2],color)


def square(x,y,angle,size,color):

    points = [
            [x + (((size*math.sqrt(2))/2) * math.cos(math.radians(angle + 45))),y + (((size*math.sqrt(2))/2) * math.sin(math.radians(angle + 45)))],
            [x + (((size*math.sqrt(2))/2) * math.cos(math.radians(angle + 135))),y + (((size*math.sqrt(2))/2) * math.sin(math.radians(angle + 135)))],
            [x + (((size*math.sqrt(2))/2) * math.cos(math.radians(angle + 225))),y + (((size*math.sqrt(2))/2) * math.sin(math.radians(angle + 225)))],
            [x + (((size*math.sqrt(2))/2) * math.cos(math.radians(angle + 315))),y + (((size*math.sqrt(2))/2) * math.sin(math.radians(angle + 315)))]
        ]

    pyxel.line(*points[0],*points[1],color)
    pyxel.line(*points[1],*points[2],color)
    pyxel.line(*points[2],*points[3],color)
    pyxel.line(*points[3],*points[0],color)


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