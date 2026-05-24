"""
Hill Cipher Implementation
Enkripsi: C = K * P mod 26
Dekripsi: P = K_inv * C mod 26
"""
from math import gcd


def _mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


def _det2x2(m):
    return m[0][0]*m[1][1] - m[0][1]*m[1][0]


def _det3x3(m):
    d = 0
    for j in range(3):
        minor = [[m[i][k] for k in range(3) if k != j] for i in range(1, 3)]
        d += ((-1)**j) * m[0][j] * _det2x2(minor)
    return d


def _matrix_det(m):
    return _det2x2(m) if len(m) == 2 else _det3x3(m)


def _inv_mod26(matrix):
    n = len(matrix)
    det = _matrix_det(matrix)
    det_mod = det % 26
    det_inv = _mod_inverse(det_mod, 26)
    if det_inv is None:
        return None, det, det_mod
    if n == 2:
        adj = [[matrix[1][1], -matrix[0][1]], [-matrix[1][0], matrix[0][0]]]
        return [[(det_inv * v) % 26 for v in r] for r in adj], det, det_mod
    cof = []
    for i in range(3):
        cr = []
        for j in range(3):
            minor = [[matrix[mi][mj] for mj in range(3) if mj != j] for mi in range(3) if mi != i]
            cr.append(((-1)**(i+j)) * _det2x2(minor))
        cof.append(cr)
    adj = [[cof[j][i] for j in range(3)] for i in range(3)]
    return [[(det_inv * v) % 26 for v in r] for r in adj], det, det_mod


def _mat_mul_vec(matrix, vector):
    n = len(matrix)
    result = []
    details = []
    for i in range(n):
        total = sum(matrix[i][j] * vector[j] for j in range(n))
        terms = [f"{matrix[i][j]}x{vector[j]}" for j in range(n)]
        result.append(total % 26)
        details.append({'terms': ' + '.join(terms), 'sum': total, 'mod_result': total % 26})
    return result, details


def encrypt(plaintext, key_matrix):
    n = len(key_matrix)
    for row in key_matrix:
        if len(row) != n:
            raise ValueError(f"Matriks harus {n}x{n}")
    det = _matrix_det(key_matrix)
    if gcd(det % 26, 26) != 1:
        raise ValueError(f"Matriks tidak valid: det={det}, det mod 26={det%26}. GCD harus 1.")
    clean = ''.join(c.upper() for c in plaintext if c.isalpha())
    pad = None
    if len(clean) % n != 0:
        pc = n - len(clean) % n
        pad = f"Ditambahkan {pc} huruf 'X' sebagai padding"
        clean += 'X' * pc
    blocks = [clean[i:i+n] for i in range(0, len(clean), n)]
    steps = []
    res = []
    for bi, blk in enumerate(blocks):
        vec = [ord(c)-65 for c in blk]
        rv, cd = _mat_mul_vec(key_matrix, vec)
        rt = ''.join(chr(v+65) for v in rv)
        res.append(rt)
        steps.append({'block_index': bi+1, 'block_text': blk, 'input_vector': vec,
                       'matrix': key_matrix, 'calc_details': cd, 'result_vector': rv,
                       'result_text': rt, 'detail': f"Blok {bi+1}: '{blk}' -> {vec} -> {rv} -> '{rt}'"})
    return {'input': plaintext, 'clean_input': clean, 'key_matrix': key_matrix,
            'matrix_size': f'{n}x{n}', 'determinant': det, 'determinant_mod26': det%26,
            'padding_info': pad, 'output': ''.join(res), 'steps': steps,
            'formula': 'C = K x P mod 26', 'algorithm': 'Hill Cipher', 'mode': 'Enkripsi'}


def decrypt(ciphertext, key_matrix):
    n = len(key_matrix)
    for row in key_matrix:
        if len(row) != n:
            raise ValueError(f"Matriks harus {n}x{n}")
    inv, det, det_mod = _inv_mod26(key_matrix)
    if inv is None:
        raise ValueError(f"Matriks tidak bisa diinversi: det={det}, det mod 26={det_mod}")
    det_inv = _mod_inverse(det_mod, 26)
    clean = ''.join(c.upper() for c in ciphertext if c.isalpha())
    if len(clean) % n != 0:
        clean += 'X' * (n - len(clean) % n)
    blocks = [clean[i:i+n] for i in range(0, len(clean), n)]
    steps = []
    res = []
    for bi, blk in enumerate(blocks):
        vec = [ord(c)-65 for c in blk]
        rv, cd = _mat_mul_vec(inv, vec)
        rt = ''.join(chr(v+65) for v in rv)
        res.append(rt)
        steps.append({'block_index': bi+1, 'block_text': blk, 'input_vector': vec,
                       'matrix': inv, 'calc_details': cd, 'result_vector': rv,
                       'result_text': rt, 'detail': f"Blok {bi+1}: '{blk}' -> {vec} -> {rv} -> '{rt}'"})
    return {'input': ciphertext, 'clean_input': clean, 'key_matrix': key_matrix,
            'inverse_matrix': inv, 'matrix_size': f'{n}x{n}', 'determinant': det,
            'determinant_mod26': det_mod, 'determinant_inverse': det_inv,
            'output': ''.join(res), 'steps': steps,
            'formula': 'P = K_inv x C mod 26', 'algorithm': 'Hill Cipher', 'mode': 'Dekripsi'}
