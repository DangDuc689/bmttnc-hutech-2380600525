class PlayFairCipher:
    def __init__(self) -> None:
        pass

    def create_playfair_matrix(self, key: str):
        # Chuyển J thành I và chữ hoa
        key = key.upper().replace("J", "I")
        # Giữ lại các chữ cái
        key = "".join([c for c in key if c.isalpha()])
        
        # Loại bỏ các chữ cái trùng lặp mà vẫn giữ nguyên thứ tự xuất hiện đầu tiên
        seen = set()
        unique_key = []
        for letter in key:
            if letter not in seen:
                seen.add(letter)
                unique_key.append(letter)
        
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        remaining_letters = [letter for letter in alphabet if letter not in seen]
        matrix = unique_key + remaining_letters
        
        # Tạo ma trận 5x5
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        return None

    def playfair_encrypt(self, plain_text: str, matrix) -> str:
        # Chuyển J thành I và chữ hoa, chỉ giữ chữ cái
        plain_text = plain_text.upper().replace("J", "I")
        plain_text = "".join([c for c in plain_text if c.isalpha()])
        
        # Chèn ký tự 'X' giữa hai chữ cái giống nhau đứng cạnh nhau và đệm 'X' nếu độ dài lẻ
        prepared_text = ""
        i = 0
        while i < len(plain_text):
            char1 = plain_text[i]
            if i + 1 < len(plain_text):
                char2 = plain_text[i+1]
                if char1 == char2:
                    prepared_text += char1 + "X"
                    i += 1
                else:
                    prepared_text += char1 + char2
                    i += 2
            else:
                prepared_text += char1 + "X"
                i += 1
        
        encrypted_text = ""
        for i in range(0, len(prepared_text), 2):
            pair = prepared_text[i:i+2]
            coords1 = self.find_letter_coords(matrix, pair[0])
            coords2 = self.find_letter_coords(matrix, pair[1])
            
            if not coords1 or not coords2:
                # Trường hợp không tìm thấy (đề phòng)
                encrypted_text += pair
                continue
                
            row1, col1 = coords1
            row2, col2 = coords2

            if row1 == row2:  # Cùng hàng
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Cùng cột
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:  # Tạo hình chữ nhật
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text: str, matrix) -> str:
        # Chuẩn hóa ciphertext
        cipher_text = cipher_text.upper().replace("J", "I")
        cipher_text = "".join([c for c in cipher_text if c.isalpha()])
        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            if len(pair) < 2:
                decrypted_text += pair
                continue
                
            coords1 = self.find_letter_coords(matrix, pair[0])
            coords2 = self.find_letter_coords(matrix, pair[1])
            
            if not coords1 or not coords2:
                decrypted_text += pair
                continue
                
            row1, col1 = coords1
            row2, col2 = coords2

            if row1 == row2:  # Cùng hàng
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  # Cùng cột
                encrypted_letter1 = matrix[(row1 - 1) % 5][col1]
                encrypted_letter2 = matrix[(row2 - 1) % 5][col2]
                decrypted_text += encrypted_letter1 + encrypted_letter2
            else:  # Tạo hình chữ nhật
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]

        # Loại bỏ ký tự 'X' đệm giữa các chữ giống nhau và ký tự đệm lẻ ở cuối
        banro = ""
        idx = 0
        while idx < len(decrypted_text):
            if idx + 2 < len(decrypted_text) and decrypted_text[idx] == decrypted_text[idx+2] and decrypted_text[idx+1] == "X":
                banro += decrypted_text[idx] + decrypted_text[idx+2]
                idx += 3
            else:
                banro += decrypted_text[idx]
                idx += 1
        
        if banro.endswith("X"):
            banro = banro[:-1]

        return banro