import json
from pathlib import Path

# __file__: 今実行されているファイル自身のPath
# .resolve(): 絶対パスに変換
# .parents[2]: storage.py からプロジェクトルートまでのぼる
BASE_DIR = Path(__file__).resolve().parents[2]
NOTES_FILE = BASE_DIR / "notes.json"

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

# 新しいメモを追加する関数
def add_note(title, body):
    notes = load_notes()

    note = {
        "id": len(notes) + 1,
        "title": title,
        "body": body
    }
    notes.append(note)
    save_notes(notes)
