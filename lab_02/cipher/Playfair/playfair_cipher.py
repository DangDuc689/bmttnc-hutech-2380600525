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
        # Chuẩn hóa chữ cái và thay J bằng I
        normalized_text = plain_text.upper().replace("J", "I")
        
        # Tách chữ cái và ghi nhận index gốc của chữ cái
        char_list = []
        source_indices = []
        non_alphas = []
        for i, c in enumerate(normalized_text):
            if c.isalpha():
                char_list.append(c)
                source_indices.append(i)
            else:
                non_alphas.append((i, c))
                
        # Chèn ký tự 'X' giữa hai chữ cái giống nhau đứng cạnh nhau và đệm 'X' nếu độ dài lẻ
        # Đồng thời ánh xạ chỉ số tương ứng
        prepared_text = ""
        prepared_indices = []
        
        i = 0
        while i < len(char_list):
            char1 = char_list[i]
            idx1 = source_indices[i]
            if i + 1 < len(char_list):
                char2 = char_list[i+1]
                idx2 = source_indices[i+1]
                if char1 == char2:
                    prepared_text += char1 + "X"
                    prepared_indices.extend([idx1, -1])
                    i += 1
                else:
                    prepared_text += char1 + char2
                    prepared_indices.extend([idx1, idx2])
                    i += 2
            else:
                prepared_text += char1 + "X"
                prepared_indices.extend([idx1, -1])
                i += 1
        
        encrypted_letters = ""
        for i in range(0, len(prepared_text), 2):
            pair = prepared_text[i:i+2]
            coords1 = self.find_letter_coords(matrix, pair[0])
            coords2 = self.find_letter_coords(matrix, pair[1])
            
            if not coords1 or not coords2:
                encrypted_letters += pair
                continue
                
            row1, col1 = coords1
            row2, col2 = coords2

            if row1 == row2:  # Cùng hàng
                encrypted_letters += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Cùng cột
                encrypted_letters += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:  # Tạo hình chữ nhật
                encrypted_letters += matrix[row1][col2] + matrix[row2][col1]

        # Ghép lại các ký tự số (non-alpha) vào encrypted_letters
        result = []
        added_non_alpha_indices = set()
        
        # Duyệt qua các chữ cái đã mã hóa và chèn các số vào đúng vị trí tương đối
        for j in range(len(prepared_indices)):
            orig_idx = prepared_indices[j]
            if orig_idx != -1:
                # Tìm các số có index gốc nhỏ hơn orig_idx và chưa được thêm
                for num_idx, num_char in non_alphas:
                    if num_idx < orig_idx and num_idx not in added_non_alpha_indices:
                        result.append(num_char)
                        added_non_alpha_indices.add(num_idx)
                result.append(encrypted_letters[j])
            else:
                # Với ký tự đệm X, cứ chèn trực tiếp chữ cái mã hóa
                result.append(encrypted_letters[j])
                
        # Thêm các số còn lại ở cuối chuỗi
        for num_idx, num_char in non_alphas:
            if num_idx not in added_non_alpha_indices:
                result.append(num_char)
                added_non_alpha_indices.add(num_idx)
                
        return "".join(result)

    def playfair_decrypt(self, cipher_text: str, matrix) -> str:
        # Chuẩn hóa ciphertext
        normalized_text = cipher_text.upper().replace("J", "I")
        
        # Tách chữ cái và ghi nhận index gốc của chữ cái trong ciphertext
        char_list = []
        source_indices = []
        non_alphas = []
        for i, c in enumerate(normalized_text):
            if c.isalpha():
                char_list.append(c)
                source_indices.append(i)
            else:
                non_alphas.append((i, c))
                
        # Giải mã chuỗi chữ cái
        decrypted_letters = ""
        for i in range(0, len(char_list), 2):
            pair = "".join(char_list[i:i+2])
            if len(pair) < 2:
                decrypted_letters += pair
                continue
                
            coords1 = self.find_letter_coords(matrix, pair[0])
            coords2 = self.find_letter_coords(matrix, pair[1])
            
            if not coords1 or not coords2:
                decrypted_letters += pair
                continue
                
            row1, col1 = coords1
            row2, col2 = coords2

            if row1 == row2:  # Cùng hàng
                decrypted_letters += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  # Cùng cột
                decrypted_letter1 = matrix[(row1 - 1) % 5][col1]
                decrypted_letter2 = matrix[(row2 - 1) % 5][col2]
                decrypted_letters += decrypted_letter1 + decrypted_letter2
            else:  # Tạo hình chữ nhật
                decrypted_letters += matrix[row1][col2] + matrix[row2][col1]

        # Ghép các chữ cái đã giải mã với các chữ số theo vị trí tương đối
        temp_result = []
        added_non_alpha_indices = set()
        
        for j in range(len(source_indices)):
            orig_idx = source_indices[j]
            for num_idx, num_char in non_alphas:
                if num_idx < orig_idx and num_idx not in added_non_alpha_indices:
                    temp_result.append(num_char)
                    added_non_alpha_indices.add(num_idx)
            temp_result.append(decrypted_letters[j])
            
        for num_idx, num_char in non_alphas:
            if num_idx not in added_non_alpha_indices:
                temp_result.append(num_char)
                added_non_alpha_indices.add(num_idx)
                
        decrypted_text_with_nums = "".join(temp_result)
        
        # Loại bỏ các chữ cái đệm 'X' trên chuỗi đã giải mã
        letters_info = []
        for idx, char in enumerate(decrypted_text_with_nums):
            if char.isalpha():
                letters_info.append((idx, char))
                
        indices_to_remove = set()
        idx_letters = 0
        while idx_letters < len(letters_info):
            if idx_letters + 2 < len(letters_info):
                char1 = letters_info[idx_letters][1]
                char_mid = letters_info[idx_letters+1][1]
                char2 = letters_info[idx_letters+2][1]
                if char1 == char2 and char_mid == 'X':
                    indices_to_remove.add(letters_info[idx_letters+1][0])
                    idx_letters += 2
                    continue
            idx_letters += 1
            
        if letters_info and letters_info[-1][1] == 'X':
            indices_to_remove.add(letters_info[-1][0])
            
        final_result = [char for idx, char in enumerate(decrypted_text_with_nums) if idx not in indices_to_remove]
        return "".join(final_result)