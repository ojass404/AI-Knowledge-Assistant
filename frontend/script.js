// ======================================================
// Backend API
// ======================================================

const API = "http://127.0.0.1:8000";

// ======================================================
// Upload PDF
// ======================================================

async function uploadPDF() {

    const file = document.getElementById("pdfFile").files[0];

    if (!file) {

        alert("Please choose a PDF.");

        return;

    }

    const formData = new FormData();

    formData.append("file", file);

    document.getElementById("uploadStatus").innerHTML =
        "Uploading PDF...";

    try {

        const response = await fetch(API + "/upload", {

            method: "POST",

            body: formData

        });

        if (!response.ok) {

            throw new Error("Upload failed");

        }

        const data = await response.json();

        document.getElementById("uploadStatus").innerHTML =
            `✅ Uploaded successfully
            <br>
            Pages : ${data.pages}
            <br>
            Chunks : ${data.chunks}
            <br>
            Embeddings : ${data.embeddings}`;

    }

    catch (error) {

        console.error(error);

        document.getElementById("uploadStatus").innerHTML =
            "❌ Upload Failed";

    }

}

    function currentTime() {

    return new Date().toLocaleTimeString([], {

        hour: "2-digit",

        minute: "2-digit"

    });

}
// ======================================================
// Chat UI Helpers
// ======================================================

function addUserMessage(text) {

    const chatBox = document.getElementById("chatBox");

    chatBox.innerHTML += `

        <div class="user">

            <div class="message">

                ${text}

                <div class="time">

                    ${currentTime()}

                </div>

            </div>

        </div>

    `;

    chatBox.scrollTo({

        top: chatBox.scrollHeight,

        behavior: "smooth"

    });

}

function addBotMessage(answer, sources = []) {

    const chatBox = document.getElementById("chatBox");

    let citationHTML = "";

    if (sources && sources.length > 0) {

        citationHTML = `
            <div class="sources">
                <hr>
                <strong>📚 Sources</strong>
        `;

        sources.forEach(source => {

            citationHTML += `

                <div class="source-card">

                    <b>📄 ${source.filename}</b><br>

                    Page ${source.page}

                </div>

            `;

        });

        citationHTML += `</div>`;
    }

    chatBox.innerHTML += `

        <div class="bot">

            <div class="message">

                ${marked.parse(answer)}

                ${citationHTML}

                <div class="time">

                    ${currentTime()}

                </div>

            </div>

        </div>

    `;

    chatBox.scrollTop = chatBox.scrollHeight;

}
// ======================================================
// Typing Indicator
// ======================================================

function showTyping() {

    const chatBox = document.getElementById("chatBox");

    chatBox.innerHTML += `

        <div class="bot" id="typingIndicator">

            <div class="message">

                <div class="typing">

                    <span></span>

                    <span></span>

                    <span></span>

                </div>

            </div>

        </div>

    `;

    chatBox.scrollTo({

        top: chatBox.scrollHeight,

        behavior: "smooth"

    });

}
function removeTyping() {

    const typing = document.getElementById("typingIndicator");

    if (typing) {

        typing.remove();

    }

}

async function typeMessage(element, text) {

    element.innerHTML = marked.parse(text);

}// ======================================================
// Ask Question
// ======================================================

async function askQuestion() {

    const input = document.getElementById("question");

    const question = input.value.trim();

    if (question === "") return;

    addUserMessage(question);

    input.value = "";

    showTyping();

    try {

        const response = await fetch(API + "/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const result = await response.json();

        removeTyping();

        addBotMessage(
            result.answer,
            result.sources
        );

    }

    catch (error) {

        removeTyping();

        console.error(error);

        addBotMessage("❌ Unable to connect to backend.");

    }

}
// ======================================================
// Clear Chat
// ======================================================

async function clearChat() {

    document.getElementById("chatBox").innerHTML = "";

    try {

        await fetch(API + "/clear-chat", {

            method: "POST"

        });

    }

    catch (error) {

        console.error(error);

    }

}

// ======================================================
// AI Form Filler
// ======================================================

async function extractInformation() {

    const fieldsText = document
        .getElementById("fields")
        .value
        .trim();

    if (fieldsText === "") {
        alert("Please enter at least one field.");
        return;
    }

    const fields = fieldsText
    .split(",")
    .map(item => item.trim().toLowerCase())
    .filter(item => item.length > 0);

    document.getElementById("extractedResult").innerHTML =
        "Extracting...";

    try {

        const response = await fetch(API + "/extract", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({

                question:
                    `Extract the following fields exactly from the uploaded PDF: ${fields.join(", ")}`,

                fields: fields

            })

        });

        const result = await response.json();

        document.getElementById("extractedResult").innerHTML =

            `<pre>${JSON.stringify(result, null, 4)}</pre>`;

    }

    catch (error) {

        console.error(error);

        document.getElementById("extractedResult").innerHTML =
            "❌ Extraction Failed";

    }

}

