def isPowerOfTwo(v, v1, v2, v3, v4):
    assertBin = v == 8 * v4 + 4 * v3 + 2 * v2 + v1
    # vX should be the only one of {v1,v2,v3,v4}. all other values should be 0
    return assertBin and (v4 + v3 + v2 + v1 == 1) and v1 * (v1 - 1) == 0 and v2 * (v2 - 1) == 0 and v3 * (v3 - 1) == 0 and v4 * (v4 - 1) == 0


def highLevel(n):
    # Convert n to a 4-bit binary representation
    binary_str = f'{n:04b}'  # Ensures the binary string is 4 bits long
    v1 = int(binary_str[3])
    v2 = int(binary_str[2])
    v3 = int(binary_str[1])
    v4 = int(binary_str[0])
    return isPowerOfTwo(n, v1, v2, v3, v4)

assert(highLevel(1))
assert(highLevel(2))
assert(highLevel(4))
assert(highLevel(8))
assert(highLevel(3) == False)
assert(highLevel(5) == False)
assert(highLevel(6) == False)
assert(highLevel(7) == False)