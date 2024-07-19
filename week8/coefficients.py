import galois

# Example polynomial
fieldOrder = 79
GF = galois.GF(fieldOrder)
U = galois.Poly([62, 47, 33], field=GF)

# Extract coefficients as a vector
coefficients = U.coefficients

# Convert the galois field elements to integers if necessary
coefficients_vector = [int(coeff) for coeff in coefficients]

print(f'Coefficients vector: {coefficients_vector}')