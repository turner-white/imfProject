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


def circlePack2D(tol, r_tot, r_min, r_max, density):
    totalArea = np.pi * r_tot ** 2
    filledArea = 0

    circles = []
    radii = []
    xlist = []
    ylist = []

    # We include this modification because otherwise our algorithm would run for far too long and perform too many
    # computations. Reducing the filled area also models the centered density distribution for these two parameters
    if density == "normal" or density == "Normal":
        totalArea = 0.7*totalArea
    if density == "cauchy" or density == "Cauchy":
        totalArea = 0.6*totalArea

    # iterate until the area is filled up to our tolerance percentage
    while filledArea / totalArea <= tol:
        validLocation = True
        # print(filledArea / totalArea)
        # generate a new circle with a random radius between R_min and R_max
        # choose a random x such that it falls within the boundary circle

        # When the density of gas in the bounding circle is uniform we can use np.random.rand
        if density == "uniform" or density == "Uniform":
            randomX = np.random.rand()
            randomY = np.random.rand()
        # To model a normal distribution we use np.random.normal and limit values exceeding 0 or 1
        elif density == "normal" or density == "Normal":
            randomX = np.random.normal(0.5, 0.1)
            randomY = np.random.normal(0.5, 0.1)
            randomX = 1 if randomX > 1 else randomX
            randomX = 0 if randomX < 0 else randomX
            randomY = 1 if randomY > 1 else randomY
            randomY = 0 if randomY < 0 else randomY
        # Since the cauchy distribution contains values far outside of 0 and 1, we divide by 10 to offset this, but
        # generally we did not have much success in creating usable results with a cauchy distribution and it was more
        # for fun than anything else
        elif density == "cauchy" or density == "Cauchy":
            randomX = np.random.standard_cauchy(1)/10
            randomY = np.random.standard_cauchy(1)/10
            randomX = 1 if randomX > 1 else randomX
            randomX = 0 if randomX < 0 else randomX
            randomY = 1 if randomY > 1 else randomY
            randomY = 0 if randomY < 0 else randomY
        else:
            randomX = np.random.rand()
            randomY = np.random.rand()
        # We cast the random x onto the range of x values that lie within the bounding circle.
        x = randomX * 2 * r_tot

        # now we generate a y value over the range of the vertical chord passing through our random x value
        chordLength = 2 * (r_tot ** 2 - (np.abs(r_tot - x)) ** 2) ** 0.5
        y = (randomY * chordLength) + (0.5 * (2 * r_tot - chordLength))

        # The next step is to bound the maximum value for the radius of our circle, and the absolute largest possible
        # value for this is the distance from the center of the circle to the outside edge of the bounding circle
        edgeDist = r_tot - (((x - r_tot) ** 2 + (y - r_tot) ** 2) ** 0.5)
        # This continues the loop if we have chosen an invalid x,y combination that puts us too close to the edge to
        # make a valid circle.
        if edgeDist < r_min:
            continue
        # If the distance to the outer edge is greater than r_max, we lower the max bound
        tempMaxR = r_max if r_max < edgeDist else edgeDist

        # Here we iterate through ever circle in the list so far to further limit the maximum radius.
        for circle in circles:
            dist = ((circle.x - x) ** 2 + (circle.y - y) ** 2) ** 0.5 - circle.r
            # This condition takes care of points that lie within the bounds of pre-existing circles
            if dist <= r_min:
                validLocation = False
                break
            # If we have found a circle that limits the max radius more than our temporary value we overwrite it
            if dist < tempMaxR:
                tempMaxR = dist

        if validLocation:
            # now we randomly choose a radius value between r_min and maxDist
            randomR = np.random.rand()
            r = randomR * (tempMaxR - r_min) + r_min
            circle = Circle(r, x, y)
            circles.append(circle)
            filledArea += circle.area()
            xlist.append(x)
            ylist.append(y)
            radii.append(r)

    return radii, xlist, ylist


def main():
    # Here we initialize parameters and collect user input
    tol = 0.73
    temp = input("Choose a gas cloud temperature (low,med,high): ")  # approximate temperature ranges for Jean's mass
    density = input("Choose a density profile (uniform, normal, cauchy): ")  # density distributions for alternate model

    r_tot = 500  # We set a global bounding circle of 500 solar units

    # These temperature conditions model the influence of temperature on Jean's mass and star formation
    if temp == "low" or temp == "Low":
        r_min = 1
        r_max = 40
    elif temp == "med" or temp == "Med":
        r_min = 2
        r_max = 60
    elif temp == "high" or temp == "High":
        r_min = 5
        r_max = 100
    else:
        r_min = 1
        r_max = 50
    # here we call our algorithm
    r, x, y = circlePack2D(tol, r_tot, r_min, r_max, density)

    # graphs log/log plot and finds alpha value
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

    # Calculate dN for Salpeter's formula
    N_diff = []
    for i in range(1, len(N)):
        N_diff.append(N[i-1]-N[i])
    N_diff.append(0)
    N_diff = abs(np.array(N_diff))

    # In order to take the logarithm of our data we found that we needed to eliminate bins where 0 stars with the given
    # mass were found.
    noZeroMask = N_diff > 0
    mNoZero = m[noZeroMask]
    NNoZero = N_diff[noZeroMask]
    lessOnes = np.where(NNoZero == 1)[0][5]
    log_m = np.log(mNoZero[0:lessOnes])
    log_N = np.log(NNoZero[0:lessOnes])

    # Plotting code
    fig, ax = plt.subplots()
    plt.scatter(log_m, log_N)

    p = np.poly1d(np.polyfit(log_m, log_N, 1))
    alpha = p.coefficients[0]
    print("Alpha = ", alpha)
    plt.plot(log_m, p(log_m))
    plt.title("Linear fit for IMF alpha parameter for " + temp + " temp & " + density + " density")

    textstr = "Alpha = " + str(np.round(alpha, 2))
    ax.text(0.75, 0.95, textstr, transform=ax.transAxes, fontsize=12, verticalalignment='top')
    plt.xlabel("log m")
    plt.ylabel("log (dN/dm)")
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
    plt.title("Circle packing for " + temp + " temp & " + density + " density")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()


# This method was mainly used to run repeated trials for higher intensity statistical analysis of the alpha value and \
# contains all the same computations without the added plot code
def getAlpha(fillingFactor):
    tol = fillingFactor

    r_tot = 400
    r_max = 50
    r_min = 2

    r, x, y = circlePack2D(tol, r_tot, r_min, r_max, "uniform")

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

    p = np.poly1d(np.polyfit(log_m, log_N, 1))
    alpha = p.coefficients[0]
    return -1*alpha

# This section of the code is an extremely intense computation for averaging alpha values over numerous trials. We
# modified the code and parameters to get the most accurate value for alpha, and in its current state this code takes
# upwards of 20 minutes to produce one graph.
# alphas = []
# tols = np.arange(0.3, 0.756, 0.025)
# for i in tols:
#     print("starting i step: " + str(i))
#     tempAlphas = []
#     if i < 0.525:
#         for j in range(1, 10):
#             tempAlphas.append(getAlpha(i))
#         alphas.append(np.average(np.array(tempAlphas)))
#     elif 0.725 > i > 0.5:
#         for j in range(0, 2):
#             tempAlphas.append(getAlpha(i))
#         alphas.append(np.average(np.array(tempAlphas)))
#     else:
#         tempAlphas.append(getAlpha(i))
#         alphas.append(np.array(tempAlphas))
# plt.scatter(tols, alphas)
# plt.show()
# print(alphas)


main()
