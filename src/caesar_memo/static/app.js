const notesList = document.getElementById("notesList");
const noteCount = document.getElementById("noteCount");
const message = document.getElementById("message");
const selectedLabel = document.getElementById("selectedLabel");

const refreshButton = document.getElementById("refreshButton");
const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");
const clearSearchButton = document.getElementById("clearSearchButton");

const decryptForm = document.getElementById("decryptForm");
const decryptPassword = document.getElementById("decryptPassword");

const updateForm = document.getElementById("updateForm");
const updateTitle = document.getElementById("updateTitle");
const updateBody = document.getElementById("updateBody");
const updatePassword = document.getElementById("updatePassword");
const deleteButton = document.getElementById("deleteButton");

let notes = [];
let selectedId = null;

function showMessage(text, isError) {
  message.textContent = text;
  message.classList.toggle("is-error", isError === true);
}

async function requestJson(url, options) {
  const response = await fetch(url, options);
  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail);
  }

  return data;
}

function formatDate(value) {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return date.toLocaleString("ja-JP", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function renderNotes() {
  noteCount.textContent = notes.length + "件";
  notesList.textContent = "";

  if (notes.length === 0) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "メモはありません";
    notesList.appendChild(empty);
    return;
  }

  for (const note of notes) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "note-item";

    if (note.id === selectedId) {
      button.classList.add("is-selected");
    }

    const title = document.createElement("span");
    title.className = "note-title";
    title.textContent = note.title;

    const meta = document.createElement("span");
    meta.className = "note-meta";
    meta.textContent = "更新 " + formatDate(note.updated_at);

    if (note.score !== undefined) {
      meta.textContent += " / 類似度 " + (note.score * 100).toFixed(1) + "%";
    }

    button.appendChild(title);
    button.appendChild(meta);
    button.addEventListener("click", function () {
      selectNote(note);
    });

    notesList.appendChild(button);
  }
}

async function loadNotes() {
  notes = await requestJson("/notes");
  renderNotes();
}

function selectNote(note) {
  selectedId = note.id;
  selectedLabel.textContent = "ID: " + note.id;
  updateTitle.value = note.title;
  updateBody.value = "";
  updatePassword.value = "";
  decryptPassword.value = "";

  renderNotes();
  showMessage("復号するにはパスワードを入力してください");
}

refreshButton.addEventListener("click", async function () {
  try {
    await loadNotes();
    showMessage("一覧を更新しました");
  } catch (error) {
    showMessage(error.message, true);
  }
});

searchForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const keyword = searchInput.value.trim();

  if (keyword === "") {
    showMessage("検索キーワードを入力してください", true);
    return;
  }

  try {
    notes = await requestJson("/notes/search?q=" + encodeURIComponent(keyword));
    renderNotes();
    showMessage("検索しました");
  } catch (error) {
    showMessage(error.message, true);
  }
});

clearSearchButton.addEventListener("click", async function () {
  searchInput.value = "";

  try {
    await loadNotes();
    showMessage("検索を解除しました");
  } catch (error) {
    showMessage(error.message, true);
  }
});

decryptForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  if (selectedId === null) {
    showMessage("メモを選択してください", true);
    return;
  }

  try {
    const note = await requestJson("/notes/" + selectedId + "/decrypt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: decryptPassword.value }),
    });

    updateTitle.value = note.title;
    updateBody.value = note.body;
    showMessage("復号しました");
  } catch (error) {
    showMessage(error.message, true);
  }
});

updateForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  if (selectedId === null) {
    showMessage("メモを選択してください", true);
    return;
  }

  const payload = {
    title: updateTitle.value.trim(),
    body: updateBody.value,
    password: updatePassword.value,
  };

  try {
    const note = await requestJson("/notes/" + selectedId, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    await loadNotes();
    showMessage("更新しました: " + note.title);
  } catch (error) {
    showMessage(error.message, true);
  }
});

deleteButton.addEventListener("click", async function () {
  if (selectedId === null) {
    showMessage("メモを選択してください", true);
    return;
  }

  const title = updateTitle.value || "ID " + selectedId;
  const confirmed = window.confirm(title + " を削除しますか?");

  if (!confirmed) {
    return;
  }

  try {
    await requestJson("/notes/" + selectedId, {
      method: "DELETE",
    });

    selectedId = null;
    selectedLabel.textContent = "未選択";
    updateForm.reset();
    decryptPassword.value = "";

    await loadNotes();
    showMessage("削除しました");
  } catch (error) {
    showMessage(error.message, true);
  }
});

loadNotes().catch(function (error) {
  showMessage(error.message, true);
});
