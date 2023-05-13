import pyxel
import math

class Cube:

    def __init__(self,radius,color) -> None:

        pyxel.init(128,128,"polylol")

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
        self.radius = radius*2
        self.color = color

        self.x = 64
        self.y = 64
        
        pyxel.run(self.update,self.draw)

    def update(self):

        self.x += (pyxel.btn(pyxel.KEY_RIGHT) - pyxel.btn(pyxel.KEY_LEFT))*3
        self.y += (pyxel.btn(pyxel.KEY_UP) - pyxel.btn(pyxel.KEY_DOWN))*3

        if pyxel.btn(pyxel.KEY_S):
            self.anglex += 5
        if pyxel.btn(pyxel.KEY_Z):
            self.anglex += -5
        if pyxel.btn(pyxel.KEY_D):
            self.angley += 5
        if pyxel.btn(pyxel.KEY_Q):
            self.angley += -5
        if pyxel.btn(pyxel.KEY_E):
            self.anglez += 5
        if pyxel.btn(pyxel.KEY_A):
            self.anglez += -5

        if self.anglex >= 360:
            self.anglex += -360 
        if self.angley >= 360:
            self.angley = -360
        if self.anglez >= 360:
            self.anglez = -360

    
    def draw(self):
        pyxel.cls(0)

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

            figure2d += [[int(projected_2d[0][0] * self.radius) + self.x,int(projected_2d[1][0] * self.radius) + self.y]]

        for k in range(4):
            pyxel.line(*figure2d[k], *figure2d[(k+1)%4],self.color)
            pyxel.line(*figure2d[k + 4], *figure2d[(k+1)%4 +4],self.color)
            pyxel.line(*figure2d[k], *figure2d[k + 4],self.color)


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
        print("columns of the first matrix must be equal to the rows of the second matrix")
        return None

Cube(25,1)

