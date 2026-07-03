from crypto import encrypt, decrypt, base64_encode, base64_decode, sha256, password_to_shift
from storage import add_note, load_notes

# パスワードをシフト数に変換
def input_password_shift():
      password = input("パスワード：")
      if password == "":
           print("パスワードを入力してください")
           return
      return password_to_shift(password)

# メモを追加する
def handle_add_note():
    title = input("タイトル:")
    body = input("本文:")

    if title == "":
        print("タイトルを入力してください")
        return
    if body == "":
        print("本文を入力してください")
        return

    shift = input_password_shift()
    if shift is None:
        return

    encrypted = encrypt(body, shift)
    encoded = base64_encode(encrypted.encode("utf-8"))

    add_note(title, encoded)

    print(f"メモを保存しました。タイトル：{title}")

# メモ一覧を表示
def notes_list():
    notes = load_notes()

    if notes == []:
        print("保存されているメモはありません")
        return
    print("\nメモ一覧:")
    print("==================")
    for note in notes:
        print(f"{note["id"]}.{note["title"]}")

# 選択したメモを復号して表示する関数
def show_note():
    notes = load_notes()

    if notes == []:
        print("保存されているメモはありません。")
        return

    note_id = input("確認するメモのID:")
    if note_id == "":
        print("IDを入力してください")
        return

    try:
        note_id = int(note_id)
    except ValueError:
        print("IDは整数で入力してください")
        return

    target_note = None
    for note in notes:
        if note["id"] == note_id:
            target_note = note
            break

    if target_note is None:
        print("指定されたIDのメモはありません")
        return

    # パスワードの入力
    shift = input_password_shift()
    if shift is None:
        return

    try:
        decoded = base64_decode(target_note["body"]).decode("utf-8")
    except Exception:
        print("保存されている本文を複合できません")
        return

    # Base64化から戻したものを、シーザー暗号の復号にかける
    decrypted = decrypt(decoded, shift)

    print("\n==================")
    print(f"タイトル: {target_note["title"]}")
    print("------------------")
    print(f"本文:\n{decrypted}")
    print("==================")




def main():
      while True:
        print()
        print("=== Caesar Memo ===")
        print("1. メモを追加する")
        print("2. メモ一覧を見る")
        print("3. メモを確認する")
        print("0. 終了")

        choice = input("選択してください: ")

        if choice == "1":
            handle_add_note()
        elif choice == "2":
            notes_list()
        elif choice == "3":
            show_note()
        elif choice == "0":
            print("終了します。")
            break
        else:
            print("不正なメニュー番号です。")


if __name__ == "__main__":
      main()
