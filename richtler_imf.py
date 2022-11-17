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

    def mass(self):
        return


def circlePack2D(tol, r_tot, r_min, r_max):
    totalArea = np.pi * r_tot ** 2
    filledArea = 0

    circles = []
    radii = []
    xlist = []
    ylist = []
    # iterate until the area is filled up to our tolerance percentage
    while filledArea / totalArea <= tol:
        validLocation = True
        print(filledArea / totalArea)
        # generate a new circle with a random radius between R_min and R_max
        # choose a random x such that it falls within the boundary circle
        uniformRandomX = np.random.rand()
        x = uniformRandomX * 2 * r_tot
        #x = np.random.normal(100, 20)

        # now generate a y value over the range of the vertical chord passing through our random x value
        uniformRandomY = np.random.rand()
        #normalRandomY = np.random.normal(-0.2,0.2)
        chordLength = 2 * (r_tot ** 2 - (np.abs(r_tot - x)) ** 2) ** 0.5
        y = (uniformRandomY * chordLength) + (0.5 * (2 * r_tot - chordLength))

        edgeDist = r_tot - (((x - r_tot) ** 2 + (y - r_tot) ** 2) ** 0.5)
        if edgeDist < r_min:
            continue
        # print(str(edgeDist) + " edge")
        tempMaxR = r_max if r_max < edgeDist else edgeDist

        for circle in circles:
            dist = ((circle.x - x) ** 2 + (circle.y - y) ** 2) ** 0.5 - circle.r
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
    tol = 0.72
    temp = 20 # temperature in Kelvin
    rho = 1408

    r_tot = 200
    r_max = 50
    r_min = 1

    r, x, y = circlePack2D(tol, r_tot, r_min, r_max)


    # graphs log/log plot and finds alpha value
    # Delta m
    m = np.arange(r_min**2, r_max**2, 1)
    dm = m[1]-m[0]
    N = []
    for mass in m:
        Ncount = 0
        for j in range(len(r)):
            if mass <= r[j]**2 < mass + dm:
                Ncount += 1
        N.append(Ncount)
    N = np.array(N)

    N_diff = []
    for i in range(1, len(N)):
        N_diff.append(N[i-1]-N[i])
    N_diff.append(0)
    N_diff = abs(np.array(N_diff))

    noZeroMask = N_diff > 0
    mNoZero = m[noZeroMask]
    NNoZero = N_diff[noZeroMask]
    lessOnes = np.where(NNoZero == 1)[0][5]

    log_m = np.log(mNoZero[0:lessOnes])
    log_N = np.log(NNoZero[0:lessOnes])
    # N_plot = N_diff[noZeroMask]
    # m_plot = m[noZeroMask]

    plt.figure(0)
    plt.scatter(log_m, log_N)

    p = np.poly1d(np.polyfit(log_m, log_N, 1))
    alpha = p.coefficients[0]
    y_int = p.coefficients[1]
    print("Alpha = ", alpha, "\nIntercept = ", y_int)
    plt.plot(log_m, p(log_m))
    plt.show()

    plt.figure(1)
    plt.xlim(r_tot * 2 + r_tot * 0.5)
    plt.ylim(r_tot * 2 + r_tot * 0.5)
    circle = plt.Circle((r_tot, r_tot), r_tot, color='blue', fill=False)
    plt.gca().add_artist(circle)
    for i in range(len(r)):
        c = patches.Circle((x[i], y[i]), r[i], fill=False)
        plt.gca().add_artist(c)
    plt.axis("equal")
    plt.show()


# def getAlpha(fillingFactor):
#     tol = fillingFactor
#
#     r_tot = 200
#     r_max = 50
#     r_min = 1
#
#     r, x, y = circlePack2D(tol, r_tot, r_min, r_max)
#
#     m = np.linspace(r_min**2, r_max**2, 20)
#     dm = m[1]-m[0]
#     N = []
#     for mass in m:
#         Ncount = 0
#         for j in range(len(r)):
#             if mass <= r[j]**2 < mass + dm:
#                 Ncount += 1
#         N.append(Ncount)
#     N = np.array(N)
#
#     N_diff = []
#     for i in range(1, len(N)):
#         N_diff.append(N[i-1]-N[i])
#     N_diff.append(0)
#     N_diff = abs(np.array(N_diff))
#
#     noZeroMask = N_diff > 0
#     N_plot = N_diff[noZeroMask]
#     m_plot = m[noZeroMask]
#
#     log_m = np.log(m_plot)
#     log_N = np.log(N_plot)
#
#     p = np.poly1d(np.polyfit(log_m, log_N, 1))
#     alpha = p.coefficients[0]
#     return alpha

# alphas = []
# for i in range(4,8):
#     tempAlphas = []
#     for j in range(1,100):
#         tempAlphas.append(getAlpha(i/10))
#     alphas.append(np.average(np.array(tempAlphas)))
# print(alphas)


main()
