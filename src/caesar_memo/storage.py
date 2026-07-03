import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

# __file__: 今実行されているファイル自身のPath
# .resolve(): 絶対パスに変換
# .parents[2]: storage.py からプロジェクトルートまでのぼる
BASE_DIR = Path(__file__).resolve().parents[2]
NOTES_FILE = BASE_DIR / "notes.json"

# 現在時刻を取得する関数
def current_time():
    jst = timezone(timedelta(hours=9))
    return datetime.now(jst).isoformat(timespec="seconds")

# 既存メモを読み込む関数
def load_notes():
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return[]
    except json.JSONDecodeError:
        return []

# メモ一覧を保存する関数
def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=2)

# メモ一覧を表示
def notes_list():
    notes = load_notes()

    if notes == []:
        print("保存されているメモはありません")
        return
    print("\nメモ一覧:")
    print("==================")
    for note in notes:
        print(f'{note["id"]}.{note["title"]}')

# 新しいメモを追加する関数
def create_note(title, body):
    notes = load_notes()
    now = current_time()

    note = {
        "id": max([note["id"] for note in notes], default=0) + 1,
        "title": title,
        "body": body,
        "created_at": now,
        "updated_at": now
    }
    notes.append(note)
    save_notes(notes)

# メモ一件を指定・復号して読み取る関数
def read_note(note_id):
    notes = load_notes()

    if notes == []:
        return

    for note in notes:
        if note["id"] == note_id:
            return note
    return None

# メモを更新する関数
def update_note(note_id, title, body):
    notes = load_notes()
    now = current_time()

    for note in notes:
        if note["id"] == note_id:
            note["title"] = title
            note["body"] = body
            note["updated_at"] = now
            save_notes(notes)
            return True
    return False

# メモを削除する関数
def delete_note(note_id):
    notes = load_notes()

    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            save_notes(notes)
            return True
    return False
