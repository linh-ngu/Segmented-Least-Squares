import pickle
import sys

dict = pickle.load(open('examples_of_instances', 'rb'))

# does one sample at a time
def loadValues(x):
    global pts, cost, errors
    pts = dict['n_list'][x]
    xcoords = dict['x_list'][x]
    ycoords = dict['y_list'][x]
    cost = dict['C_list'][x]

    # sum of the coords up to n where sumx[n] is the sum from i = 0, 1, ..., n. used to find a and b coefficients
    sumx = [0] * pts
    sumy = [0] * pts
    sumxx = [0] * pts
    sumxy = [0] * pts
    sumyy = [0] * pts

    sumx[0] = xcoords[0]
    sumy[0] = ycoords[0]
    sumxx[0] = xcoords[0] * xcoords[0]
    sumxy[0] = xcoords[0] * ycoords[0]
    sumyy[0] = ycoords[0] * ycoords[0]

    # finding current and adding to all before
    for i in range(1, pts):
        sumx[i] = xcoords[i] + sumx[i - 1]
        sumy[i] = ycoords[i] + sumy[i - 1]
        sumxx[i] = xcoords[i] * xcoords[i] + sumxx[i - 1]
        sumxy[i] = xcoords[i] * ycoords[i] + sumxy[i - 1]
        sumyy[i] = ycoords[i] * ycoords[i] + sumyy[i - 1]

    # 2d array for a, b values of each point to other points
    avals = []
    bvals = []
    errors = []
    for i in range(pts):
        avals.append([0] * pts)
        bvals.append([0] * pts)
        errors.append([0] * pts)

    for j in range(1, pts):
        for i in range(0, j):
            numpts = j - i + 1

            # if only 2 points then line can go through both
            # sums are from j to i inclusive so index is i - 1
            if numpts < 3:
                errors[i][j] = 0
                continue
            if i == 0:
                xsum = sumx[j]
                ysum = sumy[j]
                xxsum = sumxx[j]
                xysum = sumxy[j]
                yysum = sumyy[j]
            else:
                xsum = sumx[j] - sumx[i - 1]
                ysum = sumy[j] - sumy[i - 1]
                xxsum = sumxx[j] - sumxx[i - 1]
                xysum = sumxy[j] - sumxy[i - 1]
                yysum = sumyy[j] - sumyy[i - 1]

            avals[i][j] = ((numpts * xysum) - (xsum * ysum)) / (numpts * xxsum - xsum * xsum)
            bvals[i][j] = (ysum - avals[i][j] * xsum) / numpts

            # have to factor out equation or else math was wrong
            errors[i][j] = yysum - (2 * bvals[i][j] * ysum) + (avals[i][j] * avals[i][j] * xxsum) - (2 * avals[i][j] * xysum) + (2 * avals[i][j] * bvals[i][j] * xsum) + (numpts * bvals[i][j] ** 2)

def optimalSolution():
    # holds optimal solution from i to j. first point is cost only
    opt = [0] * pts
    opt[0] = cost

    # holds where line splits at j. first line starts at 0
    split = [0] * pts
    split[0] = 0

    # loop through every possible segment and decide which segment has the lowest cost and
    # compare it with the lowest cost of previous optimal cost.
    for j in range(1, pts):
        currmin = sys.maxsize
        for i in range(0, j):
            if i == 0:
                currcost = errors[i][j] + cost
            else:
                currcost = errors[i][j] + cost + opt[i - 1]

            if currcost < currmin:
                currmin = currcost
                currsplit = i
            split[j] = currsplit
            opt[j] = currmin

    # finding where new lines start and end
    temp = []
    i = pts - 1
    j = split[pts - 1]

    while i > 0:
        temp.append(i)
        temp.append(j)
        i = j - 1
        j = split[i]

    turnpts = []
    for k in range(0, len(temp), 2):
        turnpts.append(temp[k])

    return opt[pts - 1], turnpts[::-1]

def main():
    klist = []
    lastpoints = []
    optlist = []
    my_solutions = {'k_list': klist, 'last_points_list': lastpoints, 'OPT_list': optlist}

    for instance in range(len(dict['C_list'])):
        loadValues(instance)
        optimum = optimalSolution()
        my_solutions['k_list'].append(len(optimum[1]))
        my_solutions['last_points_list'].append(optimum[1])
        my_solutions['OPT_list'].append(optimum[0])

    print(my_solutions)

main()