"""
Affine Cipher Implementation
Enkripsi: E(x) = (ax + b) mod 26
Dekripsi: D(x) = a_inv * (x - b) mod 26
"""

from math import gcd


def _mod_inverse(a, m):
    """Menghitung modular inverse dari a mod m menggunakan Extended Euclidean Algorithm."""
    if gcd(a, m) != 1:
        return None
    
    # Extended Euclidean Algorithm
    g, x, _ = _extended_gcd(a, m)
    if g != 1:
        return None
    return x % m


def _extended_gcd(a, b):
    """Extended Euclidean Algorithm."""
    if a == 0:
        return b, 0, 1
    g, x, y = _extended_gcd(b % a, a)
    return g, y - (b // a) * x, x


def _get_valid_a_values():
    """Return list of valid 'a' values (coprime with 26)."""
    return [a for a in range(1, 26) if gcd(a, 26) == 1]


def encrypt(plaintext, a, b):
    """
    Enkripsi teks menggunakan Affine Cipher.
    
    Args:
        plaintext (str): Teks yang akan dienkripsi
        a (int): Nilai a (harus coprime dengan 26)
        b (int): Nilai b (0-25)
    
    Returns:
        dict: Hasil enkripsi beserta langkah-langkah proses
    """
    a = int(a)
    b = int(b)

    if gcd(a, 26) != 1:
        valid_a = _get_valid_a_values()
        raise ValueError(
            f"Nilai 'a' ({a}) harus coprime dengan 26 (GCD(a,26) = 1). "
            f"Nilai 'a' yang valid: {valid_a}"
        )

    steps = []
    result = []

    for i, char in enumerate(plaintext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            x = ord(char) - base
            c_val = (a * x + b) % 26
            encrypted_char = chr(c_val + base)

            steps.append({
                'position': i + 1,
                'original': char,
                'x_value': x,
                'formula': f"({a} × {x} + {b}) mod 26 = ({a * x} + {b}) mod 26 = {(a * x + b)} mod 26 = {c_val}",
                'result': encrypted_char,
                'detail': f"'{char}' (x={x}) → E(x) = ({a} × {x} + {b}) mod 26 = {c_val} → '{encrypted_char}'"
            })
            result.append(encrypted_char)
        else:
            steps.append({
                'position': i + 1,
                'original': char,
                'x_value': '-',
                'formula': 'Non-alfabet (tidak diubah)',
                'result': char,
                'detail': f"'{char}' → Karakter non-alfabet, tidak diubah"
            })
            result.append(char)

    return {
        'input': plaintext,
        'key_a': a,
        'key_b': b,
        'output': ''.join(result),
        'steps': steps,
        'formula': f'E(x) = ({a}x + {b}) mod 26',
        'algorithm': 'Affine Cipher',
        'mode': 'Enkripsi'
    }


def decrypt(ciphertext, a, b):
    """
    Dekripsi teks menggunakan Affine Cipher.
    """
    a = int(a)
    b = int(b)

    if gcd(a, 26) != 1:
        valid_a = _get_valid_a_values()
        raise ValueError(
            f"Nilai 'a' ({a}) harus coprime dengan 26 (GCD(a,26) = 1). "
            f"Nilai 'a' yang valid: {valid_a}"
        )

    a_inv = _mod_inverse(a, 26)
    
    steps = []
    result = []

    # Add inverse calculation step
    inverse_detail = f"a⁻¹ = {a}⁻¹ mod 26 = {a_inv} (karena {a} × {a_inv} = {a * a_inv} ≡ {(a * a_inv) % 26} mod 26)"

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            y = ord(char) - base
            p_val = (a_inv * (y - b)) % 26
            decrypted_char = chr(p_val + base)

            steps.append({
                'position': i + 1,
                'original': char,
                'y_value': y,
                'formula': f"{a_inv} × ({y} - {b}) mod 26 = {a_inv} × {y - b} mod 26 = {a_inv * (y - b)} mod 26 = {p_val}",
                'result': decrypted_char,
                'detail': f"'{char}' (y={y}) → D(y) = {a_inv} × ({y} - {b}) mod 26 = {p_val} → '{decrypted_char}'"
            })
            result.append(decrypted_char)
        else:
            steps.append({
                'position': i + 1,
                'original': char,
                'y_value': '-',
                'formula': 'Non-alfabet (tidak diubah)',
                'result': char,
                'detail': f"'{char}' → Karakter non-alfabet, tidak diubah"
            })
            result.append(char)

    return {
        'input': ciphertext,
        'key_a': a,
        'key_b': b,
        'a_inverse': a_inv,
        'inverse_detail': inverse_detail,
        'output': ''.join(result),
        'steps': steps,
        'formula': f'D(y) = {a_inv} × (y - {b}) mod 26',
        'algorithm': 'Affine Cipher',
        'mode': 'Dekripsi'
    }
