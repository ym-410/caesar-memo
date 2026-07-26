from .base64_codec import base64_encode, base64_decode
from .crypto import encrypt, decrypt
from .storage import load_notes, notes_list, create_note, read_note, update_note, delete_note
from .password_shift import input_password_shift
from .search import search_notes

# メモを作成する
def handle_create():
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

    create_note(title, encoded)

    print(f"メモを保存しました。タイトル：{title}")

# メモを1件読み取る
def handle_read():
    try:
        note_id = int(input("確認するメモのID:"))
    except ValueError:
        print("IDは整数で入力してください")
        return

    note = read_note(note_id)
    if note is None:
        print("指定されたIDのメモはありません")
        return

    title = note["title"]
    body = note["body"]

    # パスワードの入力
    shift = input_password_shift()
    if shift is None:
        return

    try:
        decoded = base64_decode(body).decode("utf-8")
    except Exception:
        print("保存されている本文を復号できません")
        return

    # Base64化から戻したものを、シーザー暗号の復号にかける
    decrypted = decrypt(decoded, shift)

    print("\n==================")
    print(f"タイトル: {title}")
    print("------------------")
    print(f"本文:\n{decrypted}")
    print("==================")

def handle_update():

    try:
        note_id = int(input("更新するメモのID:"))
    except ValueError:
        print("IDは整数で入力してください")
        return

    title = input("変更後のタイトル:")
    if title == "":
        print("タイトルを入力してください")
        return

    body = input("本文を入力してください: ")
    if body == "":
        print("本文を入力してください")
        return

    shift = input_password_shift()
    if shift is None:
        return

    encrypted = encrypt(body, shift)
    encoded = base64_encode(encrypted.encode("utf-8"))

    success = update_note(note_id, title, encoded)
    if success:
        print("ノートを更新しました")
    else:
        print("指定されたIDのメモはありません")


def handle_delete():
    try:
        note_id = int(input("削除するメモのID:"))
    except ValueError:
        print("IDは整数で入力してください")
        return

    success = delete_note(note_id)
    if success:
        print(f"メモ(ID:{note_id})が削除されました。")
    else:
        print("指定されたIDのメモはありません")

def handle_search():
    keyword = input("検索キーワード:")

    if keyword == "":
        print("検索キーワードを入力してください")
        return

    notes = load_notes()

    if notes == []:
        print("保存されているメモはありません")
        return

    results = search_notes(notes, keyword)

    if results == []:
        print("該当するメモはありませんでした")
        return

    print("\n検索結果")
    for result in results:
        note = result["note"]
        score = result["score"]
        print(f'id: {note["id"]}, title:{note["title"]} 類似度: {score * 100:.2f}%')

def main():
      while True:
        print()
        print("=== Caesar Memo ===")
        print("1. メモを追加する")
        print("2. メモ一覧を見る")
        print("3. メモを確認する")
        print("4. メモを更新する")
        print("5. メモを削除する")
        print("6. タイトルから検索する")
        print("0. 終了")

        choice = input("選択してください: ")

        if choice == "1":
            handle_create()
        elif choice == "2":
            notes_list()
        elif choice == "3":
            handle_read()
        elif choice == "4":
            handle_update()
        elif choice == "5":
            handle_delete()
        elif choice == "6":
            handle_search()
        elif choice == "0":
            print("終了します。")
            break
        else:
            print("不正なメニュー番号です。")


if __name__ == "__main__":
      main()
