from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import os
import random
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-70b-8192",
    temperature=0
)

# === Define State ===
class ChartState(dict):
    ocr_text: str
    question: str
    answer: str
    chart_type: str
    validated_ocr_text: str
    clarification_needed: bool

# === Step 1: Preprocess question ===
def parse_question(state: ChartState) -> ChartState:
    return {**state, "question": state["question"].strip()}

# === Step 2: Validate OCR output ===
def validate_ocr_output(state: ChartState) -> ChartState:
    ocr_text = state["ocr_text"]
    if not ocr_text or len(ocr_text.strip()) == 0:
        return {**state, "validated_ocr_text": "OCR failed or no text found.", "clarification_needed": True}
    return {**state, "validated_ocr_text": ocr_text, "clarification_needed": False}

# === Step 3: Classify chart type (Line, Pie, Bar) ===
def classify_chart_type(state: ChartState) -> ChartState:
    # Placeholder classifier (this can be replaced with a real model)
    if "pie" in state["ocr_text"].lower():
        chart_type = "Pie Chart"
    elif "bar" in state["ocr_text"].lower():
        chart_type = "Bar Chart"
    else:
        chart_type = "Line Chart"
    
    return {**state, "chart_type": chart_type}

# === Step 4: Generate answer using LLM ===
def generate_answer(state: ChartState) -> ChartState:
    ocr_text = state["validated_ocr_text"]
    question = state["question"]

    if state["clarification_needed"]:
        answer = "Please clarify your question or check the OCR text."
    else:
        prompt = [
            SystemMessage(content="You are a financial analyst AI. Answer questions using only the extracted chart data."),
            HumanMessage(content=f"""--- Chart Text ---\n{ocr_text}\n------------------\nQuestion: {question}\nChart Type: {state['chart_type']}""")
        ]
        response = llm.invoke(prompt)
        answer = response.content.strip()

    return {**state, "answer": answer}

# === LangGraph Definition ===
def build_graph():
    builder = StateGraph(ChartState)
    builder.add_node("parse_question", RunnableLambda(parse_question))
    builder.add_node("validate_ocr_output", RunnableLambda(validate_ocr_output))
    builder.add_node("classify_chart_type", RunnableLambda(classify_chart_type))
    builder.add_node("generate_answer", RunnableLambda(generate_answer))
    
    builder.set_entry_point("parse_question")
    builder.add_edge("parse_question", "validate_ocr_output")
    builder.add_edge("validate_ocr_output", "classify_chart_type")
    builder.add_edge("classify_chart_type", "generate_answer")
    builder.add_edge("generate_answer", END)
    
    return builder.compile()

graph = build_graph()

# === External callable function ===
def run_chart_insight(ocr_text: str, question: str) -> str:
    result = graph.invoke({"ocr_text": ocr_text, "question": question})
    return result["answer"]
