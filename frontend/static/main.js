// Live preview + send to Flask
const textarea = document.getElementById("reqText");
const preview = document.getElementById("preview");
const textareaBox = document.querySelector(".textarea-box"); // whole right box

textarea.addEventListener("input", () => {
  if (textarea.value.trim() !== "") {
    const text = textarea.value;

    // Show in preview
    preview.innerText = text;

    // Hide textarea box
    textareaBox.style.display = "none";

    // Send requirement to Flask
    fetch("/job_desc", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ requirement: text })
    })
    .then(res => res.json())
    .then(data => {
      console.log("✅ Requirement sent:", data);
    })
    .catch(err => console.error("❌ Error sending requirement:", err));
  }
});

// Example JSON for candidates table (later replace with Flask API call)
const candidates = [
  {"name": "Ali Khan", "role": "ML Engineer", "experience": "2 years"},
  {"name": "Sara Ahmed", "role": "Data Scientist", "experience": "1 year"},
  {"name": "John Doe", "role": "Fresh Graduate", "experience": "0 years"}
];

const tableBody = document.querySelector("#candidatesTable tbody");

function loadTable(data) {
  tableBody.innerHTML = "";
  data.forEach((item, index) => {
    const row = `
      <tr>
        <td><input type="checkbox" name="selectRow" value="${index}"></td>
        <td>${item.name}</td>
        <td>${item.role}</td>
        <td>${item.experience}</td>
      </tr>
    `;
    tableBody.insertAdjacentHTML("beforeend", row);
  });
}

// Load JSON into table
loadTable(candidates);
