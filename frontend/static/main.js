const textarea = document.getElementById("reqText");
const preview = document.getElementById("preview");
const textareaBox = document.querySelector(".textarea-box");
const uploadSection = document.querySelector(".upload-section");
const tableSection = document.querySelector(".table-section");
const tableBody = document.querySelector("#candidatesTable tbody");

let tableData = [];



const dummyCandidates = [
  {
    name: "Fadhil Hussain",
    email: "ibnhussainkv@gmail.com",
    phone: "9645343919",
    performance_score: 88,
    summary: "Full-stack developer with 5 years of experience in React, Node.js, and cloud services."
  },
  {
    name: "Bob Smith",
    email: "bob@example.com",
    phone: "9123456780",
    performance_score: 92,
    summary: "Data scientist with strong expertise in Python, ML models, and big data frameworks."
  },
  {
    name: "Charlie Brown",
    email: "charlie@example.com",
    phone: "9001122334",
    performance_score: 76,
    summary: "Frontend engineer skilled in Angular, TypeScript, and UX optimization."
  }
];


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

function loadTable(data) {
  tableData = data;
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

    typeWriter(item.summary,`summary-${index}`,25);
  });
}


//selected row to flask
document.getElementById("sendBtn").addEventListener("click", () => {
  const selectedData = [];

  document
    .querySelectorAll('input[name="selectRow"]:checked')
    .forEach((checkbox) => {
      const index = parseInt(checkbox.value);
      selectedData.push(tableData[index]);
  });

  // send to flask
  fetch("/select_candidate",{
    method: "POST",
    headers:{
      "Content-Type" : "application/json"
    },
    body: JSON.stringify(selectedData),
  })
    .then(res => res.json())
    .then(result => {
      console.log("Backend response",result);
    })
    .catch(err=>console.error("error:",err));
});


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


// Load dummy candidates immediately on page load (for testing)
document.addEventListener("DOMContentLoaded", () => {
  tableSection.style.display = "block";  // show table directly
  loadTable(dummyCandidates);
});
