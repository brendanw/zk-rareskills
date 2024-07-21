from py_ecc.bn128 import G1, G2, multiply, add, neg, eq, pairing

# let's figure out how to prove the below in zero knowledge
# 39 = x^3 - 4x^2 + 3x - 1

# the non zk way to prove is to just give the verifier x=5 and then the verifier can plug x in to see the equation holds
# true

# to do this in zk we would typically have the verifier encrypt x = 5 such that we have 5G, BUT we cannot calculate
# (5G)^3. So how do we prove in zk?

# one way is we can also have the prover generate G, G^2, G^3 and provide these values to the verifier
# the verifier can validate that G^2 is derived from G. And that G^3 is derived from G^2 since each of these individual
# verifications only relies on one pairing.

# prover
solutionX = 5

# must calculate G1 points to provide the verifier
X3 = multiply(G1, pow(solutionX, 3))
X2 = multiply(G1, pow(solutionX, 2))
X1 = multiply(G1, solutionX)

# must calculate G2 points to provide the verifier
x3 = multiply(G2, pow(solutionX, 3))
x2 = multiply(G2, pow(solutionX, 2))
x1 = multiply(G2, solutionX)

# verifier
lhs = multiply(G1, 39)
reduce1 = add(X3, multiply(neg(X2), 4))
reduce2 = add(multiply(X1, 3), neg(G1))
rhs = add(reduce1, reduce2)

# this isn't enough! the verifier should verify that X2 is really the result of X^2 and X3 is really the result of X^3

# let's validate that each G1 point corresponds to G2 point
assert eq(pairing(x1, G1), pairing(G2, X1)), "x1 and X1 do not encrypt the same value"
assert eq(pairing(x2, G1), pairing(G2, X2)), "x2 and X2 do not encrypt the same value"
assert eq(pairing(x3, G1), pairing(G2, X3)), "x3 and X3 do not encrypt the same value"
assert eq(pairing(x1, X1), pairing(x2, G1)), "x2 is not x^2"
assert eq(pairing(x2, X1), pairing(x3, G1)), "x3 is not x^3"
assert eq(lhs, rhs), "lhs != rhs"

# the key thing above is that the prover can generate X3, X2, and X and give those to the verifier to use
# and the verifier can then validate that 39*G1 = X3 - 4*X2 + 3*X - 1
# without knowing what the underlying x value is. they just have encrypted X3, X2, and X values

print("done")