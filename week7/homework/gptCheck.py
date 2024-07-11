import numpy as np
import galois

# Define the Galois Field GF(79)
GF = galois.GF(79)

# Define the matrices L, R, and O
L = np.array([[0, 0, 3, 0, 0, 0],
              [0, 0, 0, 0, 1, 0],
              [0, 0, 1, 0, 0, 0]])

R = np.array([[0, 0, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 5, 0, 0]])

O = np.array([[0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 1],
              [76, 1, 1, 2, 0, 78]])

# Convert matrices to Galois Field elements
L_galois = GF(L)
R_galois = GF(R)
O_galois = GF(O)

# Define x and y in the Galois Field
x = GF(21)
y = GF(21)

# Compute intermediate values
v1 = 3 * x * x
v2 = v1 * y

# Compute the output
out = 3 * x * x * y + 5 * x * y + GF(78)*x + GF(79 - 2) * y + GF(3)

# Construct the witness vector
w = GF([1, out, x, y, v1, v2])

# Print intermediate values for debugging
print("x:", x)
print("y:", y)
print("v1:", v1)
print("v2:", v2)
print("out:", out)
print("witness vector w:", w)

# Verify the constraint satisfaction step-by-step
Lw = np.matmul(L_galois, w)
Rw = np.matmul(R_galois, w)
Ow = np.matmul(O_galois, w)

print("Lw:", Lw)
print("Rw:", Rw)
print("Ow:", Ow)
print("Lw * Rw:", Lw * Rw)

assert all(Lw * Rw == Ow), "Constraints are not satisfied"
print("The constraints are satisfied.")