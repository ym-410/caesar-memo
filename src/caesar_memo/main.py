from crypto import encrypt, decrypt, base64_encode, base64_decode, sha256, password_to_shift

def input_password_shift():
      password = input("パスワード：")
      if password == "":
           print("パスワードを入力してください")
           return
      return password_to_shift(password)

def handle_encrypt():
    text = input("暗号化する文字列: ")

    if text == "":
        print("文字列を入力してください。")
        return

    shift = input_password_shift()
    if shift is None:
        return

    encrypted = encrypt(text, shift)
    encoded = base64_encode(encrypted.encode("utf-8"))

    print()
    print("暗号化結果:")
    print(encoded)


def handle_decrypt():
    text = input("復号化する文字列: ")

    if text == "":
        print("文字列を入力してください。")
        return

    shift = input_password_shift()
    if shift is None:
        return

    try:
        decoded = base64_decode(text).decode("utf-8")
    except Exception:
        print("Base64 として正しくない文字列です。")
        return

    decrypted = decrypt(decoded, shift)

    print()
    print("復号結果:")
    print(decrypted)


def main():
      while True:
        print()
        print("=== Caesar Memo ===")
        print("1. 暗号化する")
        print("2. 復号化する")
        print("0. 終了")

        choice = input("選択してください: ")

        if choice == "1":
            handle_encrypt()
        elif choice == "2":
            handle_decrypt()
        elif choice == "0":
            print("終了します。")
            break
        else:
            print("不正なメニュー番号です。")


if __name__ == "__main__":
      main()