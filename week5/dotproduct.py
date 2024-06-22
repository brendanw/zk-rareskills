import numpy

witness = [1, 18, 3, 2, 9]

# goal is to create a system of equations of the form
# Cw = Aw * Bw where w is the witness vector. And A, B, and C are matrices

# what are the dimensions of the matrices that make sense for the dot product?
numpyWitness = numpy.array(
    [
        [1, 1],
        [1, 1]
    ]
)

# number of rows in the matrix will correspond to the number of constraints in the circuit
# for out = x * y
# we have just one constraint

# for out = x * y * z * u
# v1 = x * y
# v2 = y * z
# out = v1 * v2
# we have three constraints and thus we will have 3 rows