// ======================================================
// Notes Summarizer
// ======================================================

async function generateSummary() {

    const type =
        document.getElementById(
            "summaryType"
        ).value;

    document.getElementById(
        "summaryResult"
    ).innerHTML =
        "Generating Summary...";

    try {

        const response =
            await fetch(API + "/summarize", {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json"

                },

                body: JSON.stringify({

                    summary_type: type

                })

            });

        const result =
            await response.json();

        document.getElementById("summaryResult").innerHTML =
            marked.parse(result.answer);

    }

    catch (error) {

        console.error(error);

        document.getElementById(
            "summaryResult"
        ).innerHTML =
            "❌ Summary Generation Failed";

    }

}

// ======================================================
// Tab Switching
// ======================================================

function showTab(tab) {

    document.getElementById("chatTab").style.display = "none";
    document.getElementById("summaryTab").style.display = "none";

    if (tab === "chat") {

        document.getElementById(
            "chatTab"
        ).style.display = "block";

    }

    if (tab === "extract") {

        document.getElementById(
            "extractTab"
        ).style.display = "block";

    }

    if (tab === "summary") {

        document.getElementById(
            "summaryTab"
        ).style.display = "block";

    }

}

// ======================================================
// Enable "Enter" Key to Send Chat Message
// ======================================================

document.addEventListener("DOMContentLoaded", () => {

    const questionInput = document.getElementById("question");

    if (questionInput) {

        questionInput.addEventListener("keypress", function(event) {

            if (event.key === "Enter") {

                event.preventDefault();

                askQuestion();

            }

        });

        questionInput.focus();

    }

});

// ======================================================
// Button Loading Helpers
// ======================================================

function disableButton(buttonId, text = "Please wait...") {

    const button = document.getElementById(buttonId);

    if (!button) return;

    button.dataset.originalText = button.innerHTML;

    button.disabled = true;

    button.innerHTML = text;

}

function enableButton(buttonId) {

    const button = document.getElementById(buttonId);

    if (!button) return;

    button.disabled = false;

    if (button.dataset.originalText) {

        button.innerHTML = button.dataset.originalText;

    }

}

// ======================================================
// Future Utility
// ======================================================

function showError(message) {

    alert(message);

}

function showSuccess(message) {

    console.log(message);

}

function currentTime() {

    return new Date().toLocaleTimeString([], {

        hour: "2-digit",

        minute: "2-digit"

    });

}
async function exportChat() {

    const chat = document.getElementById("chatBox").innerText;

    const response = await fetch(API + "/export/pdf", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            title: "Chat History",

            content: chat

        })

    });

    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "Chat.pdf";

    a.click();

    window.URL.revokeObjectURL(url);

}

async function exportSummary() {

    const summary = document.getElementById("summaryResult").innerText;

    const response = await fetch(API + "/export/pdf", {

        method: "POST",

        headers: {

            "Content-Type": "application/json"

        },

        body: JSON.stringify({

            title: "Summary",

            content: summary

        })

    });

    const blob = await response.blob();

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "Summary.pdf";

    a.click();

    URL.revokeObjectURL(url);

}

async function exportExtraction() {

    const text =
        document.getElementById(
            "extractedResult"
        ).innerText;

    const response =
        await fetch(API + "/export/pdf", {

            method: "POST",

            headers: {

                "Content-Type":"application/json"

            },

            body: JSON.stringify({

                title:"Extracted Information",

                content:text

            })

        });

    const blob = await response.blob();

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");

    a.href = url;

    a.download = "Extraction.pdf";

    a.click();

    URL.revokeObjectURL(url);

}