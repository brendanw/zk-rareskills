import numpy as np

# Create a graph with 3 nodes and 3 edges and write constraints for a 3-coloring. Convert the 3-coloring to a
# rank 1 constraint system.

# let our nodes be x, y, z, with edges xy, xz, and yz
# let red=1, green=2, blue=3
# an edge is only valid if the product of the two nodes is 2, 3, or 6

# our high-level constraints are:
# for each node x, x must be red, green, or blue
# (1-x)*(2-x)*(3-x) === 0
# (1-y)*(2-y)*(3-y) === 0
# (1-z)*(2-z)*(3-z) === 0
# the expanded forms will be
# -x^3 + 6x^2 - 11x + 6 === 0
# -y^3 + 6y^2 - 11y + 6 === 0
# -z^3 + 6x^2 - 11z + 6 === 0
# e = x * x
# r = y * y
# t = z * z

# -ex + 6e - 11x + 6 === 0
# -ry + 6r - 11y + 6 === 0
# -tz + 6t - 11z + 6 === 0
# final constraint set for these high-level constraints will be
# x * x = e
# y * y = r
# z * z = t
# ex = 6e - 11x + 6
# ry = 6r - 11y + 6
# tz = 6t - 11z + 6

# no two neighboring nodes should have the same color
# (2 - xy) * (3 - xy) * (6 - xy) === 0
# (2 - xz) * (3 - xz) * (6 - xz) === 0
# (2 - yz) * (3 - yz) * (6 - yz) === 0
# the expanded form of the first equation is
# -(xy)^3 + 11(xy)^2 - 36xy + 36 === 0

# the second generic constraint can be reduced to RC1S as follows
# v = xy
# w = v*v
# -v^3 + 11v^2 - 36v + 36 === 0
# -vw + 11w - 36v + 36 === 0
# vw = 11w -36v + 36

# final constraint set for second high-level constraints will be
# xy = v
# v*v = w
# vw = 11w -36v + 36
#
# xz = b
# b*b = n
# bn = 11n -36b + 36
#
# yz = a
# a*a = s
# as = 11s - 36a + 36

# final overall constraint set will be
# validate that x is {1,2,3}, y is {1,2,3}, z is {1,2,3}
# x * x = e
# y * y = r
# z * z = t
# ex = 6e - 11x + 6
# rx = 6r - 11y + 6
# tx = 6t - 11z + 6

# validate that xy is {2,3,6}, yz is {2,3,6}, xz is {2,3,6}
# xy = v
# v*v = w
# vw = 11w -36v + 36
#
# xz = b
# b*b = n
# bn = 11n -36b + 36
#
# yz = a
# a*a = s
# as = 11s - 36a + 36

# validate I did polynomials correct
def isValidThreeColoringPolynomials(x, y, z):
    # witness will be [1,x,y,z,e,r,t,v,w,b,n,a,s]

    # x*x = e
    e = x * x

    # y*y = r
    r = y * y

    # z*z = t
    t = z * z

    # x*y = v
    v = x * y

    # v*v = w
    w = v * v

    # xz = b
    b = x * z

    # b*b = n
    n = b * b

    # y*z = a
    a = y * z

    # a * a = s
    s = a * a

    if e*x != 6*e - 11*x + 6:
        return False

    if r*y != 6*r - 11*y + 6:
        return False

    if t*z != 6*t - 11*z + 6:
        return False

    if v*w != 11*w - 36*v + 36:
        return False

    if b*n != 11*n - 36*b + 36:
        return False

    if a*s != 11*s - 36*a + 36:
        return False

    return True

# let's sanity check our polynomials before converting to matrix form
assert isValidThreeColoringPolynomials(4, 5, 6) == False
assert isValidThreeColoringPolynomials(1,2,3) == True
assert isValidThreeColoringPolynomials(1, 1, 1) == False
assert isValidThreeColoringPolynomials(3, 3, 3) == False
assert isValidThreeColoringPolynomials(2, 2, 2) == False
assert isValidThreeColoringPolynomials(1, 1, 2) == False
assert isValidThreeColoringPolynomials(2, 2, 1) == False
assert isValidThreeColoringPolynomials(2, 1, 2) == False
assert isValidThreeColoringPolynomials(1, 2, 3) == True
assert isValidThreeColoringPolynomials(3, 1, 2) == True
assert isValidThreeColoringPolynomials(3, 2, 1) == True

# ok let's finally do the matrix stuff

def isValidThreeColoring(x, y, z):
    # witness will be [1,x,y,z,e,r,t,v,w,b,n,a,s]

    # x*x = e
    e = x * x

    # y*y = r
    r = y * y

    # z*z = t
    t = z * z

    # x*y = v
    v = x * y

    # v*v = w
    w = v * v

    # xz = b
    b = x * z

    # b*b = n
    n = b * b

    # y*z = a
    a = y * z

    # a * a = s
    s = a * a

    # witness will be [1,x,y,z,e,r,t,v,w,b,n,a,s]
    w = np.array([1,x,y,z,e,r,t,v,w,b,n,a,s])

    A = np.array([
        #1,x,y,z,e,r,t,v,w,b,n,a,s
        [0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,0],
        # validate product
        [0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,0,0,0,0],

        #1,x,y,z,e,r,t,v,w,b,n,a,s
        [0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,1,0,0,0],

        [0,0,1,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,0],
    ])

    B = np.array([
        #1,x,y,z,e,r,t,v,w,b,n,a,s
        [0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,0,0,0,0,0,0,0],
        # validate product
        [0,0,1,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0],

        #1,x,y,z,e,r,t,v,w,b,n,a,s
        [0,0,0,1,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0],

        [0,0,0,1,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1],
    ])

    R = np.array([
        #1,x,y,z,e,r,t,v,w,b,n,a,s
        [0,0,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,0],
        # 1,x, y,z,e,r,t,v,w,b,n,a,s
        [6,-11,0,0,6,0,0,0,0,0,0,0,0],
        [6,0,-11,0,0,6,0,0,0,0,0,0,0],
        [6,0,0,-11,0,0,6,0,0,0,0,0,0],
        # validate product
        #1,x,y,z,e,r,t,v,w,b,n,a,s
        [0,0,0,0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0],
        [36,0,0,0,0,0,0,-36,11,0,0,0,0],

        [0,0,0,0,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0],
        [36,0,0,0,0,0,0,0,0,-36,11,0,0],

        [0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1],
        [36,0,0,0,0,0,0,0,0,0,0,-36,11],
    ])

    # Aw + Bw = Rw
    left = np.dot(A, w) * np.dot(B, w)
    right = np.dot(R, w)

    return np.array_equal(left, right)

assert isValidThreeColoring(4, 5, 6) == False
assert isValidThreeColoring(1,2,3) == True
assert isValidThreeColoring(1, 1, 1) == False
assert isValidThreeColoring(3, 3, 3) == False
assert isValidThreeColoring(2, 2, 2) == False
assert isValidThreeColoring(1, 1, 2) == False
assert isValidThreeColoring(2, 2, 1) == False
assert isValidThreeColoring(2, 1, 2) == False
assert isValidThreeColoring(1, 2, 3) == True
assert isValidThreeColoring(3, 1, 2) == True
assert isValidThreeColoring(3, 2, 1) == True
