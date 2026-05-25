from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.Vigenere import VigenereCipher
from cipher.RailFence import RailFenceCipher
from cipher.Playfair import PlayFairCipher
app = Flask(__name__) 

#Caesar
caesar_cipher = CaesarCipher()

@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    data = request.json
    plain_text = data.get('plain_text', '')
    if not plain_text or not isinstance(plain_text, str) or not any(char.isalpha() for char in plain_text):
        return jsonify({'error': 'Bản rõ (plain_text) của Caesar phải chứa ít nhất một chữ cái và không được để trống.'}), 400
    try:
        key = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Khóa Caesar phải là một số nguyên.'}), 400
    if key < 1 or key > 25:
        return jsonify({'error': 'Khóa Caesar phải là một số nguyên trong khoảng từ 1 đến 25.'}), 400
    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text', '')
    if not cipher_text or not isinstance(cipher_text, str) or not any(char.isalpha() for char in cipher_text):
        return jsonify({'error': 'Bản mã (cipher_text) của Caesar phải chứa ít nhất một chữ cái và không được để trống.'}), 400
    try:
        key = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Khóa Caesar phải là một số nguyên.'}), 400
    if key < 1 or key > 25:
        return jsonify({'error': 'Khóa Caesar phải là một số nguyên trong khoảng từ 1 đến 25.'}), 400
    decrypted_message = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_message})


#Vigenere
vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data.get('plain_text', '')
    key = data.get('key', '')
    if not plain_text or not isinstance(plain_text, str) or not any(char.isalpha() for char in plain_text):
        return jsonify({'error': 'Bản rõ (plain_text) của Vigenere phải chứa ít nhất một chữ cái và không được để trống.'}), 400
    if not key or not key.isalpha():
        return jsonify({'error': 'Khóa Vigenere phải là chuỗi chỉ chứa chữ cái và không được để trống.'}), 400
    return jsonify({'encrypted_text': vigenere_cipher.encrypt_text(plain_text, key)})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text', '')
    key = data.get('key', '')
    if not cipher_text or not isinstance(cipher_text, str) or not any(char.isalpha() for char in cipher_text):
        return jsonify({'error': 'Bản mã (cipher_text) của Vigenere phải chứa ít nhất một chữ cái và không được để trống.'}), 400
    if not key or not key.isalpha():
        return jsonify({'error': 'Khóa Vigenere phải là chuỗi chỉ chứa chữ cái và không được để trống.'}), 400
    return jsonify({'decrypted_text': vigenere_cipher.decrypt_text(cipher_text, key)})


#Railfence
railfence_cipher = RailFenceCipher()

@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    data = request.json
    plain_text = data.get('plain_text', '')
    if not plain_text or not isinstance(plain_text, str) or not any(char.isalpha() for char in plain_text):
        return jsonify({'error': 'Bản rõ (plain_text) của RailFence phải chứa ít nhất một chữ cái và không được để trống.'}), 400
    try:
        key = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Khóa RailFence phải là một số nguyên.'}), 400
    if key < 2:
        return jsonify({'error': 'Khóa của RailFence phải lớn hơn hoặc bằng 2.'}), 400
    if key >= len(plain_text):
        return jsonify({'error': 'Khóa của RailFence phải nhỏ hơn độ dài của bản rõ.'}), 400
    return jsonify({'encrypted_text': railfence_cipher.rail_fence_encrypt(plain_text, key)})

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text', '')
    if not cipher_text or not isinstance(cipher_text, str) or not any(char.isalpha() for char in cipher_text):
        return jsonify({'error': 'Bản mã (cipher_text) của RailFence phải chứa ít nhất một chữ cái và không được để trống.'}), 400
    try:
        key = int(data['key'])
    except (ValueError, TypeError):
        return jsonify({'error': 'Khóa RailFence phải là một số nguyên.'}), 400
    if key < 2:
        return jsonify({'error': 'Khóa của RailFence phải lớn hơn hoặc bằng 2.'}), 400
    if key >= len(cipher_text):
        return jsonify({'error': 'Khóa của RailFence phải nhỏ hơn độ dài của bản mã.'}), 400
    return jsonify({'decrypted_text': railfence_cipher.rail_fence_decrypt(cipher_text, key)})


#Playfair
playfair_cipher = PlayFairCipher()

@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    data = request.json
    key = data.get('key', '')
    if not key or not isinstance(key, str) or not any(char.isalpha() for char in key):
        return jsonify({'error': 'Khóa Playfair phải chứa ít nhất một chữ cái và không được để trống.'}), 400
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({"playfair_matrix": playfair_matrix})

@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.json
    plain_text = data.get('plain_text', '')
    key = data.get('key', '')
    if not key or not isinstance(key, str) or not any(char.isalpha() for char in key):
        return jsonify({'error': 'Khóa Playfair phải chứa ít nhất một chữ cái và không được để trống.'}), 400
    if not plain_text or not isinstance(plain_text, str) or not any(char.isalpha() for char in plain_text):
        return jsonify({'error': 'Bản rõ (plain_text) của Playfair phải chứa ít nhất một chữ cái và không được để trống.'}), 400
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({'encrypted_text': playfair_cipher.playfair_encrypt(plain_text, playfair_matrix)})

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text', '')
    key = data.get('key', '')
    if not key or not isinstance(key, str) or not any(char.isalpha() for char in key):
        return jsonify({'error': 'Khóa Playfair phải chứa ít nhất một chữ cái và không được để trống.'}), 400
    if not cipher_text or not isinstance(cipher_text, str) or not any(char.isalpha() for char in cipher_text):
        return jsonify({'error': 'Bản mã (cipher_text) của Playfair phải chứa ít nhất một chữ cái và không được để trống.'}), 400
    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({'decrypted_text': playfair_cipher.playfair_decrypt(cipher_text, playfair_matrix)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
