"""
Aplikasi Web Simulasi Kriptografi Klasik
Framework: Flask
"""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import json

from ciphers import caesar, vigenere, affine, hill, playfair

app = Flask(__name__)
app.secret_key = 'kriptografi-uts-2026-secret-key'


# ===== PAGE ROUTES =====

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/caesar')
def caesar_page():
    return render_template('caesar.html')


@app.route('/vigenere')
def vigenere_page():
    return render_template('vigenere.html')


@app.route('/affine')
def affine_page():
    return render_template('affine.html')


@app.route('/hill')
def hill_page():
    return render_template('hill.html')


@app.route('/playfair')
def playfair_page():
    return render_template('playfair.html')


@app.route('/history')
def history_page():
    history = session.get('history', [])
    return render_template('history.html', history=history)


# ===== API ROUTES =====

def _save_history(data):
    history = session.get('history', [])
    entry = {
        'algorithm': data.get('algorithm', ''),
        'mode': data.get('mode', ''),
        'input': data.get('input', ''),
        'output': data.get('output', ''),
        'key_display': data.get('key_display', ''),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    history.insert(0, entry)
    if len(history) > 50:
        history = history[:50]
    session['history'] = history


@app.route('/api/caesar', methods=['POST'])
def api_caesar():
    try:
        data = request.get_json()
        text = data.get('text', '')
        key = data.get('key', 0)
        mode = data.get('mode', 'encrypt')

        if not text:
            return jsonify({'error': 'Teks tidak boleh kosong'}), 400

        if mode == 'encrypt':
            result = caesar.encrypt(text, key)
        else:
            result = caesar.decrypt(text, key)

        result['key_display'] = f"Shift: {key}"
        _save_history(result)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500


@app.route('/api/vigenere', methods=['POST'])
def api_vigenere():
    try:
        data = request.get_json()
        text = data.get('text', '')
        key = data.get('key', '')
        mode = data.get('mode', 'encrypt')

        if not text:
            return jsonify({'error': 'Teks tidak boleh kosong'}), 400

        if mode == 'encrypt':
            result = vigenere.encrypt(text, key)
        else:
            result = vigenere.decrypt(text, key)

        result['key_display'] = f"Keyword: {key}"
        _save_history(result)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500


@app.route('/api/affine', methods=['POST'])
def api_affine():
    try:
        data = request.get_json()
        text = data.get('text', '')
        a = data.get('a', 1)
        b = data.get('b', 0)
        mode = data.get('mode', 'encrypt')

        if not text:
            return jsonify({'error': 'Teks tidak boleh kosong'}), 400

        if mode == 'encrypt':
            result = affine.encrypt(text, a, b)
        else:
            result = affine.decrypt(text, a, b)

        result['key_display'] = f"a={a}, b={b}"
        _save_history(result)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500


@app.route('/api/hill', methods=['POST'])
def api_hill():
    try:
        data = request.get_json()
        text = data.get('text', '')
        matrix = data.get('matrix', [])
        mode = data.get('mode', 'encrypt')

        if not text:
            return jsonify({'error': 'Teks tidak boleh kosong'}), 400

        # Convert to int
        key_matrix = [[int(v) for v in row] for row in matrix]

        if mode == 'encrypt':
            result = hill.encrypt(text, key_matrix)
        else:
            result = hill.decrypt(text, key_matrix)

        size = len(key_matrix)
        mat_str = str(key_matrix)
        result['key_display'] = f"Matrix {size}x{size}: {mat_str}"
        _save_history(result)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500


@app.route('/api/playfair', methods=['POST'])
def api_playfair():
    try:
        data = request.get_json()
        text = data.get('text', '')
        key = data.get('key', '')
        mode = data.get('mode', 'encrypt')

        if not text:
            return jsonify({'error': 'Teks tidak boleh kosong'}), 400

        if mode == 'encrypt':
            result = playfair.encrypt(text, key)
        else:
            result = playfair.decrypt(text, key)

        result['key_display'] = f"Keyword: {key}"
        _save_history(result)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Terjadi kesalahan: {str(e)}'}), 500


@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    session['history'] = []
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
