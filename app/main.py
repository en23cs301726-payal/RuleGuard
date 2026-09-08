from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from .decision import decide

app = FastAPI(
    title="RuleGuard",
    description="AI-powered academic regulation reasoning system",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
def home():

    return """
<!DOCTYPE html>
<html>
<head>
    <title>RuleGuard</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f4f6f8;
            margin: 0;
        }

        header {
            background: #1f2937;
            color: white;
            text-align: center;
            padding: 30px;
        }

        header h1 {
            margin: 0;
            font-size: 34px;
        }

        .container {
            max-width: 850px;
            margin: 40px auto;
            padding: 25px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }

        textarea {
            width: 100%;
            height: 120px;
            padding: 12px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 8px;
            box-sizing: border-box;
        }

        button {
            margin-top: 15px;
            padding: 12px 25px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background: #1d4ed8;
        }

        #result {
            margin-top: 30px;
        }

        .box {
            background: #f9fafb;
            padding: 18px;
            margin-top: 15px;
            border-radius: 8px;
        }

        .status {
            font-size: 20px;
            font-weight: bold;
        }

        .citation {
            margin-top: 12px;
            padding: 15px;
            background: #eef2ff;
            border-radius: 8px;
        }
    </style>
</head>

<body>

<header>
    <h1>🛡️ RuleGuard</h1>
    <p>AI-Powered Academic Regulation Reasoning System</p>
</header>

<div class="container">

    <h2>Ask RuleGuard</h2>

    <textarea id="question"
        placeholder="Example: What happens if a student misses an examination?">
    </textarea>

    <button onclick="askQuestion()">Ask RuleGuard</button>

    <div id="result"></div>

</div>

<script>

async function askQuestion() {

    const question = document.getElementById("question").value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    document.getElementById("result").innerHTML =
        "<p>⏳ Analyzing rulebook...</p>";

    try {

        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        const data = await response.json();

        let html = `
            <div class="box">
                <div class="status">
                    Status: ${data.status.toUpperCase()}
                </div>
            </div>

            <div class="box">
                <h3>Answer</h3>
                <p>${data.answer.replace(/\\n/g, "<br>")}</p>
            </div>
        `;

        if (data.citations && data.citations.length > 0) {

            html += "<div class='box'><h3>Evidence</h3>";

            data.citations.forEach(citation => {

                html += `
                    <div class="citation">
                        <b>Section:</b> ${citation.section}<br><br>
                        <b>Source:</b> ${citation.source}<br><br>
                        <b>Similarity:</b>
                        ${citation.similarity.toFixed(4)}
                    </div>
                `;

            });

            html += "</div>";
        }

        document.getElementById("result").innerHTML = html;

    } catch (error) {

        document.getElementById("result").innerHTML =
            "<p>❌ Unable to connect to RuleGuard.</p>";

    }
}

</script>

</body>
</html>
"""


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    return decide(request.question)