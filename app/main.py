from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware 
from app.query_vectorstore import query_vectorstore
import logging
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


origins = [
    "http://localhost",  
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


logging.basicConfig(level=logging.INFO)

app.mount("/static", StaticFiles(directory = "frontend/static"), name="static")

templates = Jinja2Templates(directory="frontend/templates")

class QueryRequest(BaseModel):
    question: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/query/")
async def handle_query(request: Request):
    try:
        raw_body = await request.body()
        logger.info(f"Raw body received: {raw_body.decode('utf-8')}")

        if not raw_body:
            return {"response": "Received an empty body."}

        data = await request.json()
        logger.info(f"Raw JSON received: {data}")

        query_request = QueryRequest(**data)
        query = query_request.question

        faiss_path = "faiss_index"

        greetings = {"hi", "hello", "hey", "good morning", "good evening", "good afternoon"}

        if query.strip().lower() in greetings:
            response = "Hello! How can I assist you today?"
        elif not query.strip() or len(query.strip()) < 3:
            response = "Please ask a more specific question."
        else:
            response = query_vectorstore(query=query, db_path=faiss_path)

        # response = query_vectorstore(query=query, db_path=faiss_path)

        return {"response": response}

    except Exception as e:
        logger.error(f"Error processing the query: {e}")
        return {"response": "Error processing your query."}
