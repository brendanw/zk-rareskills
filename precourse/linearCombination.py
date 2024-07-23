import numpy as np

def linearCombination(A, B, a, b):
    # Todo, add your code
    vectorA = np.array(A)
    vectorB = np.array(B)
    return a * vectorA + b * vectorB

vector1 = np.array([1,2])
vector2 = np.array([5,6])
scalar1 = 3
scalar2 = 10

assert (np.array([53, 66]) == linearCombination(vector1, vector2, scalar1, scalar2)).all()

print('finished')