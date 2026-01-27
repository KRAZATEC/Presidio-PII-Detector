const API = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:8000"
: "https://presidio-pii-detector-production.up.railway.app"
let lastEntities = [];
let lastText = "";
let isPDF = false;

/* ================= THRESHOLD ================= */
document.getElementById("threshold").oninput = e => {
  document.getElementById("thresholdValue").innerText = e.target.value;
};

/* ================= CLEAN ENTITIES ================= */
function cleanEntities(entities) {
  const allowed = [
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "PAN",
    "AADHAAR",
    "VOTER_ID",
    "IBAN_CODE",
    "CREDIT_CARD",
    "LOCATION",
    "ORG_ID" // ✅ CRITICAL
  ];

  let filtered = entities.filter(e => allowed.includes(e.entity));

  const map = {};
  filtered.forEach(e => {
    const key = `${e.start}-${e.end}`;
    if (!map[key] || map[key].confidence < e.confidence) {
      map[key] = e;
    }
  });

  return Object.values(map).sort((a, b) => a.start - b.start);
}

/* ================= HIGHLIGHT ================= */
function highlightText(text, entities) {
  let result = text;
  const clean = cleanEntities(entities).sort((a, b) => b.start - a.start);

  clean.forEach(e => {
    const span = `
      <span class="highlight ${e.entity}">
        ${text.slice(e.start, e.end)}
        <sup>${e.confidence}</sup>
      </span>
    `;
    result = result.slice(0, e.start) + span + result.slice(e.end);
  });

  return result;
}

/* ================= ANALYZE TEXT ================= */
async function analyzeText() {
  isPDF = false;
  document.getElementById("tabHighlight").disabled = false;

  const text = document.getElementById("inputText").value;
  const threshold = document.getElementById("threshold").value;

  const res = await fetch(`${API}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, threshold })
  });

  const data = await res.json();
  lastText = text;
  lastEntities = cleanEntities(data.entities);

  renderResults();
  showView("highlight");
}

/* ================= MASK ================= */
async function maskText() {
  const text = document.getElementById("inputText").value;

  const res = await fetch(`${API}/mask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  const data = await res.json();
  document.getElementById("highlightView").innerText = data.masked;
}

/* ================= ANALYZE PDF ================= */
async function analyzePDF() {
  isPDF = true;
  document.getElementById("tabHighlight").disabled = true;

  document.getElementById("highlightView").innerHTML =
    "⚠ Highlight is available only for text input.";

  const file = document.getElementById("pdfFile").files[0];
  if (!file) return alert("Select a PDF file");

  const form = new FormData();
  form.append("file", file);

  const res = await fetch(`${API}/upload-pdf`, {
    method: "POST",
    body: form
  });

  const data = await res.json();
  lastText = "";
  lastEntities = cleanEntities(data.entities);

  renderTable();
  document.getElementById("jsonView").innerText =
    JSON.stringify(lastEntities, null, 2);

  showView("table");
}

/* ================= RENDER ================= */
function renderResults() {
  document.getElementById("highlightView").innerHTML =
    highlightText(lastText, lastEntities);

  renderTable();

  document.getElementById("jsonView").innerText =
    JSON.stringify(lastEntities, null, 2);
}

function renderTable() {
  let html = `
    <table>
      <tr>
        <th>Entity</th>
        <th>Value</th>
        <th>Confidence</th>
        <th>Start</th>
        <th>End</th>
      </tr>
  `;

  lastEntities.forEach(e => {
    html += `
      <tr>
        <td>${e.entity}</td>
        <td>${e.value}</td>
        <td>${e.confidence}</td>
        <td>${e.start}</td>
        <td>${e.end}</td>
      </tr>
    `;
  });

  html += "</table>";
  document.getElementById("tableView").innerHTML = html;
}

/* ================= VIEW SWITCH ================= */
function showView(view) {
  ["highlightView", "tableView", "jsonView"].forEach(v =>
    document.getElementById(v).classList.add("hidden")
  );

  document.getElementById(view + "View").classList.remove("hidden");

  document.querySelectorAll(".tabs button").forEach(b =>
    b.classList.remove("active")
  );

  event.target.classList.add("active");
}

/* ================= DOWNLOAD ================= */
function downloadJSON() {
  downloadFile("entities.json", JSON.stringify(lastEntities, null, 2));
}

function downloadCSV() {
  let csv = "Entity,Value,Confidence,Start,End\n";
  lastEntities.forEach(e => {
    csv += `${e.entity},${e.value},${e.confidence},${e.start},${e.end}\n`;
  });
  downloadFile("entities.csv", csv);
}

function downloadFile(name, content) {
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([content]));
  a.download = name;
  a.click();
}
