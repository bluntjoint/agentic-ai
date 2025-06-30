# 🤖 Agent Interaction Flow (LangChain)

This standalone document explains how each LangChain-based agent ingests inputs, processes data, and produces responses. Use this as an in-depth reference for developer or stakeholder understanding.

---

## 1. Common Lifecycle

1. **Initialization**

   * Instantiate agent class in `backend/app.py`:

     ```python
     incident_agent = IncidentRecallAgent()
     pdf_agent = PDFQAAgent()
     img_agent = ImageVerificationAgent()
     ```
2. **Data Loading**

   * Files are uploaded via `/api/upload` endpoints and saved to disk.
   * Each agent’s `load_...` method is invoked with `(file_id, path)`.
3. **In-Memory Storage**

   * Agents store preprocessed data (DataFrame, embeddings, images) in dictionaries keyed by `file_id`.
4. **Handling Queries**

   * On `POST /api/chat`, backend routes to `agent.handle(message)`.
   * `message` payload may include `file_id` and query text separated by `::`.
5. **Response Construction**

   * Agents return a list of structured messages (text or Base64 images).
   * Backend returns JSON `{ messages: [...] }` to frontend.

---

## 2. IncidentRecallAgent Flow

```mermaid
flowchart LR
  subgraph IncidentRecallAgent
    A[load_incidents(path)] --> B[pandas.read_excel]
    B --> C[store DataFrame in self.incidents]
    D[handle("file_id::keyword")] --> E[filter self.incidents by substring]
    E --> F[construct JSON messages]
  end
```

1. **load\_incidents(path)**

   * Read Excel into `pandas.DataFrame`
   * Convert to list of dicts: `self.incidents`
2. **handle(payload)**

   * Parse `file_id` (not used) and `query` text
   * Substring-match across incident records
   * Build response messages:

     ```json
     [{"sender": "bot", "text": "Found X incidents:"}, ...]
     ```

---

## 3. PDFQAAgent Flow

```mermaid
flowchart TD
  subgraph PDFQAAgent
    A[load_document(id, path)] --> B[extract_text(path)]
    B --> C[split_text(chunks)]
    C --> D[OpenAIEmbeddings.embed(chunks)]
    D --> E[FAISS.from_texts(chunks, embeddings)]
    E --> F[store vectorstore in self.vectors[id]]
    
    G[handle("id::question")] --> H[vectorstore.similarity_search(question)]
    H --> I[load_qa_chain(OpenAI)]
    I --> J[chain.run(docs, question)]
    J --> K[return [{sender, text: answer}]]
  end
```

1. **load\_document(doc\_id, path)**

   * Extract full text from PDF with PyMuPDF
   * Split into overlapping chunks via `CharacterTextSplitter`
   * Compute embeddings using `OpenAIEmbeddings`
   * Create FAISS vector store and save to `self.vectors[doc_id]`
2. **handle(payload)**

   * Split into `file_id` and `question`
   * Retrieve vectorstore by `file_id`
   * Perform `similarity_search(question)` → returns top document chunks
   * Initialize QA chain: `load_qa_chain(OpenAI(), chain_type="stuff")`
   * Run chain: `chain.run(input_documents=docs, question=question)`
   * Return answer wrapped in message format

---

## 4. ImageVerificationAgent Flow

```mermaid
flowchart LR
  subgraph ImageVerificationAgent
    A[load_document(id, path)] --> B[extract_images(path)]
    B --> C[for each image: create_heatmap(img)]
    C --> D[store heatmaps in self.heatmaps[id]]
    
    E[handle(file_id)] --> F[iterate heatmaps]
    F --> G[encode to Base64]
    G --> H[return [{sender, heatmap: b64}]]
  end
```

1. **load\_document(doc\_id, path)**

   * Use PyMuPDF to extract embedded images
   * For each image, generate grayscale heatmap with NumPy + Pillow
   * Store list of heatmaps in `self.heatmaps[doc_id]`
2. **handle(file\_id)**

   * Retrieve heatmaps array
   * Encode each heatmap PNG to Base64 string
   * Return list of messages containing `heatmap` field

---

## 5. Key LangChain Components

| Component                 | Description                                                              |
| ------------------------- | ------------------------------------------------------------------------ |
| **CharacterTextSplitter** | Breaks long text into fixed-size chunks with overlap to maintain context |
| **OpenAIEmbeddings**      | Converts text chunks to dense vector representations                     |
| **FAISS**                 | In-memory vector store for similarity search                             |
| **load\_qa\_chain**       | Builds a question-answering pipeline over retrieved documents            |
| **chain.run(...)**        | Executes LLM-based retrieval-augmented generation                        |

