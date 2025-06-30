# 📦 README.md

Welcome to the **Agentic System Chatbot**, a modular, AI-driven platform that helps teams:

* 🚀 **Incident Recall**: Instantly retrieve past incident resolutions.
* 📚 **PDF Q\&A**: Ask questions on long-form documents.
* 🕵️ **Document Verification**: Detect tampered sections in PDFs via heatmaps.

---

## 🔧 Installation & Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-repo/agentic-chatbot.git
   cd agentic-chatbot
   ```

2. **Create & configure** `.env`

   ```ini
   OPENAI_API_KEY=your_openai_key
   UPLOAD_FOLDER=./uploads
   ```

3. **Launch with Docker Compose**

   ```bash
   docker-compose up --build
   ```

   * Frontend: [http://localhost:8501](http://localhost:8501) (Streamlit)
   * Backend API: [http://localhost:8001](http://localhost:8001) (FastAPI)

---

## 🗂️ Repository Structure

```plaintext
.
├── docker-compose.yml       # Orchestrates frontend & backend
├── .env.example             # Environment variable template
├── frontend/                # Streamlit UI
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
└── backend/                 # FastAPI + LangChain agents
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py               # API routes
    ├── agents.py            # Agent implementations
    └── utils.py             # File + PDF/Image helpers
```

---

## 🧠 Agents & Usage

### 1. IncidentRecallAgent

* **Loads**: Excel file of incidents
* **Handles**: Keyword queries to filter past incidents
* **Usage**:

  1. Upload `.xlsx` via UI.
  2. Enter a search term (e.g., "timeout").
  3. Bot returns matching incident records.

### 2. PDFQAAgent

* **Loads**: PDF documents, splits and embeds text
* **Handles**: Natural-language questions
* **Usage**:

  1. Upload a PDF via UI.
  2. Ask a question (e.g., "What is the main conclusion?").
  3. Bot returns an answer based solely on the PDF content.

### 3. ImageVerificationAgent

* **Loads**: Extracted images from PDFs
* **Handles**: Tamper detection via heatmap generation
* **Usage**:

  1. Upload a PDF for verification.
  2. Click **Validate Document**.
  3. Inspect returned heatmaps highlighting suspicious areas.

---

## 🎨 UI & Theming

* Built with **Streamlit** for rapid prototyping.
* **Sidebar** navigation with clear emoji icons.
* Color accents:

  * **Blue** for headers (`#1f77b4`)
  * **Green** for success messages (`#2ca02c`)
  * **Red** for errors (`#d62728`)

Customize by editing `frontend/app.py`:

```python
st.set_page_config(
    page_title='Agentic Dashboard',
    page_icon='🤖',
    layout='wide',
)
```

---

## 🚀 Running the Application

1. Ensure Docker and Docker Compose are installed.

2. Fill in `.env` with your OpenAI key.

3. Start services:

   ```bash
   docker-compose up --build
   ```

4. Open http\://localhost:8501 in your browser.
