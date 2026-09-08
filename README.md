# 🛡️ RuleGuard

## AI-Powered Academic Regulation Reasoning System

RuleGuard is an AI-powered question-answering system designed to reason over academic regulations and institutional policies.

Unlike a conventional chatbot that simply generates an answer, RuleGuard retrieves relevant provisions from a rulebook corpus and classifies each query into one of three outcomes:

* **ANSWERED** — The corpus contains sufficient information to answer the question.
* **NOT_COVERED** — The corpus does not contain enough information to answer the question.
* **CONFLICT** — Two or more relevant provisions in the corpus contain contradictory rules.

Every response is accompanied by evidence showing the relevant **source document, section reference, and semantic similarity score**.

---

## 🎯 Problem Statement

Academic rulebooks often contain many regulations distributed across different documents and sections.

A student may ask a simple question such as:

> What is the minimum attendance required to appear for an examination?

A traditional keyword-based system may retrieve one rule and ignore another rule that contradicts it.

RuleGuard addresses this problem by combining:

1. Semantic search
2. Evidence retrieval
3. Similarity scoring
4. Rule-based decision logic
5. Conflict detection
6. Explicit handling of unanswered questions

The goal is to make the system **evidence-driven and transparent**, rather than blindly generating answers.

---

## 💡 Key Features

### 1. Semantic Search

RuleGuard uses sentence embeddings to find regulations that are semantically related to the user's question.

### 2. Evidence-Based Answers

Each answer provides supporting evidence including:

* Source document
* Section/reference
* Similarity score

### 3. Conflict Detection

The system identifies situations where two relevant regulations disagree.

### 4. NOT_COVERED Detection

When the corpus does not contain sufficient information, RuleGuard does not fabricate an answer.

Instead, it returns:

```text
NOT_COVERED
```

### 5. Mixed-Format Corpus

The corpus supports multiple document formats:

* Markdown
* CSV
* PDF

### 6. FastAPI Backend

The reasoning service is exposed through a FastAPI application with a single primary QA endpoint:

```text
POST /ask
```

### 7. Web Interface

A simple browser-based interface allows users to:

* Enter questions
* View the classification
* Read the answer
* Inspect supporting evidence

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    │  Academic Question  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI /ask     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Semantic Search   │
                    │ Sentence Transformer│
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Relevant Passages   │
                    │ + Similarity Scores │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Decision Engine     │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
        ┌───────────┐    ┌─────────────┐   ┌───────────┐
        │ ANSWERED  │    │ NOT_COVERED │   │  CONFLICT │
        └───────────┘    └─────────────┘   └───────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Answer + Evidence   │
                    │ Section + Source    │
                    │ Similarity Score    │
                    └─────────────────────┘
```

---

# 🧠 How RuleGuard Works

## Step 1 — Corpus Ingestion

The ingestion pipeline reads academic regulation documents from the `data/` directory.

Supported formats include:

* `.md`
* `.csv`
* `.pdf`

The documents are divided into passages.

---

## Step 2 — Embedding Generation

Each passage is converted into a numerical vector using:

```text
all-MiniLM-L6-v2
```

The generated embeddings are stored for efficient semantic retrieval.

---

## Step 3 — Question Embedding

When a user submits a question, the question is converted into an embedding using the same model.

---

## Step 4 — Similarity Search

RuleGuard calculates semantic similarity between the question and stored regulation passages.

The most relevant passages are retrieved.

---

## Step 5 — Decision Logic

The decision engine evaluates the retrieved passages.

### ANSWERED

If sufficiently relevant information is found and no contradiction is detected:

```text
STATUS: ANSWERED
```

### NOT_COVERED

If no sufficiently relevant regulation is found:

```text
STATUS: NOT_COVERED
```

### CONFLICT

If multiple relevant provisions address the same topic but contain contradictory requirements:

```text
STATUS: CONFLICT
```

---

# 📚 Corpus

The RuleGuard corpus contains academic and institutional policy documents covering areas such as:

* Attendance
* Examinations
* Medical attendance
* Fees
* Scholarships
* Hostel regulations
* Student services
* Academic appeals
* Student conduct

The corpus uses multiple file formats to demonstrate heterogeneous document ingestion.

### Corpus Files

```text
data/
├── academic_regulations.md
├── conflict_test.md
├── examination_policy.md
├── fee_deadlines.csv
├── fee_policy.md
├── hostel_policy.md
├── scholarship_policy.md
└── student_services_policy.pdf
```

---

# ⚔️ Planted Contradictions

Three intentional contradictions were planted in the corpus to evaluate RuleGuard's conflict-detection capability.

## 1. Attendance Requirement

Existing regulation:

```text
ATT-1.2
Minimum attendance: 75%
```

Planted contradiction:

```text
ATT-CONFLICT-1
Minimum attendance: 60%
```

Test question:

```text
What is the minimum attendance required to appear for the end-semester examination?
```

Expected result:

```text
CONFLICT
```

---

## 2. Hostel Entry Time

Existing regulation:

```text
HOST-6.2
Hostel entry restriction: 10:00 PM
```

Planted contradiction:

```text
HOST-CONFLICT-1
Hostel entry restriction: 11:00 PM
```

Test question:

```text
What is the normal hostel entry time for students?
```

Expected result:

```text
CONFLICT
```

---

## 3. Medical Attendance Relaxation

Existing regulation:

```text
MED-3.2
Medical attendance may be considered as low as 65%.
```

Planted contradiction:

```text
MED-CONFLICT-1
Medical attendance may be considered as low as 60%.
```

Test question:

```text
What is the minimum attendance that may be considered for a medically verified student?
```

Expected result:

```text
CONFLICT
```

---

# 🧪 Example Queries

## Example 1 — Answered

Question:

```text
What happens if a student misses an examination?
```

Expected classification:

```text
ANSWERED
```

The response includes relevant examination regulations and their source sections.

---

## Example 2 — Not Covered

Question:

```text
What is the university's policy on parking bicycles?
```

Expected classification:

```text
NOT_COVERED
```

RuleGuard does not invent a parking regulation when the corpus does not contain one.

---

## Example 3 — Conflict

Question:

```text
What is the minimum attendance required to appear for the end-semester examination?
```

Expected classification:

```text
CONFLICT
```

The response identifies the relevant contradictory provisions.

---

# 🔌 API

## POST `/ask`

Submit an academic regulation question.

### Request

```json
{
  "question": "What is the minimum attendance required?"
}
```

### Response

```json
{
  "status": "answered",
  "answer": "Relevant regulation...",
  "citations": [
    {
      "text": "Relevant passage...",
      "source": "academic_regulations.md",
      "section": "[ATT-1.2] General Attendance Requirement",
      "similarity": 0.78
    }
  ]
}
```

For a conflict, the response contains the conflicting evidence passages.

---

# 🩺 Health Endpoint

RuleGuard also provides a simple health-check endpoint:

```text
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

