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
        validLocation=True
        print(filledArea/totalArea)
        # generate a new circle with a random radius between R_min and R_max
        # choose a random x such that it falls within the boundary circle
        uniformRandomX = np.random.rand()
        x = uniformRandomX * 2 * r_tot

        # now generate a y value over the range of the vertical chord passing through our random x value
        uniformRandomY = np.random.rand()
        chordLength = 2 * (r_tot ** 2 - (np.abs(r_tot - x)) ** 2) ** 0.5
        y = (uniformRandomY * chordLength) + (0.5 * (2 * r_tot - chordLength))



        edgeDist = r_tot - (((x-r_tot) ** 2 + (y-r_tot) ** 2) ** 0.5)
        if edgeDist < r_min:
            continue
        # print(str(edgeDist) + " edge")
        tempMaxR = r_max if r_max < edgeDist else edgeDist


        for circle in circles:
            dist = ((circle.x - x)**2 + (circle.y - y)**2)**0.5 - circle.r
            if dist <= r_min:
                validLocation = False
                break

            if dist < tempMaxR and dist > r_min:
                tempMaxR = dist
        # now we randomly choose a radius value between r_min and maxDist
        if validLocation:
            uniformRandomR = np.random.rand()
            r = uniformRandomR * (tempMaxR - r_min) + r_min
            # print(r)
            circle = Circle(r, x, y)
            circles.append(circle)
            filledArea += circle.area()
            xlist.append(x)
            ylist.append(y)
            radii.append(r)

    return radii, xlist, ylist


def main():
    tol = 0.6
    r_tot = 100
    r_max = 30
    r_min = 2
    r, x, y = circlePack2D(tol, r_tot, r_min, r_max)
    plt.figure(0)
    plt.hist(r)
    plt.show()
    plt.figure(1)
    plt.xlim(r_tot*2+r_tot*0.5)
    plt.ylim(r_tot*2+r_tot*0.5)
    circle = plt.Circle((r_tot, r_tot), r_tot, color='blue', fill=False)
    plt.gca().add_artist(circle)
    for i in range(len(r)):
        c = patches.Circle((x[i], y[i]), r[i], fill=False)
        plt.gca().add_artist(c)
    plt.axis("equal")
    plt.show()

main()

