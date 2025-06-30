import io
import fitz  # PyMuPDF
from PIL import Image
import numpy as np

def save_upload_file(upload_file, destination):
    with open(destination, "wb") as buffer:
        buffer.write(upload_file.file.read())

def extract_text(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_images(path):
    doc = fitz.open(path)
    images = []
    for page in doc:
        for img in page.get_images(full=True):
            xref = img[0]
            base = doc.extract_image(xref)
            images.append(Image.open(io.BytesIO(base['image'])))
    return images

def create_heatmap(image):
    arr = np.array(image.convert('L'))
    heatmap = (arr - arr.min()) / (arr.max() - arr.min()) * 255
    return Image.fromarray(heatmap.astype(np.uint8))