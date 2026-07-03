from fastapi import FastAPI

from .storage import load_notes

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Caesar Memo API"}


@app.get("/notes")
def get_notes():
    return load_notes()
