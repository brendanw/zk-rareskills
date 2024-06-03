import matplotlib.pyplot as plt
import libnum

def generate_points(mod):
    xs = []
    ys = []

    def y_squared(x):
        return (x ** 3 + 3) % mod

    for x in range(0, mod):
        if libnum.has_sqrtmod_prime_power(y_squared(x), mod, 1):
            square_roots = libnum.sqrtmod_prime_power(y_squared(x), mod, 1)

            # Flatten the list by adding both x for each square root found
            for sr in square_roots:
                ys.append(sr)
                xs.append(x)

    return xs, ys

def double(x, y, a, p):
    lambd = (((3 * x ** 2) % p) * pow(2 * y, -1, p)) % p
    newx = (lambd ** 2 - 2 * x) % p
    newy = (-lambd * newx + lambd * x - y) % p
    return (newx, newy)

def add_points(xq, yq, xp, yp, p, a=0):
    if xq == yq == None:
        return xp, yp
    if xp == yp == None:
        return xq, yq

    assert (xq ** 3 + 3) % p == (yq ** 2) % p, "q not on curve"
    assert (xp ** 3 + 3) % p == (yp ** 2) % p, "p not on curve"

    if xq == xp and yq == yp:
        return double(xq, yq, a, p)
    elif xq == xp:
        return None, None

    lambd = ((yq - yp) * pow((xq - xp), -1, p)) % p
    xr = (lambd ** 2 - xp - xq) % p
    yr = (lambd * (xp - xr) - yp) % p
    return xr, yr


xs, ys = generate_points(11)

# for our purposes, (4, 10) is the generator point G
next_x, next_y = 4, 10
print(1, 4, 10)
points = [(next_x, next_y)]
for i in range(2, 12):
    # repeatedly add G to the next point to generate all the elements
    next_x, next_y = add_points(next_x, next_y, 4, 10, 11)
    # print(i, next_x, next_y)
    points.append((next_x, next_y))


fig, ax1 = plt.subplots(1, 1)
fig.suptitle('y^2 = x^3 + 3 (mod p)')
fig.set_size_inches(6, 6)
ax1.set_xticks(range(0, 11))
ax1.set_yticks(range(0, 11))
plt.grid()
plt.scatter(xs, ys)
for i in range(0, 11):
    print(i, points[i][0], points[i][1])
    plt.annotate(str(i+1), (points[i][0] + 0.1, points[i][1]))
plt.show()



