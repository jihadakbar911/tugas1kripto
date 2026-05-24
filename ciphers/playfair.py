"""
Playfair Cipher Implementation
Uses 5x5 key matrix (I/J merged).
"""


def _generate_matrix(key):
    key = key.upper().replace('J', 'I')
    seen = set()
    matrix_chars = []
    for c in key:
        if c.isalpha() and c not in seen:
            seen.add(c)
            matrix_chars.append(c)
    for c in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if c not in seen:
            seen.add(c)
            matrix_chars.append(c)
    matrix = [matrix_chars[i*5:(i+1)*5] for i in range(5)]
    return matrix


def _find_pos(matrix, char):
    char = char.upper()
    if char == 'J':
        char = 'I'
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None


def _prepare_text(text):
    text = text.upper().replace('J', 'I')
    clean = ''.join(c for c in text if c.isalpha())
    pairs = []
    i = 0
    while i < len(clean):
        if i + 1 >= len(clean):
            pairs.append((clean[i], 'X'))
            i += 1
        elif clean[i] == clean[i + 1]:
            pairs.append((clean[i], 'X'))
            i += 1
        else:
            pairs.append((clean[i], clean[i + 1]))
            i += 2
    return pairs


def encrypt(plaintext, key):
    if not key or not key.isalpha():
        raise ValueError("Key harus berupa huruf alfabet")
    matrix = _generate_matrix(key)
    pairs = _prepare_text(plaintext)
    steps = []
    result = []
    for pi, (a, b) in enumerate(pairs):
        ra, ca = _find_pos(matrix, a)
        rb, cb = _find_pos(matrix, b)
        if ra == rb:
            rule = 'Baris sama'
            ea = matrix[ra][(ca + 1) % 5]
            eb = matrix[rb][(cb + 1) % 5]
            rule_detail = f"Baris sama (baris {ra}) -> geser kanan"
        elif ca == cb:
            rule = 'Kolom sama'
            ea = matrix[(ra + 1) % 5][ca]
            eb = matrix[(rb + 1) % 5][cb]
            rule_detail = f"Kolom sama (kolom {ca}) -> geser bawah"
        else:
            rule = 'Persegi panjang'
            ea = matrix[ra][cb]
            eb = matrix[rb][ca]
            rule_detail = f"Persegi panjang -> tukar kolom ({ca}<->{cb})"
        result.extend([ea, eb])
        steps.append({
            'pair_index': pi + 1, 'pair': f"{a}{b}",
            'pos_a': f"({ra},{ca})", 'pos_b': f"({rb},{cb})",
            'rule': rule, 'rule_detail': rule_detail,
            'result': f"{ea}{eb}",
            'detail': f"'{a}{b}' [{ra},{ca}][{rb},{cb}] {rule_detail} -> '{ea}{eb}'"
        })
    pair_display = ' '.join(f"{a}{b}" for a, b in pairs)
    return {
        'input': plaintext, 'key': key, 'matrix': matrix,
        'pairs': pair_display, 'output': ''.join(result),
        'steps': steps, 'formula': 'Playfair 5x5 Matrix',
        'algorithm': 'Playfair Cipher', 'mode': 'Enkripsi'
    }


def decrypt(ciphertext, key):
    if not key or not key.isalpha():
        raise ValueError("Key harus berupa huruf alfabet")
    matrix = _generate_matrix(key)
    clean = ciphertext.upper().replace('J', 'I')
    clean = ''.join(c for c in clean if c.isalpha())
    if len(clean) % 2 != 0:
        clean += 'X'
    pairs = [(clean[i], clean[i+1]) for i in range(0, len(clean), 2)]
    steps = []
    result = []
    for pi, (a, b) in enumerate(pairs):
        ra, ca = _find_pos(matrix, a)
        rb, cb = _find_pos(matrix, b)
        if ra == rb:
            rule = 'Baris sama'
            da = matrix[ra][(ca - 1) % 5]
            db = matrix[rb][(cb - 1) % 5]
            rule_detail = f"Baris sama (baris {ra}) -> geser kiri"
        elif ca == cb:
            rule = 'Kolom sama'
            da = matrix[(ra - 1) % 5][ca]
            db = matrix[(rb - 1) % 5][cb]
            rule_detail = f"Kolom sama (kolom {ca}) -> geser atas"
        else:
            rule = 'Persegi panjang'
            da = matrix[ra][cb]
            db = matrix[rb][ca]
            rule_detail = f"Persegi panjang -> tukar kolom ({ca}<->{cb})"
        result.extend([da, db])
        steps.append({
            'pair_index': pi + 1, 'pair': f"{a}{b}",
            'pos_a': f"({ra},{ca})", 'pos_b': f"({rb},{cb})",
            'rule': rule, 'rule_detail': rule_detail,
            'result': f"{da}{db}",
            'detail': f"'{a}{b}' [{ra},{ca}][{rb},{cb}] {rule_detail} -> '{da}{db}'"
        })
    pair_display = ' '.join(f"{a}{b}" for a, b in pairs)
    return {
        'input': ciphertext, 'key': key, 'matrix': matrix,
        'pairs': pair_display, 'output': ''.join(result),
        'steps': steps, 'formula': 'Playfair 5x5 Matrix',
        'algorithm': 'Playfair Cipher', 'mode': 'Dekripsi'
    }
