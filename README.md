# 📊 ChartInsight AI – A Multi-Agent Chart Analyzer with Azure OCR & LangGraph

**ChartInsight AI** is a web-based application that leverages **Azure Computer Vision OCR** for chart text extraction and **LangGraph Multi-Agent AI** for intelligent analysis and question answering about chart data. This project integrates multiple AI agents to preprocess data, classify chart types, validate OCR output, and generate insightful responses to user queries based on extracted chart information.

## Key Technologies Used

🧠 Powered by:
- 🔍 **Azure Computer Vision OCR** for robust text extraction
- 🤖 **LangGraph** to coordinate multi-step AI agents (OCR validation, chart type classification, context refinement, and answering)
- ⚡ **Groq + LLaMA 3-70B** for high-performance LLM responses
- ⚡ **FastAPI**: Backend API to handle image uploads, OCR extraction, and communicate with LangGraph agents.
- 🔍 **Streamlit**: Frontend to interact with the system through a web interface, allowing users to upload images and ask questions about charts.

## Features

- **Chart Text Extraction**: Use **Azure Computer Vision** OCR to extract text from charts (line, pie, bar, etc.).
- **Multi-Agent Analysis**: Automatically classify the chart type (e.g., Line, Pie, Bar) and validate OCR output for consistency.
- **Question Answering**: Using a **LangGraph-based multi-agent system**, users can ask questions about the chart's content, and the AI will provide insights based on the extracted data.
- **Clarification Handling**: If the OCR extraction is ambiguous, a clarification agent will ask follow-up questions to refine the answer.

## Project Architecture

1. **Frontend (Streamlit)**:
   - Users can upload chart images (PNG/JPG) and input questions related to the chart.
   - The frontend sends the image and question to the backend for processing.

2. **Backend (FastAPI)**:
   - Handles image uploads and communicates with the **Azure Computer Vision OCR** API to extract text.
   - The OCR text is passed to the **LangGraph multi-agent system**, which processes it through various agents:
     - **OCR Validator Agent**: Validates OCR output.
     - **Chart Classifier Agent**: Classifies the chart type (e.g., line, pie, bar).
     - **Clarification Agent**: Asks for clarification if OCR text is ambiguous.
     - **LLM Answering Agent**: Generates answers to user questions based on the chart data.

3. **LangGraph**:
   - Orchestrates the workflow of multiple AI agents to ensure that the OCR output is validated and that answers to questions are provided based on the extracted data.

## Getting Started

### Prerequisites

To run this project locally, you need to have the following installed:

- Python 3.8+
- **Azure Cognitive Services** account (for OCR)
- **FastAPI**: Web framework for backend API.
- **Streamlit**: Frontend framework.
- **LangGraph**: For multi-agent orchestration.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/DhanushGD/ChartInsight-AI.git
   cd chartinsight-ai

2. **Set up environment variables:**

Create a .env file in the root directory with the following contents:
```bash
AZURE_OCR_KEY=your_azure_ocr_key
AZURE_OCR_ENDPOINT=your_azure_ocr_endpoint
GROQ_API_KEY=your_groq_api_key
```

3. **Install dependencies:**

Create a virtual environment and install required libraries:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. **Run FastAPI Backend:**

Start the FastAPI backend for OCR extraction and AI analysis:
```bash
uvicorn main:app --reload
```
The backend should be running at http://localhost:8000.

5. **Run Streamlit Frontend:**

Start the Streamlit frontend:
```bash
streamlit run app.py
```
The frontend should be available at http://localhost:8501.

### Example Workflow
1. User uploads a chart image.
2. The Azure OCR service extracts text from the chart.
3. The LangGraph agents:
    - Validate the OCR output.
    - Classify the chart type (Line, Pie, Bar).
    - Handle any clarification if OCR output is ambiguous.
    - Generate an answer to the user’s question.
4. The LLM agent processes the question and provides an insightful response based on the extracted chart data.

### Multi-Agents Overview
ChartInsight AI uses a **LangGraph** multi-agent system, which includes:
- An **OCR Validator Agent** to check the accuracy of extracted text.
- A **Chart Type Classifier Agent** to determine the kind of chart (bar, line, pie, etc.).
- A **Context Refiner Agent** to structure and clean the extracted content.
- An **LLM Answering Agent** powered by **Meta LLaMA 3-70B-8192**, integrated via **LangChain Groq**, which interprets the user's question and provides a meaningful answer based on the OCR output.

### 📸 Screenshot Proof

📷 **Upload and Analyze Chart**

![image](https://github.com/user-attachments/assets/f59e6556-3d7b-41be-892b-4c1a4f5c4cea)

📄 **OCR Extracted Text** & 🧠 **AI-Generated Answer Using LLaMA 3-70B**

![image](https://github.com/user-attachments/assets/9ebf938c-400f-47f0-bda5-48df8090dd75)

### Contributing
Feel free to fork this repository, make improvements, or submit issues for bugs or enhancements. Contributions are always welcome!

