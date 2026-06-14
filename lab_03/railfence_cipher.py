import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.railfence import Ui_MainWindow
import requests


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Set parent window for message boxes
        self.ui.set_parent_window(self)

        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        # Validate input first
        if not self.ui.validate_encrypt():
            return
            
        url = "http://127.0.0.1:5000/api/railfence/encrypt"

        payload = {
            "plain_text": self.ui.txt_plainText.toPlainText(),
            "key": self.ui.txt_key.toPlainText()
        }

        try:
            response = requests.post(url, json=payload)

            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                try:
                    data = response.json()

                    self.ui.txt_cipherText.setPlainText(
                        data.get("encrypted_text", "")
                    )

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Encrypted Successfully")
                    msg.exec_()

                except requests.exceptions.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")

            else:
                try:
                    error_msg = response.json().get("error", "Error while calling API")
                except Exception:
                    error_msg = "Error while calling API"
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(error_msg)
                msg.setWindowTitle("Lỗi API")
                msg.exec_()

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Không thể kết nối API: {e}")
            msg.setWindowTitle("Lỗi Kết Nối")
            msg.exec_()

    def call_api_decrypt(self):
        # Validate input first
        if not self.ui.validate_decrypt():
            return
            
        url = "http://127.0.0.1:5000/api/railfence/decrypt"

        payload = {
            "cipher_text": self.ui.txt_cipherText.toPlainText(),
            "key": self.ui.txt_key.toPlainText()
        }

        try:
            response = requests.post(url, json=payload)

            print("Response status code:", response.status_code)
            print("Response text:", response.text)

            if response.status_code == 200:
                try:
                    data = response.json()

                    self.ui.txt_plainText.setPlainText(
                        data.get("decrypted_text", "")
                    )

                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Decrypted Successfully")
                    msg.exec_()

                except requests.exceptions.JSONDecodeError as e:
                    print(f"JSON Decode Error: {e}")

            else:
                try:
                    error_msg = response.json().get("error", "Error while calling API")
                except Exception:
                    error_msg = "Error while calling API"
                
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(error_msg)
                msg.setWindowTitle("Lỗi API")
                msg.exec_()

        except requests.exceptions.RequestException as e:
            print(f"Error while calling API: {e}")
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText(f"Không thể kết nối API: {e}")
            msg.setWindowTitle("Lỗi Kết Nối")
            msg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec_())