# Create an arithmetic circuit that takes signals x₁, x₂, ..., xₙ and is satisified if all are 1.

def allValuesAreOne(x1, x2, x3, x4):
    a = x1 * x2 * x3 * x4 == 1
    b = x1 + x2 + x3 + x4 == 4
    return a and b

assert(allValuesAreOne(1, 1, 2, 1) == False)
assert(allValuesAreOne(1, 1, 1, 1))
assert(allValuesAreOne(-1, -1, -1, -1) == False)