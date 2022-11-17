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


def circlePack2D(tol, r_tot, r_min, r_max, density, temp):
    totalArea = np.pi * r_tot ** 2
    filledArea = 0

    circles = []
    radii = []
    xlist = []
    ylist = []

    if density == "normal" or density == "Normal":
        totalArea = 0.7*totalArea
    if density == "cauchy" or density == "Cauchy":
        totalArea = 0.6*totalArea
    # iterate until the area is filled up to our tolerance percentage
    while filledArea / totalArea <= tol:
        validLocation = True
        print(filledArea / totalArea)
        # generate a new circle with a random radius between R_min and R_max
        # choose a random x such that it falls within the boundary circle

        if density == "uniform" or density == "Uniform":
            randomX = np.random.rand()
            randomY = np.random.rand()
        elif density == "normal" or density == "Normal":
            randomX = np.random.normal(0.5, 0.1)
            randomY = np.random.normal(0.5, 0.1)
            randomX = 1 if randomX > 1 else randomX
            randomX = 0 if randomX < 0 else randomX
            randomY = 1 if randomY > 1 else randomY
            randomY = 0 if randomY < 0 else randomY
        elif density == "cauchy" or density == "Cauchy":
            randomX = np.random.standard_cauchy(1)/10
            randomY = np.random.standard_cauchy(1)/10
            randomX = 1 if randomX > 1 else randomX
            randomX = 0 if randomX < 0 else randomX
            randomY = 1 if randomY > 1 else randomY
            randomY = 0 if randomY < 0 else randomY

        x = randomX * 2 * r_tot

        # now generate a y value over the range of the vertical chord passing through our random x value
        #uniformRandomY = np.random.rand()
        #normalRandomY = np.random.normal(-0.2,0.2)
        chordLength = 2 * (r_tot ** 2 - (np.abs(r_tot - x)) ** 2) ** 0.5
        y = (randomY * chordLength) + (0.5 * (2 * r_tot - chordLength))

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
            if temp == "low" or temp == "Low":
                randomR = np.random.normal(0.3,0.2)
                randomR = 1 if randomR > 1 else randomR
                randomR = 0 if randomR < 0 else randomR
            elif temp == "med" or temp == "Med":
                randomR = np.random.rand()
            elif temp == "high" or temp == "High":
                randomR = np.random.normal(0.7,0.2)
                randomR = 1 if randomR > 1 else randomR
                randomR = 0 if randomR < 0 else randomR

            r = randomR * (tempMaxR - r_min) + r_min
            # print(r)
            circle = Circle(r, x, y)
            circles.append(circle)
            filledArea += circle.area()
            xlist.append(x)
            ylist.append(y)
            radii.append(r)

    return radii, xlist, ylist

def main():
    tol = 0.7
    temp = input("Choose a gas cloud temperature (low,med,high): ") # temperature in Kelvin
    density = input("Choose a density profile (uniform, normal, cauchy): ")

    r_tot = 500

    if temp == "low" or temp == "Low":
        r_min = 1
        r_max = 40
    elif temp == "med" or temp == "Med":
        r_min = 2
        r_max = 60
    elif temp == "high" or temp == "High":
        r_min = 5
        r_max = 100

    r, x, y = circlePack2D(tol, r_tot, r_min, r_max, density, temp)


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


def getAlpha(fillingFactor):
    tol = fillingFactor

    temp = 20  # temperature in Kelvin
    rho = 1408

    r_tot = 200
    r_max = 50
    r_min = 1

    r, x, y = circlePack2D(tol, r_tot, r_min, r_max)

    # graphs log/log plot and finds alpha value
    # Delta m
    m = np.arange(r_min ** 2, r_max ** 2, 1)
    dm = m[1] - m[0]
    N = []
    for mass in m:
        Ncount = 0
        for j in range(len(r)):
            if mass <= r[j] ** 2 < mass + dm:
                Ncount += 1
        N.append(Ncount)
    N = np.array(N)

    N_diff = []
    for i in range(1, len(N)):
        N_diff.append(N[i - 1] - N[i])
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


    p = np.poly1d(np.polyfit(log_m, log_N, 1))
    alpha = p.coefficients[0]
    return -1*alpha

# alphas = []
# tols = [0.4, 0.5, 0.6, 0.65, 0.7, 0.75]
# for i in tols:
#     tempAlphas = []
#     for j in range(1,5):
#         tempAlphas.append(getAlpha(i))
#     alphas.append(np.average(np.array(tempAlphas)))
# plt.scatter(tols, alphas)
# plt.show()
# print(alphas)



main()
