## 🏛️ High-Level Components

```plaintext
[ User Browser ]
       ↓ HTTP
[ Streamlit Frontend (8501) ]
       ↓ API Calls
[ FastAPI Backend (8001) ]
       ↙       ↓       ↘
[Incident] [PDFQA] [ImageVerify]
  Agent      Agent       Agent
       ↘       ↓       ↙
   In-Memory Persistence
```

---

## 🧩 Component Breakdown

| Component                  | Tech                | Responsibilities                              |
| -------------------------- | ------------------- | --------------------------------------------- |
| **Frontend**               | Streamlit (Python)  | - Upload files- Chat UI- Display heatmaps     |
| **Backend API**            | FastAPI             | - Routes for uploads & chat- Agent routing    |
| **IncidentRecallAgent**    | pandas, Python      | - Read Excel- Keyword search in memory        |
| **PDFQAAgent**             | LangChain, FAISS    | - Extract & split text- Embed & QA chain      |
| **ImageVerificationAgent** | PyMuPDF, PIL, NumPy | - Extract images- Generate grayscale heatmaps |
| **Persistence**            | In-memory dicts     | - Stores incidents, vectorstores, heatmaps    |

---

## ⚙️ Data Flow

1. **Upload**: User sends file via Streamlit → Backend saves to `UPLOAD_FOLDER`.
2. **Load**: Backend agent loads data (Excel/PDF) into memory.
3. **Query**: User input forwarded to `/api/chat` with `scenario` & `message`.
4. **Process**: Selected agent executes logic.
5. **Respond**: JSON messages (and base64 images) returned to frontend.
6. **Render**: Streamlit displays text or images to the user.

