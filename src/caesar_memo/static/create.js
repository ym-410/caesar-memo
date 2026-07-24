const message = document.getElementById("message");
const createForm = document.getElementById("createForm");
const createTitle = document.getElementById("createTitle");
const createBody = document.getElementById("createBody");
const createPassword = document.getElementById("createPassword");

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

createForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const payload = {
    title: createTitle.value.trim(),
    body: createBody.value,
    password: createPassword.value,
  };

  try {
    const note = await requestJson("/notes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    showMessage("保存しました: " + note.title);
    createForm.reset();
  } catch (error) {
    showMessage(error.message, true);
  }
});