# 🛠️ Technology Stack

| Technology            | Purpose                        |
| --------------------- | ------------------------------ |
| Python                | Core programming language      |
| FastAPI               | Backend API                    |
| Uvicorn               | Application server             |
| Sentence Transformers | Semantic embeddings            |
| all-MiniLM-L6-v2      | Embedding model                |
| NumPy                 | Vector similarity calculations |
| Pandas                | CSV/data processing            |
| PyPDF                 | PDF ingestion                  |
| HTML/CSS/JavaScript   | Web interface                  |

---

# 📁 Project Structure

```text
RuleGuard/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── ingest.py
│   ├── search.py
│   ├── decision.py
│   ├── models.py
│   ├── rag.py
│   │
│   └── index/
│       ├── chunks.json
│       └── embeddings.npy
│
├── data/
│   ├── academic_regulations.md
│   ├── conflict_test.md
│   ├── examination_policy.md
│   ├── fee_deadlines.csv
│   ├── fee_policy.md
│   ├── hostel_policy.md
│   ├── scholarship_policy.md
│   └── student_services_policy.pdf
│
├── frontend/
│   └── index.html
│
├── create_pdf.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/en23cs301726-payal/RuleGuard.git
cd RuleGuard
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

## 3. Activate Virtual Environment

### Windows

```powershell
.\venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Build the Search Index

Before running the application, process the corpus:

```bash
python -m app.ingest
```

The ingestion process creates:

```text
app/index/chunks.json
app/index/embeddings.npy
```

---

# ▶️ Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Open the address in a web browser to use the RuleGuard interface.

---

# 📖 API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

The documentation can be used to test the `/ask` endpoint directly.

---

# 🔍 Evidence and Explainability

A key feature of RuleGuard is that it does not return only a final answer.

Each retrieved passage contains:

```text
Source
Section
Similarity Score
Passage Text
```

Example:

```text
Section:
[ATT-1.2] General Attendance Requirement

Source:
academic_regulations.md

Similarity:
0.7826
```

This allows users to inspect **why** the system reached its classification.

---

# 🧪 Testing Strategy

RuleGuard is tested using three categories of questions.

### Category 1 — Answered

Questions whose answers exist in the corpus.

Expected:

```text
ANSWERED
```

### Category 2 — Not Covered

Questions about topics absent from the corpus.

Expected:

```text
NOT_COVERED
```

### Category 3 — Conflict

Questions targeting the three intentionally contradictory provisions.

Expected:

```text
CONFLICT
```

The three planted conflict scenarios are:

```text
Attendance      → 75% vs 60%
Hostel Entry    → 10 PM vs 11 PM
Medical Rule    → 65% vs 60%
```

---

# 🔐 What Is Mocked?

This project uses a **self-contained academic regulation corpus** for demonstration and testing.

The regulations are not intended to represent the actual policies of a real university.

The three contradictory provisions are intentionally planted test cases to evaluate the conflict-detection functionality.

No external university database or live institutional policy API is required.

---

# ⚠️ Limitations

RuleGuard is a prototype system.

Its accuracy depends on:

* Quality of the corpus
* Quality of document chunking
* Semantic similarity threshold
* Retrieval quality
* Explicit conflict patterns implemented in the decision engine

The system should therefore be treated as a **decision-support and research prototype**, not as an authoritative source of institutional policy.

---

# 🚀 Future Improvements

Possible future improvements include:

* LLM-based natural-language answer generation
* More advanced contradiction detection
* Temporal/version-aware regulations
* Automatic rule extraction
* Better handling of exceptions
* Cross-document reasoning
* Confidence calibration
* Admin dashboard
* Query history
* Regulation version tracking
* Automated evaluation benchmark
* More sophisticated semantic retrieval
* OCR support for scanned documents

---

# 👩‍💻 Project Information

**Project:** RuleGuard
**Domain:** Generative AI / Natural Language Processing / Information Retrieval
**Architecture:** Retrieval + Decision Engine
**Backend:** FastAPI
**Embedding Model:** all-MiniLM-L6-v2
**Language:** Python

---

# 🎥 Demo

Working demonstration video:

```text
[ADD GOOGLE DRIVE VIDEO LINK HERE]
```

The demonstration should show:

1. RuleGuard homepage
2. An `ANSWERED` question
3. A `NOT_COVERED` question
4. The three `CONFLICT` questions
5. Evidence section
6. Source and section references
7. Similarity scores

---

# 🔗 Repository

GitHub:

https://github.com/en23cs301726-payal/RuleGuard

---

# 📄 License

This project is developed for academic and demonstration purposes.
