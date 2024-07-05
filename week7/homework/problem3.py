# Refer to the code here: https://www.rareskills.io/post/r1cs-to-qap
#
# Do the same operation R1CS above but convert it to a QAP over a finite field. Don’t do it by hand, use Python. If you
# pick GF79 like the article does, you’ll need to find the congruent element in the field since some of the scalar
# values for the R1CS above will be negative or be larger than 79.