import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches


class Circle:
    def __init__(self, r: float, x: float, y: float):
        self.r = r
        self.x = x
        self.y = y

    def area(self):
        return np.pi * (self.r ** 2)


def circlePack2D(tol, r_tot, r_min, r_max):
    totalArea = np.pi * r_tot ** 2
    filledArea = 0
    circles = []
    radii = []
    xlist = []
    ylist = []
    # iterate until the area is filled up to our tolerance percentage
    while filledArea / totalArea <= tol:
        # generate a new circle with a random radius between R_min and R_max
        # choose a random x such that it falls within the boundary circle
        uniformRandomX = np.random.rand()
        x = uniformRandomX * 2 * r_tot
        xlist.append(x)
        # now generate a y value over the range of the vertical chord passing through our random x value
        uniformRandomY = np.random.rand()
        chordLength = 2 * (r_tot ** 2 - (np.abs(r_tot - x)) ** 2) ** 0.5
        y = (uniformRandomY * chordLength) + (0.5 * (2 * r_tot - chordLength))
        ylist.append(y)


        edgeDist = r_tot - (((r_tot-x) ** 2 + (r_tot-y) ** 2) ** 0.5)
        print(str(edgeDist) + " edge")
        tempMaxR = r_max if r_max < edgeDist else edgeDist

        for circle in circles:
            dist = ((circle.x - x)**2 + (circle.y - y)**2)**0.5
            if dist < circle.r:
                continue
            #print(str(dist) + " dist")
            if dist < tempMaxR and dist > r_min:
                tempMaxR = dist
        # now we randomly choose a radius value between r_min and maxDist
        uniformRandomR = np.random.rand()
        r = uniformRandomR * (tempMaxR - r_min) + r_min
        print(r)
        circle = Circle(r, x, y)
        circles.append(circle)
        filledArea += circle.area()
        radii.append(r)

    return radii, xlist, ylist


def main():
    r, x, y = circlePack2D(0.99, 100, 1, 25)
    plt.figure(0)
    plt.hist(r)
    plt.show()
    plt.figure(1)
    for i in range(len(r)):
        c = patches.Circle((x[i], y[i]), radius=r[i])
        plt.gca().add_artist(c)
    plt.xlim([0,200])
    plt.ylim([0,200])
    plt.axis("equal")
    plt.show()

main()

