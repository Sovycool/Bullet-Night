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

        self.menu_enemy = None
        self.enemy = None

        self.menus = None
        self.text_screen = None
        self.highscore = [" X ",0]
        self.score = None
        self.time = None
        self.scene = None
        self.level = None
        self.hold_to_exit = 0

        for x in range(5):
            try:
                open("scoreboards/"+ str(x) +".txt","x").write(" X ,0,0,0,0\n"*13)
            except FileExistsError:
                pass

        self.menu()

        pyxel.run(self.update,self.draw)

    def menu(self):

        self.menus = {
            "menu" : [
                Button(32,64,"Levels",self.levels),
                Button(32,80,"Build",self.build,disabled=True),
                Button(32,96,"Quit game",pyxel.quit)
                ],
            "levels" : [
                Button(16,16,"1 - 1",self.start,[0],True),SmallButton(84,16,self.scoreboard,[0],True),
                Button(16,32,"1 - 2",self.start,[1],True),SmallButton(84,32,self.scoreboard,[1],True),
                Button(16,48,"1 - 3",self.start,[2]),SmallButton(84,48,self.scoreboard,[2]),
                Button(16,64,"1 - 4",self.start,[3],True),SmallButton(84,64,self.scoreboard,[3],True),
                Button(16,80,"1 - Boss",self.start,[4],True),SmallButton(84,80,self.scoreboard,[4],True),
                Button(8,112,"Menu",self.menu)
                ],
            "scoreboard" : [Button(8,112,"Menu",self.levels)],
            "play" : [],
            "score" : [Button(8,112,"Save",self.save)]
        }
        self.text_screen = ""
        self.name = None
        self.scene = "menu"
        self.menu_enemy = Boss(random.randint(8,120),random.randint(8,120),1,666)

    def levels(self):
        self.scene = "levels"
        self.text_screen = ""

    def build(self):
        pass

    def start(self,level):

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

        self.enemy = Boss(64,16,1,level)

        self.time = pyxel.frame_count
        self.name = Name()
        self.scene = "play"
        self.level = level

    def save(self):

        score_line = [self.score[0],self.score[1],int(self.hp_percent*100),int(self.enemy.hp_percent*100),self.time]

        path = "scoreboards/" + str(self.level) + ".txt"

        scoreboard = [x.split(",") for x in open(path, "r").read().split("\n") if x.split(",") != [""]]
        output = []
        while len(scoreboard) < 13:
            scoreboard.append([" X ",0,0,0,0])

        for x in range(13):
            if int(score_line[1]) > int(scoreboard[x][1]):
                output.append(score_line)
                score_line = scoreboard[x]
            else:
                output.append(scoreboard[x])

        scoreboard = open(path, "w+")
        for line in output:
            for item in line[:-1]:
                scoreboard.write(str(item) + ",")
            scoreboard.write(str(line[-1]) + "\n")

        scoreboard.close()

        self.scoreboard()

    def scoreboard(self,level = None):

        if level == None:
            level = self.level

        self.scene = "scoreboard"
        path = "scoreboards/" + str(level) + ".txt"

        scoreboard = [x.split(",") for x in open(path, "r").read().split("\n") if x.split(",") != [""]]
        self.text_screen = "   NAM SCO  HLT  BOS TIM\n\n"
        for index,line in enumerate(scoreboard):
            self.text_screen += (" "*(2-len(str(index+1)))) + str(index+1) + " " + str(line[0]) + " " + str(line[1]) + (" "*(5-len(str(line[1])))) + str(line[2]) + "%" + (" "*(4-len(str(line[2])))) + str(line[3]) + "%" + (" "*(3-len(str(line[3])))) + str(line[4]) + "s\n"

    def update(self):

        if self.scene == "menu":

            self.menu_enemy.update(self)

        if self.scene == "play" or self.scene == "score":
            if self.hp_percent > 0:
                self.player()
            else:
                self.death()
            self.enemy.update(self)
            for bullet in self.bullets:
                bullet.update()
                if bullet.posx > self.enemy.posx - self.enemy.size and bullet.posx < self.enemy.posx + self.enemy.size and bullet.posy > self.enemy.posy - self.enemy.size and bullet.posy < self.enemy.posy + self.enemy.size and bullet.type == 0:
                    self.enemy.hp = max(self.enemy.hp-1,0)
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

            if self.scene == "play":

                if pyxel.btn(pyxel.KEY_BACKSPACE):
                    self.hold_to_exit = min(self.hold_to_exit + 1,100)

                elif pyxel.btnr(pyxel.KEY_BACKSPACE) and self.hold_to_exit == 100:
                    self.hold_to_exit = 0
                    self.levels()

                else:
                    self.hold_to_exit = max(self.hold_to_exit - 1.5,0)

            if self.scene == "score":

                self.name.update()

                self.score = [self.name.name,int(3333*self.hp_percent) + int(3333*(1-self.enemy.hp_percent)) + int((min(3333*(self.enemy.hp_percent == 0),(20*3333)/self.time)))]

                scoreboard = [x.split(",") for x in open("scoreboards/" + str(self.level) + ".txt", "r").read().split("\n") if x.split(",") != [""]]

                for index,line in enumerate(scoreboard):
                    if index == 0:
                       self.highscore = [line[0],int(line[1])]

                if self.score[1] >= self.highscore[1]:
                    self.highscore = [self.score[0],max(self.highscore[1],self.score[1])]

                self.text_screen = "You won the battle !\n\nHealth left : " + str(int(self.hp_percent*100)) + "%\nHealth boss lost : " + str(int((1-self.enemy.hp_percent)*100)) + "%\nTimer : " + str(self.time) + " seconds\n\nHighscore : " + str(self.highscore[0]) + " " + str(self.highscore[1]) + "\nScore : " + str(int(3333*self.hp_percent)) + "+" + str(int(3333*(1-self.enemy.hp_percent))) + "+" + str(int((min(3333*(self.enemy.hp_percent == 0),(20*3333)/self.time))))
            
        for button in self.menus[self.scene]:
            button.update(self)

    def draw(self):

        pyxel.cls(0)

        if self.scene == "menu":

            self.menu_enemy.draw()

            pyxel.bltm(0,0,0,0,0,128,128,0)

        if self.scene == "play" or self.scene == "score":
            for bullet in self.bullets:
                bullet.draw()
            self.enemy.draw()
            pyxel.rect(self.posx - 3,self.posy - 3,7,7,1+(12*(self.hp_percent == 0)))
            pyxel.pset(self.posx,self.posy,7)
            if self.scene == "play":
                pyxel.rect(120,2,6,124,13)
                pyxel.rect(120,2+124*(1-self.enemy.hp_percent),6,124*self.enemy.hp_percent,8)
                pyxel.rect(2,66,6,60,13)
                pyxel.rect(2,66+60*(1-self.hp_percent),6,60*self.hp_percent,11)

                if self.hold_to_exit > 0:
                    pyxel.rectb(4,4,48,3,15)
                    pyxel.rect(4,4,48*(self.hold_to_exit/100),3,15)
                    pyxel.text(4,9,"Hold to exit",15)
            else:
                pyxel.text(48,96,str(self.score[0])+" "+str(self.score[1]),7+(8*int(0.5+((pyxel.frame_count/8)%1))))
                pyxel.text(48,98,str(self.name.selection),7+(8*int(0.5+((pyxel.frame_count/8)%1))))

            for explosion in self.explosions:
                explosion.draw()

        if self.scene == "scoreboard" or self.scene == "score" or self.scene == "levels":
            pyxel.bltm(0,0,0,128,0,128,128,0)
            pyxel.text(16,16,self.text_screen,15)

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
                vector = [self.enemy.posx - self.posx,self.enemy.posy - self.posy]
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

        if self.scene == "play":
            self.deathcd += 1
            if self.deathcd < 20:
                self.explosions += [Explosion(random.uniform(self.posx-6,self.posx+6),random.uniform(self.posy-6,self.posy+6))]
            if self.deathcd >= 30:
                self.bullets = [x for x in self.bullets if x.type != 0]
                self.time = int((pyxel.frame_count - self.time)/60)
                self.scene = "score"



