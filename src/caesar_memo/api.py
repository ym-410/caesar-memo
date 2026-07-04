from fastapi import FastAPI, HTTPException

# 相対インポート
from .storage import load_notes, create_note, read_note, update_note, delete_note
from .base64_codec import base64_decode, base64_encode
from .crypto import decrypt, encrypt
from .hash import password_to_shift

# APIアプリ本体を作る
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Caesar Memo API"}

# 一覧表示
@app.get("/notes")
def get_notes():
    notes = load_notes()

    if notes is None:
        raise HTTPException(
            status_code=404,
            detail="メモが見つかりません"
        )

    return [
        {
            "id": note["id"],
            "title": note["title"],
            "updated_at": note["updated_at"],
        }
        for note in notes
    ]

# メモ追加
@app.post("/notes")
def handle_create(title: str, body: str, password: str):

    if title == "":
        raise HTTPException(
            status_code=400,
            detail="titleは必須です"
        )
    
    if body == "":
        raise HTTPException(
            status_code=400,
            detail="bodyは必須です"
        )
    
    if password == "":
        raise HTTPException(
            status_code=400,
            detail="passwordは必須です"
        )

    shift = password_to_shift(password)
    if shift is None:
        return

    encrypted = encrypt(body, shift)
    encoded = base64_encode(encrypted.encode("utf-8"))

    note = create_note(title, encoded)
    
    return {
        "id": note["id"],
        "title": note["title"],
        "created_at": note["created_at"]
    }

# 特定メモ表示
@app.post("/notes/{note_id}/decrypt")
def post_note(note_id: int, password: str):
    note = read_note(note_id)

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="ファイルが見つかりませんでした"
        )

    try:
        shift = password_to_shift(password)
        decoded = base64_decode(note["body"]).decode("utf-8")
        decrypted = decrypt(decoded, shift)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="復号に失敗しました"
        )

    return {
        "id": note["id"],
        "title": note["title"],
        "body": decrypted,
        "created_at": note["created_at"],
        "updated_at": note["updated_at"],
    }

# メモ更新
@app.put("/notes/{note_id}")
def handle_update(note_id: int, title: str, body: str, password: str):
    if title == "":
        raise HTTPException(
            status_code=400,
            detail="titleは必須です"
        )
    
    if body == "":
        raise HTTPException(
            status_code=400,
            detail="bodyは必須です"
        )
    
    if password == "":
        raise HTTPException(
            status_code=400,
            detail="passwordは必須です"
        )
    
    note = read_note(note_id)

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="ファイルが見つかりませんでした"
        )
    
    try:
        shift = password_to_shift(password)
        encrypted = encrypt(body, shift)
        encoded = base64_encode(encrypted.encode("utf-8"))

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="暗号化に失敗しました"
        )
    
    updated_note = update_note(note_id, title, encoded)
    if updated_note is None:
        raise HTTPException(
            status_code=404,
            detail="指定されたIDのメモはありません"
        )
    return {
        "id": updated_note["id"],
        "title": updated_note["title"],
        "updated_at": updated_note["updated_at"],
        }

# メモ削除
@app.delete("/notes/{note_id}")
def handle_note(note_id: int):
    note = read_note(note_id)

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="ファイルが見つかりません"
        )
    
    success = delete_note(note_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="メモが見つかりません"
        )
    return { "success": "ノートを削除しました"}