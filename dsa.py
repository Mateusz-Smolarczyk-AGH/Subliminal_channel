from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import elgamal
# Generowanie pary kluczy DSA
def get_keys():
    key = DSA.generate(1024)
    private_key = key.x
    public_key = (key.p, key.q, key.g, key.y)
    return private_key, public_key

def hash_int_to_int(number):
    # Konwertowanie liczby całkowitej na ciąg bajtów
    byte_string = str(number).encode('utf-8')
    # Obliczanie skrótu SHA-256
    sha256_hash = SHA256.new(byte_string).hexdigest()
    # Konwertowanie skrótu na liczbę całkowitą
    hashed_number = int(sha256_hash, 16)
    return hashed_number

def get_sign(private_key, public_key, message, subbominal_message):
    hashed = hash_int_to_int(message)
    p, q, g, y = public_key
    r = elgamal.power(g, subbominal_message, p) % q
    k_inv = elgamal.modinv(subbominal_message, q)
    s = (k_inv * (hashed + private_key * r)) % q
    return r, s 

def verify(signature, public_key, message):
    p, q, g, y = public_key
    r, s = signature
    w = elgamal.modinv(s, q) % q
    u1 = (hash_int_to_int(message) * w) % q
    u2 = (r * w) % q
    v = ((elgamal.power(g, u1 ,p) * elgamal.power(y, u2 ,p)) % p) % q
    return v == r

def get_subominal(signature, public_key, message, private_key):
    p, q, g, y = public_key
    r, s = signature
    h = hash_int_to_int(message)
    s_inv = elgamal.modinv(s, q)
    result = (s_inv * (h + private_key*r)) % q
    return elgamal.decode(result)

# podprogowa = 'rdaqsdw'
# niewinna = 'dkodfnniadduausdfew'
# subbominal_message = elgamal.get_number_from_text(podprogowa)
# message = elgamal.get_number_from_text(niewinna)
# private_key, public_key = get_keys()
# print(private_key)
# print(public_key)
# message = b'text'
# signature = get_sign(private_key, public_key, message, subbominal_message)
# print(signature)
# print(verify(signature, public_key, message))
# output = get_subominal(signature, public_key, message, private_key)
# print(elgamal.decode(output))