class Bullet:

    def __init__(self,x,y,angle,vel,rot_speed,type):

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

    def __init__(self,x,y,hp_percent,level):

        if level == 0:
            self.hp_max = 1500
            self.speed = 0.3
            self.size = 10

            rotation_speed = 2

            self.cubes = [[Cube(15,6),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])]]

            self.target = [64,64]
            self.moving_patterns = [
            [[16,16],[112,16]],
            [[64,64]],
            [[16,16],[112,16],[112,112],[16,112]],
            [[]],
            [[]]
            ]
            #shooting pattern : posx,posy,angle,vel,rot_speed,type,cd,cd_max,spread,amount,spin?
            self.shooting_patterns = [
            [[None,None,90,1,0,1,100,20,45,3,False],[0,34,0,1,0,3,0,2,0,1,False],[128,34,180,1,0,3,0,2,0,1,False]],
            [[None,None,0,0.5,5,2,100,10,360,3,True],[None,None,0,0.25,0,1,100,100,360,18,False]],
            [[None,None,0,0.25,0,1,100,100,360,20,True],[None,None,0,0.5,0,2,100,200,360,15,True],[None,None,0,0.75,0,3,100,200,360,10,True]],
            [[None,None,0,0.25,0,1,0,100,360,20,True],[None,None,0,0.5,0,2,0,100,360,15,True],[None,None,0,0.75,0,3,0,100,360,10,True]],
            [[]]
            ]

        elif level == 2:
            self.hp_max = 3000
            self.speed = 0.5
            self.size = 12

            rotation_speed = 2

            self.cubes = [[Cube(15,1),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(3)]
            self.cubes += [[Cube(25,2),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])]]

            self.target = [64,64]
            self.moving_patterns = [
            [[16,16],[112,16]],
            [[64,64]],
            [[16,16],[112,16],[112,112],[16,112]],
            [[]],
            [[]]
            ]
            #shooting pattern : posx,posy,angle,vel,rot_speed,type,cd,cd_max,spread,amount,spin?
            self.shooting_patterns = [
            [[None,None,90,1,0,1,100,20,45,3,False],[0,34,0,1,0,3,0,2,0,1,False],[128,34,180,1,0,3,0,2,0,1,False]],
            [[None,None,0,0.5,5,2,100,10,240,3,True],[None,None,0,0.25,0,1,100,100,360,18,False]],
            [[None,None,0,0.25,0,1,100,100,360,20,True],[None,None,0,0.5,0,2,100,200,360,15,True],[None,None,0,0.75,0,3,100,200,360,10,True]],
            [[None,None,0,0.25,0,1,0,100,360,20,True],[None,None,0,0.5,0,2,0,100,360,15,True],[None,None,0,0.75,0,3,0,100,360,10,True]],
            [[]]
            ]


        elif level == 666:

            self.hp_max = 1
            self.speed = 0.25
            self.size = 5

            rotation_speed = 2

            self.cubes = [[Cube(random.randint(10,30),random.randint(0,15)),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(random.randint(1,5))]

            self.target = [64,64]
            self.moving_patterns = [
            [[]]
            ]
            #shooting pattern : posx,posy,angle,vel,rot_speed,type,cd,cd_max,spread,amount,spin?
            self.shooting_patterns = [
            [[]]
            ]

        else:

            self.hp_max = 1
            self.speed = 0
            self.size = 12

            rotation_speed = 2

            self.cubes = [[Cube(20,7),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(1)]

            self.target = [64,64]
            self.moving_patterns = [
            [[]],
            [[]],
            [[]],
            [[]],
            [[]]
            ]
            #shooting pattern : posx,posy,angle,vel,rot_speed,type,cd,cd_max,spread,amount,spin?
            self.shooting_patterns = [
            [[]],
            [[]],
            [[]],
            [[None,None,0,0.75,0,3,0,100,360,10,True]],
            [[]]
            ]

        self.hp = self.hp_max*hp_percent
        self.hp_percent = hp_percent
        self.vel = self.speed

        self.posx = x
        self.posy = y

        if self.hp_percent > 0.75:
            self.phase = 0
        elif self.hp_percent > 0.5:
            self.phase = 1
        elif self.hp_percent > 0.25:
            self.phase = 2
        else:
            self.phase = 3

        self.deathcd = 0
        self.level = level
        self.alive = True

    def update(self,game):

        self.phases()
        self.movements(game)
        self.shoot(game)
        self.death(game)

        for cube in self.cubes:
            cube[0].update(self.posx,self.posy)

        self.hp_percent = self.hp/self.hp_max

    def draw(self):
        for cube in self.cubes:
            if self.phase < 4:
                cube[0].anglex += cube[1]
                cube[0].angley += cube[1]
                cube[0].anglez += cube[1]
            else:
                cube[0].color = 13
            cube[0].draw()
        #pyxel.pset(self.posx,self.posy,7)
        #pyxel.pset(*self.target,6)

    def movements(self,game):

        self.patterns(game)

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

    def patterns(self,game):

        if self.phase == 3 and self.level == 2:
            self.target = [game.posx,game.posy]
        elif self.level == 666:
            if self.posx == self.target[0] and self.posy == self.target[1]:
                self.target = [random.randint(8,120),random.randint(8,120)]
        else:
            self.target = self.moving_patterns[self.phase][0]
            if self.target == []:
               self.target = [self.posx,self.posy]

        if self.posx == self.target[0] and self.posy == self.target[1]:
            self.moving_patterns[self.phase].append(self.moving_patterns[self.phase][0])
            self.moving_patterns[self.phase].pop(0)

    def phases(self):

        if self.phase == 0:
            self.vel = self.speed
        if self.hp_percent <= 0.75 and self.hp_percent > 0.5:
            self.vel = self.speed * 1.5
            self.phase = 1
        elif self.hp_percent <= 0.5 and self.hp_percent > 0.25:
            self.vel = self.speed
            self.phase = 2
        elif self.hp_percent <= 0.25 and self.hp_percent > 0:
            self.vel = self.speed * 0.25
            self.phase = 3
        elif self.hp_percent <= 0:
            self.phase = 4

    def shoot(self,game):

        for pattern in self.shooting_patterns[self.phase]:
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

                    pattern[6] = bullet[7] * min(0.75 + self.hp_percent,1)

                if bullet[10]:
                    pattern[2] -= bullet[3]/2
                pattern[6] = max(0,pattern[6] - 1)

    def death(self,game):

        if self.phase == 4 and self.alive:
            self.deathcd += 1
            if self.deathcd < 30:
                game.explosions += [Explosion(random.uniform(self.posx-12,self.posx+12),random.uniform(self.posy-12,self.posy+12))]
            if self.deathcd >= 30:
                game.bullets = [x for x in game.bullets if x.type == 0]
                game.time = int((pyxel.frame_count - game.time)/60)
                game.scene = "score"
                self.alive = False



class Name:

    def __init__(self):
        self.char = [65,65,65]
        self.name = chr(self.char[0]) + chr(self.char[1]) + chr(self.char[2])
        self.selected_char = 0
        self.selection = "   "

    def update(self):

        underscore = ["_  "," _ ","  _"]

        self.name = chr(self.char[0]) + chr(self.char[1]) + chr(self.char[2])

        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.selected_char += 1
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.selected_char -= 1
        if self.selected_char > 2:
            self.selected_char = 0
        if self.selected_char < 0:
            self.selected_char = 2

        self.selection = underscore[self.selected_char]

        if pyxel.btnp(pyxel.KEY_UP):
            self.char[self.selected_char] += 1
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.char[self.selected_char] -= 1
        for x,char in enumerate(self.char):
            if char > 90:
                self.char[x] = 65
            if char < 65:
                self.char[x] = 90



class Button:

    def __init__(self,x,y,text,function,args = None,disabled = False):
        self.posx,self.posy = x,y
        self.text = text
        self.function = function
        self.args = args
        self.hover = False
        self.disabled = disabled

    def update(self,game):

        if not self.disabled:
            self.hover = pyxel.mouse_x > self.posx and pyxel.mouse_x < self.posx + 64 and pyxel.mouse_y > self.posy and pyxel.mouse_y < self.posy + 8

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.hover:
                pyxel.play(0,1)
                game.shoot_cd = 10
                if self.args == None:
                    self.function()
                else:
                    self.function(*self.args)

    def draw(self):
        if not self.disabled:
            pyxel.blt(self.posx,self.posy,0,0,32+(8*self.hover),64,8,0)
            pyxel.text(self.posx + 10 ,self.posy,self.text,15-(8*self.hover))
        else:
            pyxel.blt(self.posx,self.posy,0,0,48,64,8,0)
            pyxel.text(self.posx + 10 ,self.posy,self.text,8)



class SmallButton:

    def __init__(self,x,y,function,args = None,disabled = False):
        self.posx,self.posy = x,y
        self.function = function
        self.args = args
        self.hover = False
        self.disabled = disabled

    def update(self,game):
        if not self.disabled:
            self.hover = pyxel.mouse_x > self.posx and pyxel.mouse_x < self.posx + 8 and pyxel.mouse_y > self.posy and pyxel.mouse_y < self.posy + 8

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.hover:
                pyxel.play(0,1)
                game.shoot_cd = 10
                if self.args == None:
                    self.function()
                else:
                    self.function(*self.args)

    def draw(self):
        if not self.disabled:
            pyxel.blt(self.posx,self.posy,0,64,32+(8*self.hover),8,8,0)
        else:
            pyxel.blt(self.posx,self.posy,0,64,48,8,8,0)


class Cube:

    def __init__(self,size,color):

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