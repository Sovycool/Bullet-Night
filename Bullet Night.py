import pyxel
import math
import random



class Game:


    def __init__(self):

        pyxel.init(128,128,"Bullet Night",60)
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
        self.counters = []

        self.menu_boss = None
        self.boss = None

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

    def update(self):


        #if self.bullets != None and len(self.bullets) > 0:
        #    print(self.bullets[0].dummy)

        if self.scene == "menu":

            self.menu_boss.update()

        if self.scene == "play" or self.scene == "score":
            if self.hp_percent > 0:
                self.player()
            else:
                self.death()
            self.boss.update()
            for bullet in self.bullets:
                bullet.update()
                if bullet.posx > self.boss.posx - self.boss.size and bullet.posx < self.boss.posx + self.boss.size and bullet.posy > self.boss.posy - self.boss.size and bullet.posy < self.boss.posy + self.boss.size and bullet.type == 0:
                    new_counter = True
                    for counter in self.counters:
                        if counter.entity == self.boss and counter.live_time > 0:
                            new_counter = False
                            break
                    if new_counter:
                        self.counters.append(DamageCounter(self.boss))

                    self.boss.hp = max(self.boss.hp-1,0)
                    bullet.alive = False
                if bullet.posx > self.posx - 3 and bullet.posx < self.posx + 3 and bullet.posy > self.posy - 3 and bullet.posy < self.posy + 3 and bullet.type != 0:
                    new_counter = True
                    for counter in self.counters:
                        if counter.entity == self and counter.live_time > 0:
                            new_counter = False
                            break
                    if new_counter:
                        self.counters.append(DamageCounter(self))

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

            for counter in self.counters:
                counter.update()
                if not counter.alive:
                    self.counters.remove(counter)

            if self.scene == "play":

                if pyxel.btn(pyxel.KEY_BACKSPACE):
                    self.hold_to_exit = min(self.hold_to_exit + 1,50)

                elif pyxel.btnr(pyxel.KEY_BACKSPACE) and self.hold_to_exit == 50:
                    self.hold_to_exit = 0
                    self.levels()

                else:
                    self.hold_to_exit = max(self.hold_to_exit - 1.5,0)

            if self.scene == "score":

                self.name.update()

                self.score = [self.name.name,int(3333*self.hp_percent) + int(3333*(1-self.boss.hp_percent)) + int((min(3333*(self.boss.hp_percent == 0),(20*3333)/self.time)))]

                if self.level != None:

                    scoreboard = [x.split(",") for x in open("scoreboards/" + str(self.level) + ".txt", "r").read().split("\n") if x.split(",") != [""]]

                    for index,line in enumerate(scoreboard):
                        if index == 0:
                            self.highscore = [line[0],int(line[1])]

                    if self.score[1] >= self.highscore[1]:
                        self.highscore = [self.score[0],max(self.highscore[1],self.score[1])]

                else:

                    self.highscore = [self.score[0],self.score[1]]

                self.text_screen = "You won the battle !\n\nHealth left : " + str(int(self.hp_percent*100)) + "%\nHealth boss lost : " + str(int((1-self.boss.hp_percent)*100)) + "%\nTimer : " + str(self.time) + " seconds\n\nHighscore : " + str(self.highscore[0]) + " " + str(self.highscore[1]) + "\nScore : " + str(int(3333*self.hp_percent)) + "+" + str(int(3333*(1-self.boss.hp_percent))) + "+" + str(int((min(3333*(self.boss.hp_percent == 0),(20*3333)/self.time))))

        for button in self.menus[self.scene]:
            button.update()

    def draw(self):

        pyxel.cls(0)

        if self.scene == "menu":

            self.menu_boss.draw()

            pyxel.bltm(0,0,0,0,0,128,128,0)

        if self.scene == "play" or self.scene == "score":
            for bullet in self.bullets:
                bullet.draw()
            self.boss.draw()
            pyxel.rect(self.posx - 3,self.posy - 3,7,7,1+(12*(self.hp_percent == 0)))
            pyxel.pset(self.posx,self.posy,7)
            if self.scene == "play":
                pyxel.rect(120,2,6,124,13)
                pyxel.rect(120,2+124*(1-self.boss.hp_percent),6,124*self.boss.hp_percent,8)
                pyxel.rect(2,66,6,60,13)
                pyxel.rect(2,66+60*(1-self.hp_percent),6,60*self.hp_percent,11)

                if self.hold_to_exit > 0:
                    pyxel.rectb(4,4,49,3,15)
                    pyxel.rect(4,4,49*(self.hold_to_exit/50),3,15)
                    pyxel.text(5,9,"Hold to exit",15)
            else:
                pyxel.text(48,96,str(self.score[0])+" "+str(self.score[1]),7+(8*int(0.5+((pyxel.frame_count/8)%1))))
                pyxel.text(48,98,str(self.name.selection),7+(8*int(0.5+((pyxel.frame_count/8)%1))))

            for explosion in self.explosions:
                explosion.draw()

            for counter in self.counters:
                counter.draw()

        if self.scene == "scoreboard" or self.scene == "score" or self.scene == "levels":
            pyxel.bltm(0,0,0,128,0,128,128,0)
            pyxel.text(16,16,self.text_screen,15)

        for button in self.menus[self.scene]:
                button.draw()

    def menu(self):

        self.menus = {
            "menu" : [
                Button(32,64,"Levels",self.levels,self),
                Button(32,80,"Build",self.build,self,disabled=True),
                Button(32,96,"Quit game",pyxel.quit,self)
                ],
            "levels" : [
                Button(16,16,"1 - 1",self.start,self,[0]),SmallButton(84,16,self.scoreboard,self,[0]),
                Button(16,32,"1 - 2",self.start,self,[1]),SmallButton(84,32,self.scoreboard,self,[1]),
                Button(16,48,"1 - 3",self.start,self,[2]),SmallButton(84,48,self.scoreboard,self,[2]),
                Button(16,64,"1 - 4",self.start,self,[3],True),SmallButton(84,64,self.scoreboard,self,[3],True),
                Button(16,80,"1 - Boss",self.start,self,[4],True),SmallButton(84,80,self.scoreboard,self,[4],True),
                Button(16,96,"Test Map",self.start,self,[None]),
                Button(8,112,"Menu",self.menu,self)
                ],
            "scoreboard" : [Button(8,112,"Menu",self.levels,self)],
            "play" : [],
            "score" : [Button(8,112,"Save",self.save,self)]
        }
        self.text_screen = ""
        self.name = None
        self.scene = "menu"
        self.menu_boss = Boss(random.randint(8,120),random.randint(8,120),1,666,self)

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

        self.boss = Boss(64,16,1,level,self)

        self.time = pyxel.frame_count
        self.name = Name()
        self.scene = "play"
        self.level = level

    def save(self):

        if self.level != None:

            score_line = [self.score[0],self.score[1],int(self.hp_percent*100),int(self.boss.hp_percent*100),self.time]

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

        self.scene = "scoreboard"

        if level == None:
            level = self.level
        else:
            self.level = level

        if self.level != None:

            path = "scoreboards/" + str(level) + ".txt"

            scoreboard = [x.split(",") for x in open(path, "r").read().split("\n") if x.split(",") != [""]]
            self.text_screen = "   NAM SCO  HLT  BOS TIM\n\n"
            for index,line in enumerate(scoreboard):
                self.text_screen += (" "*(2-len(str(index+1)))) + str(index+1) + " " + str(line[0]) + " " + str(line[1]) + (" "*(5-len(str(line[1])))) + str(line[2]) + "%" + (" "*(4-len(str(line[2])))) + str(line[3]) + "%" + (" "*(3-len(str(line[3])))) + str(line[4]) + "s\n"

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
                    self.bullets += [Bullet(self.posx,self.posy,angle,1,0,0,self)]
                else:
                    for x in range(int(-self.spread/2),int(self.spread/2)+1,int(self.spread/(self.amount_bullet-1))):
                        self.bullets += [Bullet(self.posx,self.posy,angle+x,1,0,0,self)]

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


    def __init__(self,x,y,angle,vel,pattern,type,game,dummy = None):

        if pattern == 1:
            self.dummy = 5
        elif pattern == 2:
            self.dummy = [0,dummy]

        self.posx,self.posy = x,y
        self.angle = angle
        self.graphic_angle = 0
        self.vel = vel
        self.pattern = pattern
        self.type = type
        self.alive = True

        self.game = game

    def update(self):

        if self.pattern == 0:
            angle = self.angle
        elif self.pattern == 1:
            self.angle += self.dummy
            angle = self.angle
            self.dummy = self.dummy*0.98
        elif self.pattern == 2:
            angle = self.angle + self.dummy[1]*math.cos(math.radians(self.dummy[0]))
            self.dummy[0] += 5

        self.posx,self.posy = self.posx + math.cos(math.radians(angle))*self.vel,self.posy + math.sin(math.radians(angle))*self.vel
        self.graphic_angle += 3
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
        if self.type == 4:
            prism = Prism(20,5)
            prism.posx,prism.posy,prism.angley = self.posx,self.posy,self.graphic_angle
            prism.draw()


