const textarea = document.getElementById("reqText");
const preview = document.getElementById("preview");
const textareaBox = document.querySelector(".textarea-box");
const uploadSection = document.querySelector(".upload-section");
const tableSection = document.querySelector(".table-section");

// Step 1: Enter Requirement → Hide textarea, show upload
textarea.addEventListener("input", () => {
  if (textarea.value.trim() !== "") {
    const text = textarea.value;
    preview.innerText = text;
    textareaBox.style.display = "none";   // hide textarea
    uploadSection.style.display = "block"; // show upload section

    // Send requirement to Flask
    fetch("/job_desc", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ requirement: text })
    })
    .then(res => res.json())
    .then(data => console.log("✅ Requirement uploaded:", data))
    alert("uploaded")
    .catch(err => console.error("❌ Error sending requirement:", err));
  }
});

// Step 2: Upload PDF files
const uploadForm = document.getElementById("uploadForm");
uploadForm.addEventListener("submit", function(e) {
  e.preventDefault();
  const formData = new FormData(uploadForm);

  fetch("/Review_panel", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    console.log("✅ Files uploaded:", data);
    uploadSection.style.display = "none";  // hide upload section
    tableSection.style.display = "block";  // show table section
    loadTable(data); // use backend JSON
  })
  .catch(err => console.error("❌ Error uploading resumes:", err));
});

// Step 3: Populate table
const tableBody = document.querySelector("#candidatesTable tbody");

function loadTable(data) {
  tableBody.innerHTML = "";
  data.forEach((item, index) => {
    const row = document.createElement("tr");
      row.innerHTML = `
        <td><input type="checkbox" name="selectRow" value="${index}"></td>
        <td>${item.name}</td>
        <td>${item.email}</td>
        <td>${item.phone}</td>
        <td>${item.performance_score}</td>
        <td id="summary-${index}"></td>
      </tr>
    `;
    tableBody.appendChild(row);

    typeWriter(item.summary,`summary-${index}`,25)
  });
}

function typeWriter(text,elementId,speed=30){
  let i = 0;
  const element = document.getElementById(elementId);
  
  function typing(){
    if(i<text.length){
      element.innerHTML += text.charAt(i);
      i++;
      setTimeout(typing,speed)
    }
  }
  typing();
}