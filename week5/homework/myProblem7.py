# The covering set problem starts with a set S = {1, 2, …, 10} and several well-defined subsets of S, for example:
# {1, 2, 3}, {3, 5, 7, 9}, {8, 10}, {5, 6, 7, 8}, {2, 4, 6, 8},
# and asks if we can take at most k subsets of S such that their union is S.
# In the example problem above, the answer for k = 4 is true because we can use
# {1, 2, 3}, {3, 5, 7, 9}, {8, 10}, {2, 4, 6, 8}.
#
# Note that for each problems, the subsets we can work with are determined at the beginning. We cannot construct the
# subsets ourselves. If we had been given the subsets {1,2,3}, {4,5} {7,8,9,10} then there would be no solution
# because the number 6 is not in the subsets.
#
# On the other hand, if we had been given S = {1,2,3,4,5} and the subsets {1}, {1,2}, {3, 4}, {1, 4, 5} and asked can
# it be covered with k = 2 subsets, then there would be no solution. However, if k = 3 then a valid solution would be
# {1, 2}, {3, 4}, {1, 4, 5}.
#
# Our goal is to prove for a given set S and a defined list of subsets of S, if we can pick a set of subsets such that
# their union is S. Specifically, the question is if we can do it with k or fewer subsets. We wish to prove we know
# which k (or fewer) subsets to use by encoding the problem as an arithmetic circuit.

def validate(S, subsets, k):
    # probably need to use prime number trick

    return True

# gonna assume we have already mapped each number in S to a corresponding prime
def validateSolution(S, A, B, k):
    # the grand product of all numbers in A=[2,3,5] and B=[5,7] should be able to be expressed in terms of
    # (S[0])^n * (S[1])^m * (S[2])^o * (S[3])^p where  k >= n,m,s,p >= 1

    lefthand = S[0] * S[1] * S[2] * S[3]
    righthand = A[0] * A[1] * A[2] * B[0] * B[1]
    # righthand mod lefthand === 0 if all elements are prime



assert(validateSolution([2,3,5,7], [2,3,5], [5,7], 2) == True)

