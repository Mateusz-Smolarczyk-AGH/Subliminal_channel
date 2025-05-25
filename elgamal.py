import random

def is_prime(n, k=5):
    """Test Millera-Rabina na pierwszość."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bits):
    """Generuje dużą liczbę pierwszą o podanej liczbie bitów."""
    while True:
        p = random.getrandbits(bits)
        p |= (1 << (bits - 1)) | 1

        if is_prime(p):
            return p

def power(a, b, c):
    x = 1
    y = a % c

    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c
        y = (y * y) % c
        b //= 2

    return x % c

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return g, x, y

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError('Odwrotność nie istnieje')
    else:
        return x % m

def solve_congruence(M_prime, r, X, M, p):
    m_inv = modinv(M, p - 1)
    Y = (m_inv * (M_prime - r * X)) % (p-1)
    return Y

def solve_for_M(M_prime, r, X, Y, p):
    Y_inv = modinv(Y, p - 1)
    M = (Y_inv * (M_prime - r * X)) % (p - 1)
    return M

def gen_key(M):
    p = generate_large_prime(512)
    while extended_gcd(M, p-1)[0] != 1:
        p = generate_large_prime(512)
        print(p)

    return p

def decode(coded):
    str_value = str(coded)
    str_value = str_value[:-1]
    output = ''
    if len(str_value) % 3 == 2:
        str_value = '0' + str_value
    for i in range(0, len(str_value), 3):
        output += chr(int(str_value[i:i+3]))
    return output

def elgamala_code(M, M_prime):
    while True:
        p = gen_key(M)
        g = random.randint(2, p - 2)
        r = random.randint(1, p - 2)
        k = power(g, r, p)


        X = power(g, M, p)
        Y = solve_congruence(M_prime, r, X, M, p)
        check, x, y = extended_gcd(Y, p - 1)
        if check == 1:
            break
    public_key = (k, g, p)
    private_key = r
    signature = (X, Y)

    return public_key, private_key, signature

def check_signature(public_key, signature, message, private_key=None):
    (k, g, p) = public_key
    (X, Y) = signature

    lhs = (power(k, X, p) * power(X, Y, p)) % p
    rhs = power(g, message, p)

    return lhs == rhs

def get_subliminal_channel(public_key, private_key, signature, message):
    tajne_info  = solve_for_M(message, private_key, signature[0], signature[1], public_key[2])
    # print(tajne_info)
    return decode(tajne_info)

def get_number_from_text(text):
    M = int(''.join(f"{ord(c):03d}" for c in text))
    return M*10+1

# podprogowa = 'rdasdw'
# niewinna = 'dkodfnniauausdfew'
# M = get_number_from_text(podprogowa)
# message = get_number_from_text(niewinna)
# print(M)
# get_number_from_text
# public_key, private_key, signature = elgamala_code(M, message)

# print(f"podprogowa: {podprogowa}")
# print(f"niewinna: {niewinna}")
# print(f"podprogowa_liczba: {M}")
# print(f"niewinna_liczba: {message}")

# print(f"public_key: {public_key}")
# print(f"private_key: {private_key}")
# print(f"signature: {signature}")

# check = check_signature(public_key, signature, message, private_key)
# print(f"poprawna: {check}")

# decoded = get_subliminal_channel(public_key, private_key, signature, message)
# print(f"odkodowana podprogowa: {decoded}")
