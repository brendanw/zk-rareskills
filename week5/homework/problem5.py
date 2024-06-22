# Create an arithmetic circuit that takes signals x₁, x₂, ..., xₙ, constrains them to be binary, and outputs 1 if at
# least one of the signals is 1. Hint: this is tricker than it looks. Consider combining what you learned in the first
# two problems and using the NOT gate.

def returnOneWhenAtLeastOneOne(x1, x2, x3, x4):
    isBin1 = x1 * (x1 - 1) == 0
    isBin2 = x2 * (x2 - 1) == 0
    isBin3 = x3 * (x3 - 1) == 0
    isBin4 = x4 * (x4 - 1) == 0
    atLeastOneOne = (x1 - 1) * (x2 - 1) * (x3 - 1) * (x4 - 1) == 0
    return isBin1 and isBin2 and isBin3 and isBin4 and atLeastOneOne

assert(returnOneWhenAtLeastOneOne(0, 0, 0, 0) == False)
assert(returnOneWhenAtLeastOneOne(0, 0, 0, 1) == True)
assert(returnOneWhenAtLeastOneOne(1, 0, 0, 0) == True)
assert(returnOneWhenAtLeastOneOne(1, 1, 1, 1) == True)
