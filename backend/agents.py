import io, base64
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from utils import extract_text, extract_images, create_heatmap

class IncidentRecallAgent:
    def __init__(self):
        self.incidents = []

    def load_incidents(self, path):
        df = pd.read_excel(path)
        self.incidents = df.to_dict(orient='records')

    def handle(self, payload):
        file_id, query = payload.split("::", 1)
        results = [inc for inc in self.incidents if query.lower() in str(inc).lower()]
        messages = [{"sender": "bot", "text": f"Found {len(results)} incidents:"}]
        for inc in results:
            messages.append({"sender": "bot", "text": str(inc)})
        return messages

class PDFQAAgent:
    def __init__(self):
        self.vectors = {}

    def load_document(self, doc_id, path):
        text = extract_text(path)
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_text(text)
        embeddings = OpenAIEmbeddings()
        vectorstore = FAISS.from_texts(chunks, embeddings)
        self.vectors[doc_id] = vectorstore

    def handle(self, payload):
        file_id, question = payload.split("::", 1)
        vs = self.vectors.get(file_id)
        if not vs:
            return [{"sender": "bot", "text": "Document not found."}]
        docs = vs.similarity_search(question)
        chain = load_qa_chain(OpenAI(), chain_type="stuff")
        answer = chain.run(input_documents=docs, question=question)
        return [{"sender": "bot", "text": answer}]

class ImageVerificationAgent:
    def __init__(self):
        self.heatmaps = {}

    def load_document(self, doc_id, path):
        imgs = extract_images(path)
        self.heatmaps[doc_id] = [create_heatmap(img) for img in imgs]

    def handle(self, file_id):
        hms = self.heatmaps.get(file_id)
        if not hms:
            return [{"sender": "bot", "text": "No images found."}]
        messages = []
        for idx, hm in enumerate(hms):
            buf = io.BytesIO()
            hm.save(buf, format='PNG')
            b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            messages.append({"sender": "bot", "heatmap": b64})
        return messages