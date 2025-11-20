import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from Schema import text_request
from fastapi import FastAPI 
import uvicorn 
from RAG_pipeline import rag_pipeline,rag_flow
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from Fine_tuned import medical_chat
from dotenv import load_dotenv 

load_dotenv()

model = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    global default_session_id
    with open("mental_health.txt", "r", encoding="utf-8") as f:
        text = f.read()

    docs = [
        {"id": "doc1", "text": text, "meta": {"title": "Mental Health Overview"}}
    ]
    model_instance = rag_pipeline.RAGChatbot(docs)
    second_model_instance= medical_chat.MedicalChat("YeBhoneLin10/FTL-Capstone-v2")
    
    model["Mic_Chat"] = model_instance
    model['Medical_Chat'] = second_model_instance
    yield
    model.clear()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/Mic_Chat")
def medical_textRequest(user_input:text_request.TextRequestModel):


    mic_chat = model['Mic_Chat'].ask(user_input.user_input)


    return {"response": mic_chat}

@app.post("/Medical_Chat")
def medical_textRequest(user_input:text_request.TextRequestModel):


    medical_chat = model['Medical_Chat'].predict(user_input.user_input)


    return {"response": medical_chat}