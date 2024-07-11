import numpy as np
from numpy.typing import NDArray
from typing import Any
from scipy.interpolate import lagrange

# Let φ be the transformation of a column vector into a polynomial like we discussed in class (using lagrange
# interpolation over the x values [0, 1, …, n] and the y values being the values in the vector).
#
# Use Python compute:
# \phi(c\cdot\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix}) = c\cdot\phi(\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix})
#
# Test out a few vectors to convince yourself this is true in general.
#
# In English, what is the above equality stating?

def phi(inputArr):
    x = np.array([1,2,3])
    poly = lagrange(x, inputArr)
    return poly

def runTest(vector, scalar):
    preScalarApplication = np.dot(vector, scalar)
    prePoly = phi(preScalarApplication)

    postScalarPoly = phi(vector)
    postPoly = scalar * postScalarPoly
    assert(prePoly(1) == postPoly(1))
    assert(prePoly(2) == postPoly(2))
    assert(prePoly(3) == postPoly(3))

runTest(np.array([1,2,3]), 2)
runTest(np.array([2,5,6]), 27)
runTest(np.array([11,13,17]), 23)
runTest(np.array([17,23,27]), 23)
runTest(np.array([31,37,41]), 23)

print("Test Successful")

# It doesn't matter if we apply a scalar before or after we transform a column vector as a polynomial