class Boss:


    def __init__(self,x,y,hp_percent,level,game):

        if level == 0:
            self.hp_max = 1500
            self.vel = 0.3
            self.size = 10

            rotation_speed = 2

            self.cubes = [[Cube(15,4),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])]]

            self.target = [64,64]
            self.moving_patterns = [
            [[16,16],[112,16]],
            [[64,64]],
            [[64,64]]
            ]
            #shooting pattern : posx,posy,angle,vel,pattern,type,cd,cd_max,spread,amount,spin?
            self.shooting_patterns = [
            [[None,None,90,1,0,1,100,20,45,3,False,None],[0,34,0,1,0,3,0,2,0,1,False,None],[128,34,180,1,0,3,0,2,0,1,False,None]],
            [[64,64,0,0.5,1,2,100,15,360,2,True,None],[64,64,90,0.5,1,1,100,15,180,8,True,None]],
            [[64,64,90,0.5,0,2,0,20,360,4,True,None],[64,64,45,0.6,0,1,0,20,360,4,True,None]]
            ]

        elif level == 1:

            self.hp_max = 1
            self.vel = 0
            self.size = 12

            rotation_speed = 2

            self.cubes = [[Cube(20,7),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(1)]

            self.target = [64,64]
            self.moving_patterns = [
            [[]]
            ]
            #shooting pattern : posx,posy,angle,vel,rot_speed,type,cd,cd_max,spread,amount,spin?
            self.shooting_patterns = [
            [[]]
            ]

        elif level == 2:
            self.hp_max = 3000
            self.vel = 0.5
            self.size = 12

            rotation_speed = 2

            self.cubes = [[Cube(15,1),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(3)]
            self.cubes += [[Cube(25,2),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])]]

            self.target = [64,64]
            self.moving_patterns = [
            [[16,16],[112,16]],
            [[64,64]],
            [[112,16],[112,112],[16,112],[16,16]],
            [[]]
            ]
            #shooting pattern : posx,posy,angle,vel,pattern,type,cd,cd_max,spread,amount,spin?
            self.shooting_patterns = [
            [[None,0,90,0.5,0,1,0,20,180,8,False,None]],
            [[64,64,0,0.5,0,2,100,10,360,6,True,None],[64,64,0,0.25,0,1,100,100,360,18,False,None]],
            [[None,None,0,0.25,0,1,100,100,360,20,True,None],[None,None,0,0.5,1,2,100,200,360,15,True,None],[None,None,0,0.75,1,3,100,200,360,10,True,None]],
            [[None,None,0,0.5,1,2,0,100,360,15,True,None],[None,None,0,0.75,1,3,0,100,360,10,True,None]]
            ]

        elif level == 3:

            self.hp_max = 1
            self.vel = 0
            self.size = 12

            rotation_speed = 2

            self.cubes = [[Cube(20,7),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(1)]

            self.target = [64,64]
            self.moving_patterns = [
            [[]]
            ]
            #shooting pattern : posx,posy,angle,vel,rot_speed,type,cd,cd_max,spread,amount,spin?
            self.shooting_patterns = [
            [[]]
            ]

        elif level == 4:

            self.hp_max = 1
            self.vel = 0
            self.size = 12

            rotation_speed = 2

            self.cubes = [[Cube(20,7),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(1)]

            self.target = [64,64]
            self.moving_patterns = [
            [[]]
            ]
            #shooting pattern : posx,posy,angle,vel,rot_speed,type,cd,cd_max,spread,amount,spin?
            self.shooting_patterns = [
            #[[None,0,90,0.5,0,1,0,40,180,8,False],[None,128,270,0.5,0,1,0,40,180,8,False],[0,None,0,0.5,0,1,0,40,180,8,False],[128,None,180,0.5,0,1,0,40,180,8,False]]
            [[]]
            ]

        elif level == 666:

            self.hp_max = 1
            self.vel = 0.25
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

            self.hp_max = 100
            self.vel = 2
            self.size = 12

            rotation_speed = 2

            self.cubes = [[Cube(20,7),random.uniform(rotation_speed*0.90,rotation_speed*1.1)*random.choice([-1,1])] for i in range(1)]

            self.target = [64,64]
            self.moving_patterns = [
            [[64,64]]
            ]
            #shooting pattern : posx,posy,angle,vel,pattern,type,cd,cd_max,spread,amount,spin?,dummy
            self.shooting_patterns = [
            [[None,None,0,1,2,2,0,10,0,1,False,45],[None,None,0,1,2,1,0,10,0,1,False,-45]]
            ]

        if len(self.shooting_patterns) == len(self.moving_patterns):
            self.number_of_phases = len(self.shooting_patterns)
        else:
            assert False, f"Not same amount of moving and shooting patterns of boss number {level}"

        self.hp = self.hp_max*hp_percent
        self.hp_percent = hp_percent

        self.posx = x
        self.posy = y

        self.phase = 0

        self.deathcd = 0
        self.level = level
        self.alive = True

        self.game = game

    def update(self):

        if self.alive:

            self.phases()
            self.movements()
            self.shoot()
            self.death()

            for cube in self.cubes:
                cube[0].update(self.posx,self.posy)

            self.hp_percent = self.hp/self.hp_max

    def draw(self):
        for cube in self.cubes:
            if self.alive:
                cube[0].anglex += cube[1]
                cube[0].angley += cube[1]
                cube[0].anglez += cube[1]
            else:
                cube[0].color = 13
            cube[0].draw()

        pyxel.blt(self.posx-11,self.posy-8,0,40,56,24,16,0)

        if self.alive:
            if self.level == 666:
                angle = angle_from_vector(self.posx,self.posy,pyxel.mouse_x,pyxel.mouse_y)
                pyxel.circ(self.posx + (math.cos(math.radians(angle))*min(2,pyxel.mouse_x-self.posx,key=lambda x:abs(x))),self.posy + (math.sin(math.radians(angle))*min(2,pyxel.mouse_y-self.posy-1,key=lambda x:abs(x))) - 1,2,self.cubes[0][0].color)
            else:
                angle = angle_from_vector(self.posx,self.posy,self.game.posx,self.game.posy)
                pyxel.circ(self.posx + (math.cos(math.radians(angle))*min(2,self.game.posx-self.posx,key=lambda x:abs(x))),self.posy + (math.sin(math.radians(angle))*min(2,self.game.posy-self.posy-1,key=lambda x:abs(x))) - 1,2,self.cubes[0][0].color)

        #pyxel.pset(self.posx,self.posy,7)
        #pyxel.pset(*self.target,6)

    def movements(self):

        if self.phase != self.number_of_phases:
            self.patterns()

        angle = angle_from_vector(self.posx,self.posy,*self.target)

        self.posx += min((math.cos(math.radians(angle))*self.vel, self.target[0] - self.posx),key=lambda x:abs(x))
        self.posy += min((math.sin(math.radians(angle))*self.vel, self.target[1] - self.posy),key=lambda x:abs(x))

    def patterns(self):

        if (self.level == 2 and self.phase == 3) or self.level == 666:
            if not self.level == 666:
                self.vel = 0.125
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

        for x in range(self.number_of_phases):
            if self.hp_percent <= (1/self.number_of_phases)*(self.number_of_phases-x) and self.hp_percent > (1/self.number_of_phases)*(self.number_of_phases-(x+1)):
                self.phase = x
        if self.hp_percent <= 0:
            self.phase = self.number_of_phases
            self.target = [self.posx,self.posy]

    def shoot(self):

        if self.phase != self.number_of_phases:
            for pattern in self.shooting_patterns[self.phase]:
                bullet = [x for x in pattern]
                if len(bullet) > 0:
                    if bullet[0] == None:
                        bullet[0] = self.posx
                    if bullet[1] == None:
                        bullet[1] = self.posy

                    if bullet[6] == 0:
                        if bullet[9] == 1:
                            self.game.bullets += [Bullet(*bullet[0:6],self.game,bullet[11])]

                        elif bullet[8] == 360:
                            for x in range(bullet[9]):
                                self.game.bullets += [Bullet(*bullet[0:2],bullet[2]-(bullet[8]/2)+((bullet[8]/bullet[9])*x),*bullet[3:6],self.game,bullet[11])]
                        else:
                            for x in range(bullet[9]):
                                self.game.bullets += [Bullet(*bullet[0:2],bullet[2]-(bullet[8]/2)+((bullet[8]/(bullet[9]-1))*x),*bullet[3:6],self.game,bullet[11])]
                        try:
                            pattern[6] = bullet[7] * min(1,0.25 + (self.hp/(self.hp_max/self.number_of_phases)))
                        except ZeroDivisionError:
                            pass

                    if bullet[10]:
                        pattern[2] -= bullet[3]
                    pattern[6] = max(0,pattern[6] - 1)

    def death(self):

        if self.phase == self.number_of_phases and self.alive:
            self.deathcd += 1
            if self.deathcd < 30:
                self.game.explosions += [Explosion(random.uniform(self.posx-12,self.posx+12),random.uniform(self.posy-12,self.posy+12))]
            if self.deathcd >= 30:
                self.game.bullets = [x for x in self.game.bullets if x.type == 0]
                self.game.time = int((pyxel.frame_count - self.game.time)/60)
                self.game.scene = "score"
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


    def __init__(self,x,y,text,function,game,args = None,disabled = False):
        self.posx,self.posy = x,y
        self.text = text
        self.function = function
        self.args = args
        self.hover = False
        self.disabled = disabled

        self.game = game

    def update(self):

        if not self.disabled:
            self.hover = pyxel.mouse_x > self.posx and pyxel.mouse_x < self.posx + 64 and pyxel.mouse_y > self.posy and pyxel.mouse_y < self.posy + 8

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.hover:
                pyxel.play(0,1)
                self.game.shoot_cd = 10
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


    def __init__(self,x,y,function,game,args = None,disabled = False):
        self.posx,self.posy = x,y
        self.function = function
        self.args = args
        self.hover = False
        self.disabled = disabled

        self.game = game

    def update(self):
        if not self.disabled:
            self.hover = pyxel.mouse_x > self.posx and pyxel.mouse_x < self.posx + 8 and pyxel.mouse_y > self.posy and pyxel.mouse_y < self.posy + 8

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.hover:
                pyxel.play(0,1)
                self.game.shoot_cd = 10
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


class Prism:


    def __init__(self,size,color):

        self.corners = [
            [[0],[-1],[0]],
            [[0],[-1],[0]],
            [[1],[1],[1]],
            [[-1],[1],[1]],
            [[0],[-1],[0]],
            [[0],[-1],[0]],
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


class DamageCounter:


    def __init__(self,entity):

        self.entity = entity
        self.posx = 0
        self.posy = 0
        self.base_hp = self.entity.hp
        self.damage = 0
        self.live_time = 60
        self.alive = True

    def update(self):

        if self.damage < self.base_hp - self.entity.hp and self.live_time > 0:
            self.damage = self.base_hp - self.entity.hp
            self.live_time = max(30,self.live_time)

        self.live_time -= 1

        if self.live_time > 0:
            self.posx = self.entity.posx - (2 + 2*len(str(self.damage)))
            self.posy = self.entity.posy - 12
        elif self.live_time > -15:
            self.posy -= 1
        else:
            self.alive = False

    def draw(self):

        pyxel.text(self.posx,self.posy,f"-{self.damage}",15)



def angle_from_vector(posx,posy,endx,endy):

    vector = [endx - posx, endy - posy]
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
    return angle



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