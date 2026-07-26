# パスワードを受け取り、シフト数に変換
def input_password_shift():
    password = input("パスワード：")
    if password == "":
        print("パスワードを入力してください")
        return
    return password_to_shift(password)


def password_to_shift(password):
    total = 0

    for char in password:
        total += ord(char)

    return total % 26
