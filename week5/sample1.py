import numpy as np

# problem is out = x * y
# witness is 4223 = 41 * 223 ie [1, 4223, 41, 103]


# witness is [1, out, x, y]

# Cw = Aw dot Bw
C = np.array([[0,1,0,0]])
A = np.array([[0,0,1,0]])
B = np.array([[0,0,0,1]])

w = [1, 4223, 41, 103]
Cw = C.dot(w)
print(Cw)

Aw = A.dot(w)
print(Aw)

Bw = B.dot(w)
print(Bw)

print(Aw * Bw)
print(Cw)


