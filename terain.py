
import math
import random
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
class HillGrid:

    def __init__(self,KRADIUS =(1.0/5.0),ITER=200,SIZE=40):
        self.KRADIUS = KRADIUS
        self.ITER = ITER
        self.SIZE = SIZE

        self.grid = [[0 for x in range(self.SIZE)] for y in range(self.SIZE)]

        self.MAX = self.SIZE * self.KRADIUS
        for i in range(self.ITER):
            self.step()

    def dump(self):
        for ele in self.grid:
            s = ''
            for alo in ele:
                s += '%s ' % str(alo)

            plt.imshow(self.grid,interpolation='nearest')
            plt.show()

    def __getitem__(self,n):
        return self.grid[n]

    def step(self):
        point = [random.randint(0,self.SIZE-1),random.randint(0,self.SIZE-1)]
        radius = random.uniform(0,self.MAX)

        x2 = point[0]
        y2 = point[1]    

        for x in range(self.SIZE):
            for y in range(self.SIZE):

                z = (radius**2) - ( math.pow(x2-x,2) + math.pow(y2-y,2) )
                if z >= 0:
                    self.grid[x][y] += int(z)


if __name__ == '__main__':
    h = HillGrid(ITER=50,SIZE = 100)
    h.dump()