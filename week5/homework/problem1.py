# Create an arithmetic circuit that takes signals x₁, x₂, ..., xₙ and is satisfied if at least one signal is 0.

def hasAtLeastOneZero(x1, x2, x3):
    return (x1 * x2 * x3 == 0)

assert(hasAtLeastOneZero(1, 1, 1) == False)
assert(hasAtLeastOneZero(1, 1, 0))
