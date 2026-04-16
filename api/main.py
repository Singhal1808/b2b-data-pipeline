from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URI = os.getenv("MONGO_URI")
templates = Jinja2Templates(
    directory="templates"
)
client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = client["b2b_database"]

collection = db["startups"]

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
         request,
        "index.html",
        {
            "request": request
        }
    )

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# ...existing code...
from fastapi import FastAPI, Request, Query
import re
# ...existing code...

@app.get("/startups")
def get_startups(
    page: int = 1,
    limit: int = 50,
    search: str = Query(default="")
):
    page = max(1, page)
    limit = max(1, min(limit, 200))
    skip = (page - 1) * limit

    mongo_filter = {}

    if search.strip():
        mongo_filter["name"] = {
            "$regex": re.escape(search.strip()),
            "$options": "i"
        }

    total_records = collection.count_documents(mongo_filter)
    total_pages = (total_records + limit - 1) // limit

    data = list(
        collection.find(mongo_filter, {"_id": 0})
        .skip(skip)
        .limit(limit)
    )

    return {
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
        "data": data
    }
