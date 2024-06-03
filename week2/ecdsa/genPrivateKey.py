import secrets

n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
newPrivKey = secrets.randbelow(n)
print(newPrivKey)
print(hex(newPrivKey))
