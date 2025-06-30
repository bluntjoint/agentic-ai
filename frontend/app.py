import streamlit as st
import requests
import os
import base64

BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:8001')

st.title('Agentic System Dashboard')
mode = st.sidebar.selectbox('Select Scenario', ['Incident Recall', 'PDF Q&A', 'Document Verification'])

if mode == 'Incident Recall':
    st.header('Upload Incidents Excel')
    incident_file = st.file_uploader('Choose an Excel file', type=['xlsx', 'xls'])
    if incident_file:
        files = {'file': (incident_file.name, incident_file, incident_file.type)}
        resp = requests.post(f"{BACKEND_URL}/api/upload/incidents", files=files)
        file_id = resp.json().get('file_id')
        st.success(f'Loaded incidents file: {file_id}')
        query = st.text_input('Ask about incidents (keyword)')
        if st.button('Get Incidents') and query:
            payload = {'scenario': 'incident', 'message': f"{file_id}::{query}"}
            chat = requests.post(f"{BACKEND_URL}/api/chat", json=payload).json()
            for msg in chat['messages']:
                st.write(f"**{msg['sender']}**: {msg.get('text', '')}")

elif mode == 'PDF Q&A':
    st.header('Upload PDF Document')
    pdf_file = st.file_uploader('Choose a PDF', type=['pdf'])
    if pdf_file:
        files = {'file': (pdf_file.name, pdf_file, pdf_file.type)}
        resp = requests.post(f"{BACKEND_URL}/api/upload/pdf", files=files)
        file_id = resp.json().get('file_id')
        st.success(f'PDF uploaded: {file_id}')
        question = st.text_input('Ask a question')
        if st.button('Get Answer') and question:
            payload = {'scenario': 'pdf_qa', 'message': f"{file_id}::{question}"}
            chat = requests.post(f"{BACKEND_URL}/api/chat", json=payload).json()
            for msg in chat['messages']:
                st.write(f"**{msg['sender']}**: {msg.get('text', '')}")

else:
    st.header('Document Verification')
    doc_file = st.file_uploader('Choose a PDF for verification', type=['pdf'])
    if doc_file:
        files = {'file': (doc_file.name, doc_file, doc_file.type)}
        resp = requests.post(f"{BACKEND_URL}/api/upload/pdf", files=files)
        file_id = resp.json().get('file_id')
        st.success(f'Document uploaded: {file_id}')
        if st.button('Validate Document'):
            payload = {'scenario': 'image_verify', 'message': file_id}
            chat = requests.post(f"{BACKEND_URL}/api/chat", json=payload).json()
            for item in chat['messages']:
                if item.get('heatmap'):
                    img_data = base64.b64decode(item['heatmap'])
                    st.image(img_data, caption='Heatmap')
                else:
                    st.write(f"**{item['sender']}**: {item.get('text', '')}")