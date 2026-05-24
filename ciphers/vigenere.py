"""
Vigenère Cipher Implementation
Enkripsi: Ci = (Pi + Ki) mod 26
Dekripsi: Pi = (Ci - Ki) mod 26
"""


def _extend_key(text, key):
    """Extend key to match the length of alphabetic characters in text."""
    key = key.upper()
    key_chars = []
    key_index = 0
    for char in text:
        if char.isalpha():
            key_chars.append(key[key_index % len(key)])
            key_index += 1
        else:
            key_chars.append(None)
    return key_chars


def encrypt(plaintext, key):
    """
    Enkripsi teks menggunakan Vigenère Cipher.
    
    Args:
        plaintext (str): Teks yang akan dienkripsi
        key (str): Kata kunci
    
    Returns:
        dict: Hasil enkripsi beserta langkah-langkah proses
    """
    if not key or not key.isalpha():
        raise ValueError("Key harus berupa huruf alfabet (tanpa angka/simbol)")

    key_upper = key.upper()
    extended_key = _extend_key(plaintext, key_upper)

    steps = []
    result = []

    for i, char in enumerate(plaintext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            p_val = ord(char.upper()) - ord('A')
            k_val = ord(extended_key[i]) - ord('A')
            c_val = (p_val + k_val) % 26
            encrypted_char = chr(c_val + base)

            steps.append({
                'position': i + 1,
                'original': char,
                'key_char': extended_key[i],
                'p_value': p_val,
                'k_value': k_val,
                'formula': f"({p_val} + {k_val}) mod 26 = {c_val}",
                'result': encrypted_char,
                'detail': f"'{char}' (P={p_val}) + '{extended_key[i]}' (K={k_val}) → C = ({p_val} + {k_val}) mod 26 = {c_val} → '{encrypted_char}'"
            })
            result.append(encrypted_char)
        else:
            steps.append({
                'position': i + 1,
                'original': char,
                'key_char': '-',
                'p_value': '-',
                'k_value': '-',
                'formula': 'Non-alfabet (tidak diubah)',
                'result': char,
                'detail': f"'{char}' → Karakter non-alfabet, tidak diubah"
            })
            result.append(char)

    # Build key extension display
    key_extension = []
    ki = 0
    for char in plaintext:
        if char.isalpha():
            key_extension.append(key_upper[ki % len(key_upper)])
            ki += 1
        else:
            key_extension.append('-')

    return {
        'input': plaintext,
        'key': key,
        'key_extension': ''.join(key_extension),
        'output': ''.join(result),
        'steps': steps,
        'formula': 'Ci = (Pi + Ki) mod 26',
        'algorithm': 'Vigenère Cipher',
        'mode': 'Enkripsi'
    }


def decrypt(ciphertext, key):
    """
    Dekripsi teks menggunakan Vigenère Cipher.
    """
    if not key or not key.isalpha():
        raise ValueError("Key harus berupa huruf alfabet (tanpa angka/simbol)")

    key_upper = key.upper()
    extended_key = _extend_key(ciphertext, key_upper)

    steps = []
    result = []

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            c_val = ord(char.upper()) - ord('A')
            k_val = ord(extended_key[i]) - ord('A')
            p_val = (c_val - k_val) % 26
            decrypted_char = chr(p_val + base)

            steps.append({
                'position': i + 1,
                'original': char,
                'key_char': extended_key[i],
                'c_value': c_val,
                'k_value': k_val,
                'formula': f"({c_val} - {k_val}) mod 26 = {p_val}",
                'result': decrypted_char,
                'detail': f"'{char}' (C={c_val}) - '{extended_key[i]}' (K={k_val}) → P = ({c_val} - {k_val}) mod 26 = {p_val} → '{decrypted_char}'"
            })
            result.append(decrypted_char)
        else:
            steps.append({
                'position': i + 1,
                'original': char,
                'key_char': '-',
                'c_value': '-',
                'k_value': '-',
                'formula': 'Non-alfabet (tidak diubah)',
                'result': char,
                'detail': f"'{char}' → Karakter non-alfabet, tidak diubah"
            })
            result.append(char)

    key_extension = []
    ki = 0
    for char in ciphertext:
        if char.isalpha():
            key_extension.append(key_upper[ki % len(key_upper)])
            ki += 1
        else:
            key_extension.append('-')

    return {
        'input': ciphertext,
        'key': key,
        'key_extension': ''.join(key_extension),
        'output': ''.join(result),
        'steps': steps,
        'formula': 'Pi = (Ci - Ki) mod 26',
        'algorithm': 'Vigenère Cipher',
        'mode': 'Dekripsi'
    }
