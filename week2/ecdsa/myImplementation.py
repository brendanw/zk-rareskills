from ecpy.curves import Curve, Point
from Crypto.Hash import keccak
import secrets

cv = Curve.get_curve('secp256k1')

# generator order
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
g = Point(55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424, cv)

# 1) pick a private key
privKey = 7424806760604989754642554183948312713366168026655686637506192756168823274118

# 2) generate the public key using that private key (not the eth address, the public key)
pubKeyPoint = cv.mul_point(privKey, g)
pubKeyX = pubKeyPoint.x
print(f'pubKeyPoint: {pubKeyPoint}')
print(f'pubKeyX: {pubKeyPoint.x}')

# 3) pick message m and hash it to produce h (h can be thought of as a 256-bit number)
msg1 = "hello world"
def hashMsg(msg):
    keccak_hash = keccak.new(digest_bits=256)
    keccak_hash.update(msg.encode('utf-8'))
    hex_hash = keccak_hash.hexdigest()
    h_int = int(hex_hash, 16)
    return h_int

# 4) sign m using your private key and a randomly chosen nonce k. produce (r, s, h, PubKey)
# (r, s, h, PubKey) = sign(h)
# returns (r,s) signature
def sign(msg):
    h = hashMsg(msg)
    k = secrets.randbelow(n) # some random number below n
    R = cv.mul_point(k, g)
    r = R.x
    kInv = pow(k, -1, n)
    product = kInv * (h + r * privKey)
    s = pow(product, 1, n)
    return r, s


(r, s) = sign(msg1)
print(f'r: {r}, s: {s}')

# 5) verify (r, s, h, PubKey) is valid
def verify(r, s, m):
    h = hashMsg(m)
    sInv = pow(s, -1, n)
    left = cv.mul_point((h * sInv), g)
    right = cv.mul_point((r * sInv), pubKeyPoint)
    sum = cv.add_point(left, right)
    rPrime = sum.x
    return rPrime == r


print(f'is msg \'{msg1}\' signed correctly?: {verify(r, s, msg1)}')

msg2 = "hello new world"
print(f'is msg \'{msg2}\' signed correctly?: {verify(r, s, msg2)}')



