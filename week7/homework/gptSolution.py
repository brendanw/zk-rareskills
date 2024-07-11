import numpy as np
from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial

# Define the matrices
A = np.array([[0, 0, 3, 0, 0, 0],
              [0, 0, 0, 0, 1, 0],
              [0, 0, 1, 0, 0, 0]])

B = np.array([[0, 0, 1, 0, 0, 0],
              [0, 0, 0, 1, 0, 0],
              [0, 0, 0, 5, 0, 0]])

C = np.array([[0, 0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0, 1],
              [-3, 1, 1, 2, 0, -1]])

# Pick values for x and y
x = 100
y = 100

# Compute the witness vector
v1 = 3 * x * x
v2 = v1 * y
out = 3 * x * x * y + 5 * x * y - x - 2 * y + 3
w = np.array([1, out, x, y, v1, v2])


# Function to convert matrix columns to polynomials using Lagrange interpolation
def convert_matrix_to_polynomials(matrix, w):
    xs = np.array([1, 2, 3])  # Use points 1, 2, 3 for interpolation
    polynomials = []

    for i in range(matrix.shape[1]):
        col = matrix[:, i]
        poly = lagrange(xs, col)
        poly = Polynomial(poly.coef[::-1])  # Convert to numpy's Polynomial format
        polynomials.append(poly * w[i])

    final_polynomial = sum(polynomials, Polynomial([0]))
    return final_polynomial


# Convert matrices to polynomials
aPolynomial = convert_matrix_to_polynomials(A, w)
bPolynomial = convert_matrix_to_polynomials(B, w)
cPolynomial = convert_matrix_to_polynomials(C, w)

# Multiply polynomials a and b
leftPolynomial = aPolynomial * bPolynomial

# Print the polynomials
print("aPolynomial:", aPolynomial)
print("bPolynomial:", bPolynomial)
print("leftPolynomial:", leftPolynomial)
print("cPolynomial:", cPolynomial)

# Evaluate the polynomials at a given point to verify
evaluation_point = 1
print(f'leftPolynomial({evaluation_point}) = {leftPolynomial(evaluation_point)}')
print(f'cPolynomial({evaluation_point}) = {cPolynomial(evaluation_point)}')

# Check if the polynomials are equivalent by evaluating at multiple points
points = np.linspace(0, 5, num=100)
for point in points:
    assert np.isclose(leftPolynomial(point), cPolynomial(point), atol=1e-8), f"Mismatch at point {point}"

print("The polynomials are equivalent.")
