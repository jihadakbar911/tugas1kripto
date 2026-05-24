"""
Caesar Cipher Implementation
Enkripsi: C = (P + K) mod 26
Dekripsi: P = (C - K) mod 26
"""


def encrypt(plaintext, key):
    """
    Enkripsi teks menggunakan Caesar Cipher.
    
    Args:
        plaintext (str): Teks yang akan dienkripsi
        key (int): Nilai shift (1-25)
    
    Returns:
        dict: Hasil enkripsi beserta langkah-langkah proses
    """
    key = int(key)
    if key < 1 or key > 25:
        raise ValueError("Nilai key harus antara 1-25")

    steps = []
    result = []

    for i, char in enumerate(plaintext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            p_val = ord(char) - base
            c_val = (p_val + key) % 26
            encrypted_char = chr(c_val + base)

            steps.append({
                'position': i + 1,
                'original': char,
                'p_value': p_val,
                'formula': f"({p_val} + {key}) mod 26 = {c_val}",
                'result': encrypted_char,
                'detail': f"'{char}' (P={p_val}) → C = ({p_val} + {key}) mod 26 = {c_val} → '{encrypted_char}'"
            })
            result.append(encrypted_char)
        else:
            steps.append({
                'position': i + 1,
                'original': char,
                'p_value': '-',
                'formula': 'Non-alfabet (tidak diubah)',
                'result': char,
                'detail': f"'{char}' → Karakter non-alfabet, tidak diubah"
            })
            result.append(char)

    return {
        'input': plaintext,
        'key': key,
        'output': ''.join(result),
        'steps': steps,
        'formula': 'C = (P + K) mod 26',
        'algorithm': 'Caesar Cipher',
        'mode': 'Enkripsi'
    }


def decrypt(ciphertext, key):
    """
    Dekripsi teks menggunakan Caesar Cipher.
    
    Args:
        ciphertext (str): Teks yang akan didekripsi
        key (int): Nilai shift (1-25)
    
    Returns:
        dict: Hasil dekripsi beserta langkah-langkah proses
    """
    key = int(key)
    if key < 1 or key > 25:
        raise ValueError("Nilai key harus antara 1-25")

    steps = []
    result = []

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            c_val = ord(char) - base
            p_val = (c_val - key) % 26
            decrypted_char = chr(p_val + base)

            steps.append({
                'position': i + 1,
                'original': char,
                'c_value': c_val,
                'formula': f"({c_val} - {key}) mod 26 = {p_val}",
                'result': decrypted_char,
                'detail': f"'{char}' (C={c_val}) → P = ({c_val} - {key}) mod 26 = {p_val} → '{decrypted_char}'"
            })
            result.append(decrypted_char)
        else:
            steps.append({
                'position': i + 1,
                'original': char,
                'c_value': '-',
                'formula': 'Non-alfabet (tidak diubah)',
                'result': char,
                'detail': f"'{char}' → Karakter non-alfabet, tidak diubah"
            })
            result.append(char)

    return {
        'input': ciphertext,
        'key': key,
        'output': ''.join(result),
        'steps': steps,
        'formula': 'P = (C - K) mod 26',
        'algorithm': 'Caesar Cipher',
        'mode': 'Dekripsi'
    }
