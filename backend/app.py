from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, uuid
from agents import IncidentRecallAgent, PDFQAAgent, ImageVerificationAgent
from utils import save_upload_file

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', './uploads')

# Initialize agents
incident_agent = IncidentRecallAgent()
pdf_agent = PDFQAAgent()
img_agent = ImageVerificationAgent()

@app.post('/api/upload/incidents')
def upload_incidents(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_FOLDER, f"{file_id}.xlsx")
    save_upload_file(file, path)
    incident_agent.load_incidents(path)
    return {"file_id": file_id}

@app.post('/api/upload/pdf')
def upload_pdf(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_FOLDER, f"{file_id}.pdf")
    save_upload_file(file, path)
    pdf_agent.load_document(file_id, path)
    img_agent.load_document(file_id, path)
    return {"file_id": file_id}

@app.post('/api/chat')
def chat(payload: dict):
    scenario = payload.get('scenario')
    message = payload.get('message')
    if scenario == 'incident':
        response = incident_agent.handle(message)
    elif scenario == 'pdf_qa':
        response = pdf_agent.handle(message)
    elif scenario == 'image_verify':
        response = img_agent.handle(message)
    else:
        raise HTTPException(status_code=400, detail="Invalid scenario")
    return {"messages": response}