import numpy as np

def isValidThreeColoring(x,y,z):
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

    C = np.array([
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
    result = np.dot(A, w) * np.dot(B, w) - np.dot(C, w)

    result = np.array(result)
    return np.all(result == 0)

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
