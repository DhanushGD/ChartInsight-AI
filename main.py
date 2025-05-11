from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from lang import run_chart_insight
from PIL import Image
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from dotenv import load_dotenv
import os
import io
import time
import re

# === FastAPI Setup ===
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Environment Setup ===
load_dotenv()
AZURE_OCR_KEY = os.getenv("AZURE_OCR_KEY")
AZURE_OCR_ENDPOINT = os.getenv("AZURE_OCR_ENDPOINT")

# === Azure OCR Setup ===
cv_client = ComputerVisionClient(
    AZURE_OCR_ENDPOINT,
    CognitiveServicesCredentials(AZURE_OCR_KEY)
)

# === OCR Function ===
def extract_text_with_azure(image: Image.Image) -> str:
    try:
        with io.BytesIO() as img_bytes:
            image.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            response = cv_client.read_in_stream(img_bytes, language="en", raw=True)
            operation_location = response.headers["Operation-Location"]
            operation_id = operation_location.split("/")[-1]

            while True:
                result = cv_client.get_read_result(operation_id)
                if result.status not in ['notStarted', 'running']:
                    break
                time.sleep(1)

            if result.status == OperationStatusCodes.succeeded:
                lines = []
                for read_result in result.analyze_result.read_results:
                    for line in read_result.lines:
                        lines.append(line.text)
                return "\n".join(lines)
            else:
                return "OCR failed or no text found."

    except Exception as e:
        return f"Azure OCR Error: {e}"

# === Cleanup Function ===
def clean_llm_output(text: str) -> str:
    text = re.sub(r'\.(\w)', r'. \1', text)
    text = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', text)
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)
    return re.sub(r'\s+', ' ', text).strip()

# === Main Endpoint ===
@app.post("/analyze")
async def analyze_chart(file: UploadFile, question: str = Form(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        return {"error": f"Error loading image: {e}"}

    ocr_text = extract_text_with_azure(image)

    if "OCR failed" in ocr_text or "no text found" in ocr_text:
        return {"error": ocr_text}

    try:
        answer = run_chart_insight(ocr_text=ocr_text, question=question)
        return {
            "ocr_extracted_text": ocr_text,
            "llm_answer": clean_llm_output(answer)
        }
    except Exception as e:
        return {"error": f"LangGraph error: {e}"}

