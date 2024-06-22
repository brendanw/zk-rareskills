# 4) Devise an arithmetic circuit that constrains k to be the maximum of x, y, or z. That is, k should be equal to x if
# x is the maximum value, and same for y and z.

# we will assume x, y, and z are 4-bit numbers
def myMax(x, y, z):
    # take advantage of the fact that 01 is half of 10, 010 is half of 100, 0100 is half of 1000
    # (x - y) is positive if x > y. if x > y, thus (x - y) + 16 > 16
    # (x - y) is negative if x < y. if x < y, thus (x - y) + 16 < 16
    u = (x - y) + 16
    # if u is greater than 16, x > y
    # if u is less than 16, x < y
    # MSB is 1 if u >= 16. MSB is 0 if u < 16
    v = u >> 4
    # when v=1 (u >= 16 eg x >= y), assign max as X
    # when v=0 (u < 16 eg x < y), assign max as y
    maxOfXY = x * v + y * (1 - v)

    m = (maxOfXY - z) + 16
    n = m >> 4
    maxOfXYZ = maxOfXY * n + z * (1 - n)
    # print(f'maxOfXYZ({x},{y},{z}) = {maxOfXYZ}')
    return maxOfXYZ

assert(myMax(1,2,3) == 3)
assert(myMax(15, 4, 12) == 15)
assert(myMax(5, 10, 6) == 10)

# generalize for higher number where n is number of bits for inputs x,y,z
def highMax(n, x, y, z):
    assert(n < 256)
    increment = 2**n
    u = (x - y) + increment
    v = u >> n
    maxOfXY = x * v + y * (1 - v)

    m = (maxOfXY - z) + increment
    n = m >> n
    maxOfXYZ = maxOfXY * n + z * (1 - n)
    print(f'maxOfXYZ: {maxOfXYZ}')
    return maxOfXYZ


def highLevelMax(x, y, z):
    xLen = len(bin(x)) - 2
    yLen = len(bin(y)) - 2
    zLen = len(bin(z)) - 2
    binMax = max(xLen, yLen, zLen)
    return highMax(binMax, x, y, z)

highLevelMax(65, 32, 8)
highLevelMax(7, 70, 42)
highLevelMax(42, 42, 70)