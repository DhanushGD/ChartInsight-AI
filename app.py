import streamlit as st
from PIL import Image
import requests
import io

# Page Config
st.set_page_config(page_title="📊 ChartInsight AI", layout="centered")

# App Title and Description
st.title("📊 ChartInsight AI")
st.markdown("**Ask questions about uploaded chart images with AI-powered insights.**")
st.markdown("---")

# Image Upload
st.subheader("📤 Upload Chart Image")
uploaded_file = st.file_uploader("Choose a chart image (PNG, JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Open the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Chart Image", use_container_width=True)

    # Question Input
    st.subheader("❓ Ask a Question About the Chart")
    question = st.text_input("Example: Which product had the highest sales growth?")

    if question:
        with st.spinner("🔍 Extracting data and analyzing..."):
            backend_url = "http://localhost:8000/analyze"  # Change if hosted elsewhere
            files = {"file": uploaded_file.getvalue()}
            data = {"question": question}

            try:
                # Make the request to FastAPI backend
                response = requests.post(backend_url, files=files, data=data)
                result = response.json()

                # DEBUG: Show full raw response
                st.subheader("📦 Raw Backend Response")
                st.code(result)

                # Extract fields from the backend response
                ocr_text = result.get("ocr_extracted_text", "N/A")
                llm_answer = result.get("llm_answer", "N/A")

                # Display the OCR extracted text and the LLM generated answer
                st.markdown("---")
                st.subheader("📄 OCR Extracted Chart Text")
                st.code(ocr_text, language="text")

                st.subheader("🧠 LLM Answer")
                st.success(llm_answer)

            except Exception as e:
                st.error("⚠️ Failed to connect to the backend. Please check the API and try again.")
                st.exception(e)

else:
    st.info("👆 Please upload a chart image to get started.")

st.markdown("---")
st.markdown("🔧 Powered by **LangChain**, **CrewAI**, **FastAPI**, and **AZURE OCR** 🔍")
